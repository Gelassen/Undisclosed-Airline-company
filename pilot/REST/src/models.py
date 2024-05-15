from pydantic import BaseModel

class Inventory(BaseModel):
    time: int
    flight: str
    departure: int
    flight_booking_class: str
    idle_seats_count: int
