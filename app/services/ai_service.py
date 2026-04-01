# IMPORT LIBRARIES

import json
from tenacity import retry, stop_after_attempt, wait_fixed
from google import genai

from app.core.config import GEMINI_API_KEY
from app.utils.logger import logger


# INITIALIZE AI CLIENT

client = genai.Client(api_key=GEMINI_API_KEY)


# AI CALL FUNCTION WITH TENACITY RETRY

@retry(
    stop=stop_after_attempt(3),   # Retry 3 times
    wait=wait_fixed(1),           # Wait 1 second between retries
    reraise=True                  # Raise error after all retries fail
)
async def call_gemini_with_retry(prompt: str):
    """
    Calls Gemini AI with automatic retry using Tenacity.

    Steps:
    1. Send prompt to AI
    2. Clean response
    3. Convert to JSON
    4. Retry automatically if error occurs
    """

    try:
        logger.info("Calling Gemini AI...")

        # CALL GEMINI
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # CLEAN RESPONSE
        raw_json = response.text.strip().replace("```json", "").replace("```", "")

        # PARSE JSON
        result = json.loads(raw_json)

        logger.info("Gemini response parsed successfully")

        return result

    except Exception as e:
        # Log retry attempt
        logger.warning(f"Gemini call failed, retrying... Error: {str(e)}")

        # Raise error so Tenacity retries
        raise e