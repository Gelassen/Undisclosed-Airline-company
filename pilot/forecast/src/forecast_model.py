import pandas as pd
from prophet import Prophet
import joblib
import threading

class ForecastModel:
    def __init__(self, model_cache_path="cached_models.joblib"):
        self.model_cache_path = model_cache_path
        self.cached_models = {}
        self.lock = threading.Lock()

    def load_cached_models(self):
        with self.lock:
            try:
                self.cached_models = joblib.load(self.model_cache_path)
                print("Loaded cached models from disk")
            except FileNotFoundError:
                print("No cached models found")

    def cache_models(self):
        with self.lock:
            joblib.dump(self.cached_models, self.model_cache_path)
            print(f"Cached models to disk at {self.model_cache_path}")

    def train_model(self, data):
        data['unique_id'] = data['flight'] + '_' + data['flight_booking_class']
        unique_ids = data['unique_id'].unique()

        filtered_data = data.groupby(['unique_id']).filter(lambda x: len(x) > 1)

        insufficient_data_count = filtered_data.groupby(['unique_id']).size()
        if insufficient_data_count.size > (data.shape[0] * 0.05):
            raise RuntimeError("Test data contains unacceptable amount of not valid data")

        data["time"] = pd.to_datetime(data['time'], unit="ms")
        data["departure"] = pd.to_datetime(data['departure'], unit="ms")

        with self.lock:
            for unique_id in unique_ids:
                subset = data[data['unique_id'] == unique_id]
                subset = subset.rename(columns={'departure': 'ds', 'idle_seats_count': 'y'})

                model = Prophet()
                model.fit(subset[['ds', 'y']])
                self.cached_models[unique_id] = model

            self.cache_models()

    def retrain_model(self, data):
        self.train_model(data)

    def forecast(self, new_inventory):
        new_inventory = pd.DataFrame(new_inventory)
        new_inventory['unique_id'] = new_inventory['flight'] + '_' + new_inventory['flight_booking_class']
        forecasts = {}

        with self.lock:
            for unique_id, model in self.cached_models.items():
                subset = new_inventory[new_inventory['unique_id'] == unique_id]
                if not subset.empty:
                    subset = subset.rename(columns={'departure': 'ds'})
                    future = model.make_future_dataframe(periods=30)
                    forecast = model.predict(future)
                    forecasts[unique_id] = forecast.to_dict(orient='records')

        return forecasts

# Example usage
# if __name__ == "__main__":
#     forecast_model = ForecastModel()

#     # Load cached models from disk
#     forecast_model.load_cached_models()

#     # Example data for training
#     data = pd.read_csv("your_data.csv")
#     forecast_model.train_model(data)

#     # Example new inventory data for forecasting
#     new_inventory = [
#         {"flight": "(LY) EL AL 611", "departure": 1715798945000, "flight_booking_class": "E", "idle_seats_count": 40},
#         {"flight": "(LY) EL AL 611", "departure": 1715810691000, "flight_booking_class": "V", "idle_seats_count": 25}
#     ]
#     forecasts = forecast_model.forecast(new_inventory)
#     print(forecasts)
