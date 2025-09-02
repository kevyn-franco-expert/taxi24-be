from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class DriverStatusEnum(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class TripStatusEnum(enum.Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DriverModel(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    status = Column(Enum(DriverStatusEnum), default=DriverStatusEnum.AVAILABLE)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PassengerModel(Base):
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TripModel(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    destination_latitude = Column(Float)
    destination_longitude = Column(Float)
    status = Column(Enum(TripStatusEnum), default=TripStatusEnum.REQUESTED)
    fare = Column(DECIMAL(10, 2))
    distance_km = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    passenger = relationship("PassengerModel")
    driver = relationship("DriverModel")


class InvoiceModel(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    
    trip = relationship("TripModel")