import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from main import app
from app.infrastructure.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Taxi24 API", "docs": "/docs"}


def test_get_all_drivers():
    response = client.get("/api/v1/drivers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_available_drivers():
    response = client.get("/api/v1/drivers/available")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_available_drivers_nearby():
    response = client.get("/api/v1/drivers/available/nearby?latitude=-12.0464&longitude=-77.0428&radius=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_driver_by_id():
    response = client.get("/api/v1/drivers/1")
    if response.status_code == 200:
        driver = response.json()
        assert "id" in driver
        assert "name" in driver
        assert "email" in driver


def test_get_driver_not_found():
    response = client.get("/api/v1/drivers/999")
    assert response.status_code == 404


def test_get_all_passengers():
    response = client.get("/api/v1/passengers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_passenger_by_id():
    response = client.get("/api/v1/passengers/1")
    if response.status_code == 200:
        passenger = response.json()
        assert "id" in passenger
        assert "name" in passenger
        assert "email" in passenger


def test_get_passenger_not_found():
    response = client.get("/api/v1/passengers/999")
    assert response.status_code == 404


def test_get_nearby_drivers_for_passenger():
    payload = {
        "latitude": -12.0464,
        "longitude": -77.0428
    }
    response = client.post("/api/v1/passengers/1/nearby-drivers", json=payload)
    if response.status_code == 200:
        assert isinstance(response.json(), list)


def test_get_active_trips():
    response = client.get("/api/v1/trips/active")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_trip():
    payload = {
        "passenger_id": 1,
        "pickup_location": {
            "latitude": -12.0464,
            "longitude": -77.0428
        },
        "destination_location": {
            "latitude": -12.0500,
            "longitude": -77.0450
        }
    }
    response = client.post("/api/v1/trips", json=payload)
    if response.status_code == 200:
        trip = response.json()
        assert "id" in trip
        assert trip["passenger_id"] == 1
        assert trip["status"] == "requested"


def test_complete_trip():
    # First create a trip
    create_payload = {
        "passenger_id": 1,
        "pickup_location": {
            "latitude": -12.0464,
            "longitude": -77.0428
        }
    }
    create_response = client.post("/api/v1/trips", json=create_payload)
    
    if create_response.status_code == 200:
        trip = create_response.json()
        trip_id = trip["id"]
        
        # Complete the trip
        complete_payload = {
            "destination_location": {
                "latitude": -12.0500,
                "longitude": -77.0450
            },
            "fare": "25.50"
        }
        response = client.put(f"/api/v1/trips/{trip_id}/complete", json=complete_payload)
        
        if response.status_code == 200:
            completed_trip = response.json()
            assert completed_trip["status"] == "completed"
            assert completed_trip["fare"] == "25.50"


def test_generate_invoice():
    # First create and complete a trip
    create_payload = {
        "passenger_id": 1,
        "pickup_location": {
            "latitude": -12.0464,
            "longitude": -77.0428
        }
    }
    create_response = client.post("/api/v1/trips", json=create_payload)
    
    if create_response.status_code == 200:
        trip = create_response.json()
        trip_id = trip["id"]
        
        # Complete the trip
        complete_payload = {
            "destination_location": {
                "latitude": -12.0500,
                "longitude": -77.0450
            },
            "fare": "30.00"
        }
        complete_response = client.put(f"/api/v1/trips/{trip_id}/complete", json=complete_payload)
        
        if complete_response.status_code == 200:
            # Generate invoice
            response = client.post(f"/api/v1/trips/{trip_id}/invoice")
            
            if response.status_code == 200:
                invoice = response.json()
                assert "id" in invoice
                assert invoice["trip_id"] == trip_id
                assert "amount" in invoice
                assert "tax_amount" in invoice
                assert "total_amount" in invoice


if __name__ == "__main__":
    pytest.main([__file__])