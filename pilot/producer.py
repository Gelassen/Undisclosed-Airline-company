import time 
import json 
import random 
from datetime import datetime
from data_generator import generate_inventory
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv("config/.env")

kafka_host = os.environ.get('KAFKA_BROKER_HOST')
kafka_port = os.environ.get('KAFKA_BROKER_PORT')
kafka_topic = os.environ.get('KAFKA_TOPIC')

def serializer(message):
    return json.dumps(message).encode('utf-8')

def on_send_success(record_metadata):
    print("Message sent successfully.")
    print("Topic:", record_metadata.topic)
    print("Partition:", record_metadata.partition)
    print("Offset:", record_metadata.offset)

def on_send_error(excp):
    log.error('An error happened while writing to kafka topic', exc_info=excp)

producer = KafkaProducer(
    bootstrap_servers=[f"{kafka_host}:{kafka_port}"],
    value_serializer=serializer
)

if __name__ == '__main__':
    print('Producer has been started')
    while True:
        new_event = generate_inventory() 
        print(f'Produce new event @ {datetime.now()} : payload = {str(new_event)}')
        producer.send(kafka_topic, new_event).add_callback(on_send_success).add_errback(on_send_error)

        time_to_sleep = random.randint(1,7)
        time.sleep(time_to_sleep)

