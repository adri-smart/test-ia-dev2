import os
from dotenv import load_dotenv

# KAN-466: Load credentials and configurations securely from environment variables
load_dotenv()

# --- LLM Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Cache Configuration (KAN-490) ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = 3600  # 1 hour TTL for cache entries

# --- Database Configuration (KAN-467) ---
DB_PATH = "data/analytics.db"
CUSTOMER_DATA_PATH = "data/customers.csv"
TRANSACTION_DATA_PATH = "data/transactions.csv"

# --- Logging Configuration (KAN-465) ---
LOG_FILE = "logs/app.log"
LOG_LEVEL = "INFO"
LOG_ROTATION = "10 MB"
LOG_RETENTION = "30 days"

# --- Performance Thresholds (KAN-465) ---
QUERY_TIME_ALERT_THRESHOLD_SECONDS = 2.0
