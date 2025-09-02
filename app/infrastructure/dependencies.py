"""
FastAPI dependency injection for services.
This module provides dependency injection functions for FastAPI endpoints.
"""

from ..application.services import DriverService, PassengerService, TripService, InvoiceService
from .repositories import SQLDriverRepository, SQLPassengerRepository, SQLTripRepository, SQLInvoiceRepository
from .database import SessionLocal


def get_driver_service() -> DriverService:
    """Get driver service with injected dependencies."""
    db = SessionLocal()
    try:
        driver_repo = SQLDriverRepository(db)
        return DriverService(driver_repo)
    finally:
        db.close()


def get_passenger_service() -> PassengerService:
    """Get passenger service with injected dependencies."""
    db = SessionLocal()
    try:
        passenger_repo = SQLPassengerRepository(db)
        driver_repo = SQLDriverRepository(db)
        return PassengerService(passenger_repo, driver_repo)
    finally:
        db.close()


def get_trip_service() -> TripService:
    """Get trip service with injected dependencies."""
    db = SessionLocal()
    try:
        trip_repo = SQLTripRepository(db)
        driver_repo = SQLDriverRepository(db)
        passenger_repo = SQLPassengerRepository(db)
        return TripService(trip_repo, driver_repo, passenger_repo)
    finally:
        db.close()


def get_invoice_service() -> InvoiceService:
    """Get invoice service with injected dependencies."""
    db = SessionLocal()
    try:
        invoice_repo = SQLInvoiceRepository(db)
        trip_repo = SQLTripRepository(db)
        return InvoiceService(invoice_repo, trip_repo)
    finally:
        db.close()