#  IMPORT LIBRARIES

from sqlalchemy import create_engine            # Creates database connection engine
from sqlalchemy.orm import sessionmaker, declarative_base  # ORM tools for sessions and models
# SQLite database URL
DATABASE_URL = "sqlite:///data/app.db"


#  CREATE DATABASE ENGINE 
engine = create_engine(
    DATABASE_URL,
    
    # Required for SQLite to allow multi-thread access (FastAPI uses async/multi-threading)
    connect_args={"check_same_thread": False}
)
# SessionLocal is used to create new database sessions
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()