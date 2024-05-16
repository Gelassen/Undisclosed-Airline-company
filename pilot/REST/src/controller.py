from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from .models import Inventory
from .database import Database, InventoryDB

router = APIRouter()

db = Database()
db.create_tables()  # Create tables if they don't exist

@router.get("/inventories/", response_model=list[Inventory])
async def get_all_inventories(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100)):
    session = db.get_session()
    try:
        items = session.query(InventoryDB).offset((page - 1) * per_page).limit(per_page).all()
        return items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()

@router.get("/inventories/search/", response_model=list[Inventory])
async def get_inventories_by_search_clause(flight: str = None, departure: int = None, flight_booking_class: str = None):
    session = db.get_session()
    try:
        query = session.query(InventoryDB)
        if flight:
            query = query.filter(InventoryDB.flight == flight)
        if departure:
            query = query.filter(InventoryDB.departure == departure)
        if flight_booking_class:
            query = query.filter(InventoryDB.flight_booking_class == flight_booking_class)
        items = query.all()
        return items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()