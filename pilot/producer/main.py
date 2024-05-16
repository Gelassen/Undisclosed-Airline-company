from src.producer import KafkaInventoryProducer

if __name__ == '__main__':
    producer = KafkaInventoryProducer()
    producer.produce_events()
