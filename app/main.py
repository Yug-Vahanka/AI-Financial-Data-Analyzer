import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

# SQLite / SQLAlchemy imports
from app.core.database import Base, engine
from app.models import db_models  # Importing models ensures Base knows about the tables

# Route imports
from app.routes import extract, records

# APP INITIALIZATION
app = FastAPI(
    title="Financial Data Extraction Service",
    description="AI-powered financial extraction with CSV + Metrics + SQLite storage",
    version="2.0.0"
)

# CORS SETUP 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Automatically create storage directories if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# This line creates the app.db file and all tables defined in db_models.py
Base.metadata.create_all(bind=engine)



app.include_router(extract.router)
app.include_router(records.router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# HEALTH CHECK 
@app.get("/", tags=["System"])
def health_check():
    return {
        "status": "API is running",
        "storage": {
            "csv": "enabled",
            "metrics": "enabled",
            "database": "SQLite connected"
        },
        "endpoints": {
            "extract": "/extract (POST)",
            "records": "/records (GET)",
            "docs": "/docs"
        }
    }