from typing import Optional, Dict, Any
from ..domain.entities import Driver, Passenger, Trip, Invoice, Location


class EntityMapper:
    """Mapper class to convert domain entities to dictionaries for presentation layer"""
    
    @staticmethod
    def location_to_dict(location: Optional[Location]) -> Optional[Dict[str, Any]]:
        if not location:
            return None
        return {
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    
    @staticmethod
    def driver_to_dict(driver: Driver) -> Dict[str, Any]:
        return {
            "id": driver.id,
            "name": driver.name,
            "email": driver.email,
            "phone": driver.phone,
            "license_number": driver.license_number,
            "status": driver.status.value,
            "current_location": EntityMapper.location_to_dict(driver.current_location),
            "created_at": driver.created_at,
            "updated_at": driver.updated_at
        }
    
    @staticmethod
    def passenger_to_dict(passenger: Passenger) -> Dict[str, Any]:
        return {
            "id": passenger.id,
            "name": passenger.name,
            "email": passenger.email,
            "phone": passenger.phone,
            "created_at": passenger.created_at,
            "updated_at": passenger.updated_at
        }
    
    @staticmethod
    def trip_to_dict(trip: Trip) -> Dict[str, Any]:
        return {
            "id": trip.id,
            "passenger_id": trip.passenger_id,
            "driver_id": trip.driver_id,
            "pickup_location": EntityMapper.location_to_dict(trip.pickup_location),
            "destination_location": EntityMapper.location_to_dict(trip.destination_location),
            "status": trip.status.value,
            "fare": trip.fare,
            "distance_km": trip.distance_km,
            "created_at": trip.created_at,
            "completed_at": trip.completed_at
        }
    
    @staticmethod
    def invoice_to_dict(invoice: Invoice) -> Dict[str, Any]:
        return {
            "id": invoice.id,
            "trip_id": invoice.trip_id,
            "amount": invoice.amount,
            "tax_amount": invoice.tax_amount,
            "total_amount": invoice.total_amount,
            "issued_at": invoice.issued_at
        }