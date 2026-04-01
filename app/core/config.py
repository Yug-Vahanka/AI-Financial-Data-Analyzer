# IMPORT LIBRARIES 
import os                          # Used to access environment variables
from dotenv import load_dotenv    # Used to load variables from .env file
#LOAD ENV FILE 
load_dotenv()
# Fetch Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Fetch Bearer token for API authentication
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
# Path where extracted financial data will be stored (CSV file)
DATA_FILE = "data/financial_data.csv"
# Path where API performance metrics will be stored (CSV file)
METRICS_FILE = "data/metrics.csv"
# Path where application logs will be stored
LOG_FILE = "logs/backend.log"