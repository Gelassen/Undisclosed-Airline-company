import threading
import src.forecast_service import ForecastService

if __name__ == "__main__":
    service = ForecastService()

    retrain_thread = threading.Thread(target=service.retrain_model_periodically)
    retrain_thread.start()

    service.respond_on_queue()