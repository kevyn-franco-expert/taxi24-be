# Taxi24 API

A REST API for taxi service management built with FastAPI and Clean Architecture principles.

## Features

### Driver Management
- Get all drivers
- Get available drivers
- Get available drivers within 3km radius of a location
- Get specific driver by ID

### Passenger Management
- Get all passengers
- Get specific passenger by ID
- Get 3 closest drivers for a passenger's pickup location

### Trip Management
- Create trip requests (automatically assigns closest available driver)
- Complete trips
- Get all active trips

### Invoice Management
- Generate invoices for completed trips (with 18% tax)

## Architecture

This project follows Clean Architecture principles with clear separation of concerns:

```
app/
├── domain/           # Business entities and repository interfaces
├── application/      # Use cases and business logic
├── infrastructure/   # Database implementation and external services
└── presentation/     # API endpoints and request/response models
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Database & Sample Data

The application automatically handles database setup and sample data loading:

- **Database Creation**: SQLite database (`taxi24.db`) is created automatically on first run
- **Sample Data Loading**: Sample data is loaded automatically when the application starts
- **No Manual Setup Required**: Everything is configured to work out of the box

#### Sample Data Includes:
- **5 Drivers** with different statuses and locations in Lima, Peru:
  - Carlos Rodriguez (Available) - Downtown Lima
  - Maria Gonzalez (Available) - San Isidro
  - Juan Perez (Available) - Miraflores
  - Ana Torres (Busy) - Barranco
  - Luis Martinez (Offline) - Callao

- **4 Passengers** ready for testing:
  - Pedro Silva, Sofia Vargas, Miguel Castro, Carmen Lopez

#### Manual Sample Data Loading (Optional):
If you need to reload sample data manually:
```bash
python -m app.infrastructure.seed_data
```

#### Database Reset (Optional):
To start with a fresh database:
```bash
rm taxi24.db
python main.py
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Postman Collection

A complete Postman collection is provided in [`Taxi24_API.postman_collection.json`](Taxi24_API.postman_collection.json) with:

- **All API endpoints** with example requests
- **Environment variables** for easy configuration
- **Complete workflow example** showing the full trip lifecycle
- **Pre-configured test data** using the sample data

### How to use the Postman collection:

1. Import `Taxi24_API.postman_collection.json` into Postman
2. The collection includes a `base_url` variable set to `http://localhost:8000`
3. Start with the "Complete Workflow Example" folder to see the full trip process
4. All endpoints are organized by resource (Drivers, Passengers, Trips, Invoices)

## Testing

Run tests with:
```bash
pytest tests/
```

## Database

Uses SQLite database (`taxi24.db`) for simplicity. The database schema includes:
- Drivers (with location and status)
- Passengers
- Trips (with pickup/destination locations)
- Invoices (with tax calculations)

## Business Logic

- Trip requests automatically assign the closest available driver within 3km
- Drivers become "busy" when assigned to a trip
- Drivers return to "available" status when trips are completed
- Invoices include 18% tax calculation
- Distance calculations use the Haversine formula