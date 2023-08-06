import os
import json
import kafka

from threading import Thread
from mindsdb.utilities.config import STOP_THREADS_EVENT
# from mindsdb.utilities.log import log
from mindsdb.integrations.base import StreamIntegration
from mindsdb.streams.kafka.kafka_stream import KafkaStream
from mindsdb.interfaces.storage.db import session, Stream, Configuration

class KafkaConnectionChecker:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 9092)

    def _get_connection(self):
        return kafka.KafkaAdminClient(bootstrap_servers=f"{self.host}:{self.port}")
    def check_connection(self):
        try:
            client = self._get_connection()
            client.close()
            return True
        except Exception:
            return False


class Kafka(StreamIntegration, KafkaConnectionChecker):
    def __init__(self, config, name):
        StreamIntegration.__init__(self, config, name)
        intergration_info = self.config['integrations'][self.name]
        self.host = intergration_info.get('host')
        self.port = intergration_info.get('port', 9092)
        self.control_topic_name = intergration_info.get('topic', None)
        self.client = self._get_connection()

    def start(self):
        Thread(target=Kafka.work, args=(self, )).start()

    def start_stored_streams(self):
        existed_streams = session.query(Stream).filter_by(company_id=self.company_id, integration=self.name)

        for stream in existed_streams:
            to_launch = self.get_stream_from_db(stream)
            if stream.name not in self.streams:
                params = {"integration": stream.integration,
                          "predictor": stream.predictor,
                          "stream_in": stream.stream_in,
                          "stream_out": stream.stream_out,
                          "type": stream._type}

                self.log.error(f"Integration {self.name} - launching from db : {params}")
                to_launch.start()
                self.streams[stream.name] = to_launch.stop_event

    def work(self):
        if self.control_topic_name is not None:
            self.consumer = kafka.KafkaConsumer(bootstrap_servers=f"{self.host}:{self.port}",
                                                consumer_timeout_ms=1000)

            self.consumer.subscribe([self.control_topic_name])
            self.log.error(f"Integration {self.name}: subscribed  to {self.control_topic_name} kafka topic")
        else:
            self.consumer = None
            self.log.error(f"Integration {self.name}: worked mode - DB only.")

        while not self.stop_event.wait(0.5):
            try:
                # break if no record about this integration has found in db
                if not self.exist_in_db():
                    break
                self.start_stored_streams()
                self.stop_deleted_streams()
                if self.consumer is not None:
                    try:
                        msg_str = next(self.consumer)

                        stream_params = json.loads(msg_str.value)
                        stream = self.get_stream_from_kwargs(**stream_params)
                        stream.start()
                        # store created stream in database
                        self.store_stream(stream)
                    except StopIteration:
                        pass
            except Exception as e:
                self.log.error(f"Integration {self.name}: {e}")

        # received exit event
        self.consumer.close()
        self.stop_streams()
        session.close()
        self.log.error(f"Integration {self.name}: exiting...")

    def store_stream(self, stream):
        """Stories a created stream."""
        stream_name = f"{self.name}_{stream.predictor}"
        stream_rec = Stream(name=stream_name, host=stream.host, port=stream.port,
                            _type=stream._type, predictor=stream.predictor,
                            integration=self.name, company_id=self.company_id,
                            stream_in=stream.stream_in_name, stream_out=stream.stream_out_name)
        session.add(stream_rec)
        session.commit()
        self.streams[stream_name] = stream.stop_event

    def get_stream_from_db(self, db_record):
        kwargs = {"type": db_record._type,
                  "predictor": db_record.predictor,
                  "input_stream": db_record.stream_in,
                  "output_stream": db_record.stream_out}
        return self.get_stream_from_kwargs(**kwargs)

    def get_stream_from_kwargs(self, **kwargs):
        topic_in = kwargs.get('input_stream')
        topic_out = kwargs.get('output_stream')
        predictor_name = kwargs.get('predictor')
        stream_type = kwargs.get('type', 'forecast')
        return KafkaStream(self.host, self.port,
                           topic_in, topic_out,
                           predictor_name, stream_type)
