import time
import logging
import json
import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.utils.logger import logger

# MODELS
from app.models.schemas import UserInput, ExtractedData

# SERVICES
from app.services.ai_service import call_gemini_with_retry

# UTILITIES
from app.utils.csv_handler import write_to_csv

# SECURITY
from app.core.security import get_auth

# CONFIG
from app.core.config import DATA_FILE, METRICS_FILE

# DATABASE
from app.core.database import SessionLocal
from app.models.db_models import FinancialData

router = APIRouter()
request_count = 0


def clean_ai_data(data: dict):
    if not data:
        return {}

    mapping = {
        "property_value": "asset_value",
        "house_price": "asset_value",
        "asset_price": "asset_value",
        "savings": "user_savings",
        "interest_rate": "loan_interest_rate",
        "loan_rate": "loan_interest_rate",
        "loan_term_years": "loan_tenure_years",
        "tenure": "loan_tenure_years",
        "loan_amount": None,
    }

    for old_key, new_key in mapping.items():
        if old_key in data:
            value = data.pop(old_key)
            if new_key and new_key not in data:
                data[new_key] = value

    if not data.get("asset_type"):
        data["asset_type"] = "property"

    try:
        val = float(data.get("down_payment_percentage", 0))
        data["down_payment_percentage"] = int(val * 100) if 0 < val <= 1 else int(val)
    except:
        data["down_payment_percentage"] = 0

    for field in ["asset_value", "user_savings", "loan_tenure_years", "monthly_emi_capability"]:
        if field in data:
            try:
                data[field] = int(data[field])
            except:
                pass

    try:
        ir = float(data.get("loan_interest_rate", 0))
        data["loan_interest_rate"] = ir * 100 if 0 < ir <= 1 else ir
    except:
        pass

    if not data.get("investment_preference"):
        data["investment_preference"] = "moderate"

    return data


@router.post("/extract", response_model=ExtractedData)
async def extract_data(payload: UserInput, token: str = Depends(get_auth)):
    global request_count
    request_count += 1
    start_time = time.time()
    success = False

    #  USE request_id FROM PYDANTIC
    request_id = payload.request_id

    logger.info(f"/extract API called | Request number: {request_count} | Request ID: {request_id}")

    schema_instructions = ExtractedData.model_json_schema()

    prompt = f"""
    Extract financial data from the text into STRICT JSON.
    Use these exact keys: {list(schema_instructions['properties'].keys())}
    
    Rules:
    - asset_value and user_savings must be integers.
    - loan_interest_rate must be a float (e.g., 8.5).
    - down_payment_percentage must be an integer (0-100).
    
    Text: {payload.user_input}
    Return ONLY valid JSON.
    """

    try:
        data_dict = await call_gemini_with_retry(prompt)

        cleaned_data = clean_ai_data(data_dict)

        validated = ExtractedData(**cleaned_data)

        # SAVE CSV (UNCHANGED)
        await write_to_csv(DATA_FILE, validated.model_dump(), validated.model_dump().keys())

        # SAVE DATABASE (UNCHANGED)
        db = SessionLocal()
        try:
            db.add(FinancialData(**validated.model_dump()))
            db.commit()
        finally:
            db.close()

        # SAVE JSON FILE
        json_dir = "data/json_logs"
        os.makedirs(json_dir, exist_ok=True)

        json_data = {
            "request_id": request_id,
            "request": payload.user_input,
            "response": validated.model_dump(),
            "timestamp": datetime.now().isoformat()
        }

        json_file_path = os.path.join(json_dir, f"{request_id}.json")

        with open(json_file_path, "w") as f:
            json.dump(json_data, f, indent=4)

        success = True
        logger.info(f"Data extracted and saved successfully | Request ID: {request_id}")

        return validated

    except Exception as e:
        logger.error(f"Extraction failed | Request ID: {request_id} | Error: {str(e)}")
        logging.error(f"Extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        execution_time = time.time() - start_time
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "success": int(success),
            "failed": int(not success),
            "total_requests": request_count
        }
        await write_to_csv(METRICS_FILE, metrics, metrics.keys())