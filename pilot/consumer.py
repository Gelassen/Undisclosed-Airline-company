import json 
from json import JSONDecodeError
from kafka import KafkaConsumer

# TODO expose endpoint into config file
# TODO consumer should update record in database to give correct view on how much seats are left
if __name__ == '__main__':
    try:
        consumer = KafkaConsumer(
            'messages',
            bootstrap_servers='172.16.254.3:9092',
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