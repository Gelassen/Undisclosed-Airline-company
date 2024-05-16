from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()
class InventoryDB(Base):
    __tablename__ = 'Inventory'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(BigInteger, nullable=False)
    flight = Column(String(256), nullable=False)
    departure = Column(BigInteger, nullable=False)
    flight_booking_class = Column(Text, nullable=False)
    idle_seats_count = Column(Integer, nullable=False)

db_username = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = os.environ.get('POSTGRESS_HOST')

if not all([db_username, db_password, db_name, db_host]):
    raise ValueError("Missing one or more environment variables: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRESS_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
