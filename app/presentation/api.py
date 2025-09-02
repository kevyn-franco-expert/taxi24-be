from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..domain.entities import Location
from ..application.services import DriverService, PassengerService, TripService, InvoiceService
from ..infrastructure.mappers import EntityMapper
from ..infrastructure.dependencies import get_driver_service, get_passenger_service, get_trip_service, get_invoice_service
from .schemas import (
    DriverSchema, PassengerSchema, TripSchema, InvoiceSchema,
    TripRequestSchema, CompleteTripSchema, LocationSchema
)

router = APIRouter()


# Driver Endpoints
@router.get("/drivers", response_model=List[DriverSchema])
def get_all_drivers(service: DriverService = Depends(get_driver_service)):
    drivers = service.get_all_drivers()
    return [DriverSchema(**EntityMapper.driver_to_dict(driver)) for driver in drivers]


@router.get("/drivers/available", response_model=List[DriverSchema])
def get_available_drivers(service: DriverService = Depends(get_driver_service)):
    drivers = service.get_available_drivers()
    return [DriverSchema(**EntityMapper.driver_to_dict(driver)) for driver in drivers]


@router.get("/drivers/available/nearby", response_model=List[DriverSchema])
def get_available_drivers_nearby(
    latitude: float,
    longitude: float,
    radius: float = None,
    service: DriverService = Depends(get_driver_service)
):
    location = Location(latitude=latitude, longitude=longitude)
    drivers = service.get_available_drivers_within_radius(location, radius)
    return [DriverSchema(**EntityMapper.driver_to_dict(driver)) for driver in drivers]


@router.get("/drivers/{driver_id}", response_model=DriverSchema)
def get_driver_by_id(driver_id: int, service: DriverService = Depends(get_driver_service)):
    driver = service.get_driver_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return DriverSchema(**EntityMapper.driver_to_dict(driver))


# Passenger Endpoints
@router.get("/passengers", response_model=List[PassengerSchema])
def get_all_passengers(service: PassengerService = Depends(get_passenger_service)):
    passengers = service.get_all_passengers()
    return [PassengerSchema(**EntityMapper.passenger_to_dict(passenger)) for passenger in passengers]


@router.get("/passengers/{passenger_id}", response_model=PassengerSchema)
def get_passenger_by_id(passenger_id: int, service: PassengerService = Depends(get_passenger_service)):
    passenger = service.get_passenger_by_id(passenger_id)
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return PassengerSchema(**EntityMapper.passenger_to_dict(passenger))


@router.post("/passengers/{passenger_id}/nearby-drivers", response_model=List[DriverSchema])
def get_nearby_drivers_for_passenger(
    passenger_id: int,
    request: LocationSchema,
    service: PassengerService = Depends(get_passenger_service)
):
    location = Location(latitude=request.latitude, longitude=request.longitude)
    drivers = service.get_closest_drivers_for_passenger(passenger_id, location)
    return [DriverSchema(**EntityMapper.driver_to_dict(driver)) for driver in drivers]


# Trip Endpoints
@router.get("/trips/active", response_model=List[TripSchema])
def get_active_trips(service: TripService = Depends(get_trip_service)):
    trips = service.get_all_active_trips()
    return [TripSchema(**EntityMapper.trip_to_dict(trip)) for trip in trips]


@router.post("/trips", response_model=TripSchema)
def create_trip(request: TripRequestSchema, service: TripService = Depends(get_trip_service)):
    pickup_location = Location(
        latitude=request.pickup_location.latitude,
        longitude=request.pickup_location.longitude
    )
    destination_location = None
    if request.destination_location:
        destination_location = Location(
            latitude=request.destination_location.latitude,
            longitude=request.destination_location.longitude
        )
    
    trip = service.create_trip_request(
        passenger_id=request.passenger_id,
        pickup_location=pickup_location,
        destination_location=destination_location
    )
    
    if not trip:
        raise HTTPException(status_code=400, detail="Unable to create trip. No available drivers or passenger not found.")
    
    return TripSchema(**EntityMapper.trip_to_dict(trip))


@router.put("/trips/{trip_id}/complete", response_model=TripSchema)
def complete_trip(
    trip_id: int,
    request: CompleteTripSchema,
    service: TripService = Depends(get_trip_service)
):
    destination_location = Location(
        latitude=request.destination_location.latitude,
        longitude=request.destination_location.longitude
    )
    
    trip = service.complete_trip(trip_id, destination_location, request.fare)
    if not trip:
        raise HTTPException(status_code=400, detail="Unable to complete trip. Trip not found or not in correct status.")
    
    return TripSchema(**EntityMapper.trip_to_dict(trip))


# Invoice Endpoints
@router.post("/trips/{trip_id}/invoice", response_model=InvoiceSchema)
def generate_invoice(trip_id: int, service: InvoiceService = Depends(get_invoice_service)):
    invoice = service.generate_invoice_for_trip(trip_id)
    if not invoice:
        raise HTTPException(status_code=400, detail="Unable to generate invoice. Trip not completed or invoice already exists.")
    
    return InvoiceSchema(**EntityMapper.invoice_to_dict(invoice))