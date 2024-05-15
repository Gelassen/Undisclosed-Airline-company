from fastapi.testclient import TestClient
from src.controller import router
from src.database import SessionLocal, engine, Base
from src.models import Inventory

client = TestClient(router)

def setup_function():
    Base.metadata.create_all(bind=engine)


def test_search_items_by_all_fields():
    response = client.get("/inventories/search/?flight=(TYA) NORDSTAR 403&departure=1715727251000&flight_booking_class=R")
    assert response.status_code == 200
    assert response.json() == [
        {"time": 1715329740000, "flight": "(TYA) NORDSTAR 403", "departure": 1715727251000, "flight_booking_class": "R", "idle_seats_count": 9}
    ]