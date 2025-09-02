from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..domain.entities import Driver, Passenger, Trip, Invoice, Location, DriverStatus, TripStatus
from ..domain.repositories import DriverRepository, PassengerRepository, TripRepository, InvoiceRepository
from ..domain.services import find_drivers_within_radius
from .models import DriverModel, PassengerModel, TripModel, InvoiceModel, DriverStatusEnum, TripStatusEnum


class SQLDriverRepository(DriverRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: DriverModel) -> Driver:
        location = None
        if model.latitude and model.longitude:
            location = Location(latitude=model.latitude, longitude=model.longitude)
        
        return Driver(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            license_number=model.license_number,
            status=DriverStatus(model.status.value),
            current_location=location,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def get_all(self) -> List[Driver]:
        models = self.db.query(DriverModel).all()
        return [self._to_entity(model) for model in models]
    
    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        model = self.db.query(DriverModel).filter(DriverModel.id == driver_id).first()
        return self._to_entity(model) if model else None
    
    def get_available(self) -> List[Driver]:
        models = self.db.query(DriverModel).filter(
            DriverModel.status == DriverStatusEnum.AVAILABLE
        ).all()
        return [self._to_entity(model) for model in models]
    
    def get_available_within_radius(self, location: Location, radius_km: float) -> List[Driver]:
        available_drivers = self.get_available()
        return find_drivers_within_radius(available_drivers, location, radius_km)
    
    def create(self, driver: Driver) -> Driver:
        model = DriverModel(
            name=driver.name,
            email=driver.email,
            phone=driver.phone,
            license_number=driver.license_number,
            status=DriverStatusEnum(driver.status.value),
            latitude=driver.current_location.latitude if driver.current_location else None,
            longitude=driver.current_location.longitude if driver.current_location else None
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)
    
    def update(self, driver: Driver) -> Driver:
        model = self.db.query(DriverModel).filter(DriverModel.id == driver.id).first()
        if model:
            model.name = driver.name
            model.email = driver.email
            model.phone = driver.phone
            model.license_number = driver.license_number
            model.status = DriverStatusEnum(driver.status.value)
            if driver.current_location:
                model.latitude = driver.current_location.latitude
                model.longitude = driver.current_location.longitude
            self.db.commit()
            self.db.refresh(model)
            return self._to_entity(model)
        return driver


class SQLPassengerRepository(PassengerRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: PassengerModel) -> Passenger:
        return Passenger(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def get_all(self) -> List[Passenger]:
        models = self.db.query(PassengerModel).all()
        return [self._to_entity(model) for model in models]
    
    def get_by_id(self, passenger_id: int) -> Optional[Passenger]:
        model = self.db.query(PassengerModel).filter(PassengerModel.id == passenger_id).first()
        return self._to_entity(model) if model else None
    
    def create(self, passenger: Passenger) -> Passenger:
        model = PassengerModel(
            name=passenger.name,
            email=passenger.email,
            phone=passenger.phone
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)


class SQLTripRepository(TripRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: TripModel) -> Trip:
        pickup_location = Location(latitude=model.pickup_latitude, longitude=model.pickup_longitude)
        destination_location = None
        if model.destination_latitude and model.destination_longitude:
            destination_location = Location(
                latitude=model.destination_latitude, 
                longitude=model.destination_longitude
            )
        
        return Trip(
            id=model.id,
            passenger_id=model.passenger_id,
            driver_id=model.driver_id,
            pickup_location=pickup_location,
            destination_location=destination_location,
            status=TripStatus(model.status.value),
            fare=model.fare,
            distance_km=model.distance_km,
            created_at=model.created_at,
            completed_at=model.completed_at
        )
    
    def get_all_active(self) -> List[Trip]:
        models = self.db.query(TripModel).filter(
            TripModel.status.in_([TripStatusEnum.REQUESTED, TripStatusEnum.IN_PROGRESS])
        ).all()
        return [self._to_entity(model) for model in models]
    
    def get_by_id(self, trip_id: int) -> Optional[Trip]:
        model = self.db.query(TripModel).filter(TripModel.id == trip_id).first()
        return self._to_entity(model) if model else None
    
    def create(self, trip: Trip) -> Trip:
        model = TripModel(
            passenger_id=trip.passenger_id,
            driver_id=trip.driver_id,
            pickup_latitude=trip.pickup_location.latitude,
            pickup_longitude=trip.pickup_location.longitude,
            destination_latitude=trip.destination_location.latitude if trip.destination_location else None,
            destination_longitude=trip.destination_location.longitude if trip.destination_location else None,
            status=TripStatusEnum(trip.status.value),
            fare=trip.fare,
            distance_km=trip.distance_km
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)
    
    def update(self, trip: Trip) -> Trip:
        model = self.db.query(TripModel).filter(TripModel.id == trip.id).first()
        if model:
            model.driver_id = trip.driver_id
            model.status = TripStatusEnum(trip.status.value)
            model.fare = trip.fare
            model.distance_km = trip.distance_km
            model.completed_at = trip.completed_at
            if trip.destination_location:
                model.destination_latitude = trip.destination_location.latitude
                model.destination_longitude = trip.destination_location.longitude
            self.db.commit()
            self.db.refresh(model)
            return self._to_entity(model)
        return trip


class SQLInvoiceRepository(InvoiceRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: InvoiceModel) -> Invoice:
        return Invoice(
            id=model.id,
            trip_id=model.trip_id,
            amount=model.amount,
            tax_amount=model.tax_amount,
            total_amount=model.total_amount,
            issued_at=model.issued_at
        )
    
    def get_by_trip_id(self, trip_id: int) -> Optional[Invoice]:
        model = self.db.query(InvoiceModel).filter(InvoiceModel.trip_id == trip_id).first()
        return self._to_entity(model) if model else None
    
    def create(self, invoice: Invoice) -> Invoice:
        model = InvoiceModel(
            trip_id=invoice.trip_id,
            amount=invoice.amount,
            tax_amount=invoice.tax_amount,
            total_amount=invoice.total_amount
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)