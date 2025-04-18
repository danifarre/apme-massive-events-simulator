from kafka import KafkaProducer, errors
from kafka.errors import NoBrokersAvailable
import json


class MessagingService:
    def __init__(self):
        try:
            self._producer = KafkaProducer(bootstrap_servers=['localhost:29092', 'localhost:39092', 'localhost:49092'])
        except NoBrokersAvailable:
            self._producer = None

    def send_message(self, message, topic):
        if self._producer:
            self._producer.send(topic, json.dumps(message).encode('utf-8'))
            return 0
        else:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=['localhost:29092', 'localhost:39092', 'localhost:49092'])
                if self._producer:
                    self._producer.send(topic, json.dumps(message).encode('utf-8'))
                    return 0
                else:
                    return 1
            except NoBrokersAvailable:
                self._producer = None
                return 1
