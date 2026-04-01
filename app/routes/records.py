from fastapi import APIRouter, Depends, HTTPException
from app.utils.logger import logger

# SECURITY
from app.core.security import get_auth

# DATABASE
from app.core.database import SessionLocal
from app.models.db_models import FinancialData

# Initialize router
router = APIRouter()


@router.get("/records", tags=["Data"])
async def get_records(token: str = Depends(get_auth)):
    """
    Fetch all stored financial records from SQLite database.

    Returns:
        List of financial records
    """

    logger.info("/records API called")

    db = SessionLocal()

    try:
        # Fetch records
        records = db.query(FinancialData).all()

        # Log success
        logger.info(f"Fetched {len(records)} records successfully")

        return records

    except Exception as e:
        # Log error
        logger.error(f"Error fetching records: {str(e)}")

        # Return proper error response
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching records"
        )

    finally:
        # Always close DB
        db.close()