import os
import time
import threading
import pandas as pd
from kafka import Kafka
from forecast_model import ForecastModel
from database import Database, InventoryDB, Forecast

class ForecastService:
    def __init__(self):
        self.db = Database()
        self.db.create_tables()
        self.forecast_model = ForecastModel()
        self.forecast_model.load_cached_models()
        self.kafka_host = os.environ.get('KAFKA_BROKER_HOST')
        self.kafka_port = os.environ.get('KAFKA_BROKER_PORT')
        self.kafka_topic = os.environ.get('KAFKA_TOPIC')

        if not all([self.kafka_host, self.kafka_port, self.kafka_topic]):
            raise ValueError("Missing one or more environment variables: KAFKA_BROKER_HOST, KAFKA_BROKER_PORT, KAFKA_TOPIC")

    def fetch_data_from_database(self):
        session = self.db.get_session()
        query = session.query(InventoryDB).all()
        data = pd.DataFrame([item.__dict__ for item in query])
        session.close()
        return data

    def save_forecast_to_database(self, forecasts):
        session = self.db.get_session()
        for unique_id, forecast in forecasts.items():
            for record in forecast:
                forecast_entry = Forecast(
                    unique_id=unique_id,
                    forecast_time=int(record['ds'].timestamp() * 1000),
                    yhat=record['yhat'],
                    yhat_lower=record['yhat_lower'],
                    yhat_upper=record['yhat_upper']
                )
                session.add(forecast_entry)
        session.commit()
        session.close()

    def respond_on_queue(self):
        try:
            consumer = KafkaConsumer(
                kafka_topic,
                bootstrap_servers=f"{kafka_host}:{kafka_port}",
                auto_offset_reset='earliest'
            )
            for message in consumer: 
            try:
                print(json.loads(message.value))
                event_data = pd.read_json(event)
                forecasts = self.forecast_model.forecast(event_data)
                self.save_forecast_to_postgres(forecasts)
            except JSONDecodeError as jsonError:
                print("Have you put in queue invalid json?", jsonError)
                continue   
        except Exception as e:
            print("Something went wrong due consumer work", e)
        # consumer.close()

    def retrain_model_periodically(self):
        while True:
            print("Retraining model...")
            data = self.fetch_data_from_postgres()
            self.forecast_model.retrain_model(data)
            time.sleep(86400)  # Sleep for 24 hours
