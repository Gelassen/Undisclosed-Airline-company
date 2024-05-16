import os
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from .data_generator import generate_inventory

class KafkaInventoryProducer:
    def __init__(self):
        self.kafka_host = os.environ.get('KAFKA_BROKER_HOST')
        self.kafka_port = os.environ.get('KAFKA_BROKER_PORT')
        self.kafka_topic = os.environ.get('KAFKA_TOPIC')

        if not all([self.kafka_host, self.kafka_port, self.kafka_topic]):
            raise ValueError("Missing one or more environment variables: KAFKA_BROKER_HOST, KAFKA_BROKER_PORT, KAFKA_TOPIC")

        self.producer = KafkaProducer(
            bootstrap_servers=[f"{self.kafka_host}:{self.kafka_port}"],
            value_serializer=self.serializer
        )

    def serializer(self, message):
        return json.dumps(message).encode('utf-8')

    def on_send_success(self, record_metadata):
        print("Message sent successfully.")
        print("Topic:", record_metadata.topic)
        print("Partition:", record_metadata.partition)
        print("Offset:", record_metadata.offset)

    def on_send_error(self, excp):
        print('An error happened while writing to kafka topic', exc_info=excp)

    def produce_events(self):
        print('Producer has been started')
        while True:
            new_event = generate_inventory()
            print(f'Produce new event @ {datetime.now()} : payload = {str(new_event)}')
            self.producer.send(self.kafka_topic, new_event).add_callback(self.on_send_success).add_errback(self.on_send_error)

            time_to_sleep = random.randint(1, 7)
            time.sleep(time_to_sleep)


