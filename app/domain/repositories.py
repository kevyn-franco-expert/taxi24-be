from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Driver, Passenger, Trip, Invoice, Location


class DriverRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Driver]:
        pass
    
    @abstractmethod
    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        pass
    
    @abstractmethod
    def get_available(self) -> List[Driver]:
        pass
    
    @abstractmethod
    def get_available_within_radius(self, location: Location, radius_km: float) -> List[Driver]:
        pass
    
    @abstractmethod
    def create(self, driver: Driver) -> Driver:
        pass
    
    @abstractmethod
    def update(self, driver: Driver) -> Driver:
        pass


class PassengerRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Passenger]:
        pass
    
    @abstractmethod
    def get_by_id(self, passenger_id: int) -> Optional[Passenger]:
        pass
    
    @abstractmethod
    def create(self, passenger: Passenger) -> Passenger:
        pass


class TripRepository(ABC):
    @abstractmethod
    def get_all_active(self) -> List[Trip]:
        pass
    
    @abstractmethod
    def get_by_id(self, trip_id: int) -> Optional[Trip]:
        pass
    
    @abstractmethod
    def create(self, trip: Trip) -> Trip:
        pass
    
    @abstractmethod
    def update(self, trip: Trip) -> Trip:
        pass


class InvoiceRepository(ABC):
    @abstractmethod
    def get_by_trip_id(self, trip_id: int) -> Optional[Invoice]:
        pass
    
    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        pass