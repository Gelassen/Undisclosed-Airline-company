from fastapi import APIRouter, HTTPException, Query
from .models import Inventory
from .database import SessionLocal, InventoryDB

router = APIRouter()

@router.get("/items/", response_model=list[Inventory])
async def read_items(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100)):
    db = SessionLocal()
    items = db.query(InventoryDB).offset((page - 1) * per_page).limit(per_page).all()
    db.close()
    return items

@router.get("/items/search/", response_model=list[Inventory])
async def search_items(flight: str = None, departure: int = None, flight_booking_class: str = None):
    db = SessionLocal()
    query = db.query(InventoryDB)
    if flight:
        query = query.filter(InventoryDB.flight == flight)
    if departure:
        query = query.filter(InventoryDB.departure == departure)
    if flight_booking_class:
        query = query.filter(InventoryDB.flight_booking_class == flight_booking_class)
    items = query.all()
    db.close()
    return items