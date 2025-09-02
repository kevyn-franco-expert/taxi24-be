from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class DriverStatusSchema(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class TripStatusSchema(str, Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LocationSchema(BaseModel):
    latitude: float
    longitude: float


class DriverSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    license_number: str
    status: DriverStatusSchema
    current_location: Optional[LocationSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PassengerSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TripSchema(BaseModel):
    id: Optional[int] = None
    passenger_id: int
    driver_id: Optional[int] = None
    pickup_location: LocationSchema
    destination_location: Optional[LocationSchema] = None
    status: TripStatusSchema
    fare: Optional[Decimal] = None
    distance_km: Optional[float] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvoiceSchema(BaseModel):
    id: Optional[int] = None
    trip_id: int
    amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    issued_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TripRequestSchema(BaseModel):
    passenger_id: int
    pickup_location: LocationSchema
    destination_location: Optional[LocationSchema] = None


class CompleteTripSchema(BaseModel):
    destination_location: LocationSchema
    fare: Decimal

