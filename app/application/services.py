from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from ..core.config import settings
from ..domain.entities import Driver, Passenger, Trip, Invoice, Location, DriverStatus, TripStatus
from ..domain.repositories import DriverRepository, PassengerRepository, TripRepository, InvoiceRepository
from ..domain.services import calculate_distance, find_closest_drivers


class DriverService:
    def __init__(self, driver_repo: DriverRepository):
        self.driver_repo = driver_repo
    
    def get_all_drivers(self) -> List[Driver]:
        return self.driver_repo.get_all()
    
    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        return self.driver_repo.get_by_id(driver_id)
    
    def get_available_drivers(self) -> List[Driver]:
        return self.driver_repo.get_available()
    
    def get_available_drivers_within_radius(self, location: Location, radius_km: float = None) -> List[Driver]:
        if radius_km is None:
            radius_km = settings.default_search_radius_km
        return self.driver_repo.get_available_within_radius(location, radius_km)


class PassengerService:
    def __init__(self, passenger_repo: PassengerRepository, driver_repo: DriverRepository):
        self.passenger_repo = passenger_repo
        self.driver_repo = driver_repo
    
    def get_all_passengers(self) -> List[Passenger]:
        return self.passenger_repo.get_all()
    
    def get_passenger_by_id(self, passenger_id: int) -> Optional[Passenger]:
        return self.passenger_repo.get_by_id(passenger_id)
    
    def get_closest_drivers_for_passenger(self, passenger_id: int, pickup_location: Location, limit: int = None) -> List[Driver]:
        if limit is None:
            limit = settings.max_nearby_drivers
        available_drivers = self.driver_repo.get_available()
        return find_closest_drivers(available_drivers, pickup_location, limit)


class TripService:
    def __init__(self, trip_repo: TripRepository, driver_repo: DriverRepository, passenger_repo: PassengerRepository):
        self.trip_repo = trip_repo
        self.driver_repo = driver_repo
        self.passenger_repo = passenger_repo
    
    def get_all_active_trips(self) -> List[Trip]:
        return self.trip_repo.get_all_active()
    
    def create_trip_request(self, passenger_id: int, pickup_location: Location, destination_location: Optional[Location] = None) -> Optional[Trip]:
        passenger = self.passenger_repo.get_by_id(passenger_id)
        if not passenger:
            return None
        
        available_drivers = self.driver_repo.get_available_within_radius(pickup_location, settings.default_search_radius_km)
        if not available_drivers:
            return None
        
        closest_drivers = find_closest_drivers(available_drivers, pickup_location, 1)
        if not closest_drivers:
            return None
        closest_driver = closest_drivers[0]
        
        trip = Trip(
            id=None,
            passenger_id=passenger_id,
            driver_id=closest_driver.id,
            pickup_location=pickup_location,
            destination_location=destination_location,
            status=TripStatus.REQUESTED,
            fare=None,
            distance_km=None
        )
        
        created_trip = self.trip_repo.create(trip)
        
        closest_driver.status = DriverStatus.BUSY
        self.driver_repo.update(closest_driver)
        
        return created_trip
    
    def complete_trip(self, trip_id: int, destination_location: Location, fare: Decimal) -> Optional[Trip]:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip or trip.status != TripStatus.REQUESTED:
            return None
        
        distance_km = calculate_distance(
            trip.pickup_location.latitude, trip.pickup_location.longitude,
            destination_location.latitude, destination_location.longitude
        )
        
        trip.destination_location = destination_location
        trip.status = TripStatus.COMPLETED
        trip.fare = fare
        trip.distance_km = distance_km
        trip.completed_at = datetime.utcnow()
        
        updated_trip = self.trip_repo.update(trip)
        
        if trip.driver_id:
            driver = self.driver_repo.get_by_id(trip.driver_id)
            if driver:
                driver.status = DriverStatus.AVAILABLE
                self.driver_repo.update(driver)
        
        return updated_trip


class InvoiceService:
    def __init__(self, invoice_repo: InvoiceRepository, trip_repo: TripRepository):
        self.invoice_repo = invoice_repo
        self.trip_repo = trip_repo
    
    def generate_invoice_for_trip(self, trip_id: int) -> Optional[Invoice]:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip or trip.status != TripStatus.COMPLETED or not trip.fare:
            return None
        
        existing_invoice = self.invoice_repo.get_by_trip_id(trip_id)
        if existing_invoice:
            return existing_invoice
        
        tax_rate = Decimal(str(settings.tax_rate))
        amount = trip.fare
        tax_amount = amount * tax_rate
        total_amount = amount + tax_amount
        
        invoice = Invoice(
            id=None,
            trip_id=trip_id,
            amount=amount,
            tax_amount=tax_amount,
            total_amount=total_amount
        )
        
        return self.invoice_repo.create(invoice)