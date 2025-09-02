from fastapi import FastAPI
from app.core.config import settings
from app.presentation.api import router
from app.infrastructure.database import create_tables
from app.infrastructure.seed_data import create_sample_data

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    create_tables()
    create_sample_data()

@app.get("/")
def read_root():
    return {"message": "Welcome to Taxi24 API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)