from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from decimal import Decimal


class DriverStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class TripStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class Driver:
    id: Optional[int]
    name: str
    email: str
    phone: str
    license_number: str
    status: DriverStatus
    current_location: Optional[Location]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Passenger:
    id: Optional[int]
    name: str
    email: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Trip:
    id: Optional[int]
    passenger_id: int
    driver_id: Optional[int]
    pickup_location: Location
    destination_location: Optional[Location]
    status: TripStatus
    fare: Optional[Decimal]
    distance_km: Optional[float]
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class Invoice:
    id: Optional[int]
    trip_id: int
    amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    issued_at: Optional[datetime] = None