import time 
import json 
import random 
from datetime import datetime
from data_generator import generate_inventory
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode('utf-8')

def on_send_success(record_metadata):
    print("Message sent successfully.")
    print("Topic:", record_metadata.topic)
    print("Partition:", record_metadata.partition)
    print("Offset:", record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

# TODO expose endpoint into config file 
# TODO expose topic name into config file
producer = KafkaProducer(
    bootstrap_servers=['172.16.254.3:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':
    print('Producer has been started')
    while True:
        new_event = generate_inventory() 
        print(f'Produce new event @ {datetime.now()} : payload = {str(new_event)}')
        producer.send('Inventory', new_event).add_callback(on_send_success).add_errback(on_send_error)

        time_to_sleep = random.randint(1,7)
        time.sleep(time_to_sleep)

