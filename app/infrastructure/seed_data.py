from sqlalchemy.orm import Session
from .database import SessionLocal, create_tables
from .models import DriverModel, PassengerModel, DriverStatusEnum


def create_sample_data():
    create_tables()
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(DriverModel).first() or db.query(PassengerModel).first():
            return
        
        # Create sample drivers
        drivers = [
            DriverModel(
                name="Carlos Rodriguez",
                email="carlos@taxi24.com",
                phone="+51987654321",
                license_number="LIC001",
                status=DriverStatusEnum.AVAILABLE,
                latitude=-12.0464,
                longitude=-77.0428
            ),
            DriverModel(
                name="Maria Gonzalez",
                email="maria@taxi24.com",
                phone="+51987654322",
                license_number="LIC002",
                status=DriverStatusEnum.AVAILABLE,
                latitude=-12.0500,
                longitude=-77.0450
            ),
            DriverModel(
                name="Juan Perez",
                email="juan@taxi24.com",
                phone="+51987654323",
                license_number="LIC003",
                status=DriverStatusEnum.AVAILABLE,
                latitude=-12.0520,
                longitude=-77.0480
            ),
            DriverModel(
                name="Ana Torres",
                email="ana@taxi24.com",
                phone="+51987654324",
                license_number="LIC004",
                status=DriverStatusEnum.BUSY,
                latitude=-12.0600,
                longitude=-77.0500
            ),
            DriverModel(
                name="Luis Martinez",
                email="luis@taxi24.com",
                phone="+51987654325",
                license_number="LIC005",
                status=DriverStatusEnum.OFFLINE,
                latitude=-12.0700,
                longitude=-77.0600
            )
        ]
        
        # Create sample passengers
        passengers = [
            PassengerModel(
                name="Pedro Silva",
                email="pedro@email.com",
                phone="+51912345678"
            ),
            PassengerModel(
                name="Sofia Vargas",
                email="sofia@email.com",
                phone="+51912345679"
            ),
            PassengerModel(
                name="Miguel Castro",
                email="miguel@email.com",
                phone="+51912345680"
            ),
            PassengerModel(
                name="Carmen Lopez",
                email="carmen@email.com",
                phone="+51912345681"
            )
        ]
        
        # Add to database
        for driver in drivers:
            db.add(driver)
        
        for passenger in passengers:
            db.add(passenger)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()