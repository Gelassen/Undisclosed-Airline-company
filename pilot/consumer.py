import json 
from kafka import KafkaConsumer

# TODO expose endpoint into config file
# TODO consumer should update record in database to give correct view on how much seats are left
if __name__ == '__main__':
    consumer = KafkaConsumer(
        'messages',
        bootstrap_servers='172.16.254.2:9092',
        auto_offset_reset='earliest'
    )
    for message in consumer: 
        print(json.loads(message.value))