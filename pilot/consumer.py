import json 
from json import JSONDecodeError
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

load_dotenv("config/.env")

kafka_host = os.environ.get('KAFKA_BROKER_HOST')
kafka_port = os.environ.get('KAFKA_BROKER_PORT')
kafka_topic = os.environ.get('KAFKA_TOPIC')

# TODO consumer should update record in database to give correct view on how much seats are left
if __name__ == '__main__':
    try:
        consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=f"{kafka_host}:{kafka_port}",
            auto_offset_reset='earliest'
        )
        for message in consumer: 
            try:
                print(json.loads(message.value))
            except JSONDecodeError as jsonError:
                print("Have you put in queue invalid json?", jsonError)
                continue        
    except Exception as e:
        print("Something went wrong due consumer work", e)