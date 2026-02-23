import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from functools import wraps
import time
from src.backend import config

# KAN-465: Implement a centralized logging system for queries and application events.

def setup_logging():
    """
    Configures the centralized logging system.
    Logs to both console and a rotating file.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File Handler
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(config.LOG_LEVEL)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(config.LOG_LEVEL)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.LOG_LEVEL)
    
    # Clear existing handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging system initialized.")

def log_db_query(func):
    """
    A decorator to log the execution time of database queries.
    It also checks if the query duration exceeds a predefined threshold and logs a warning.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1] # Assuming the query is the second argument
        params = args[2] if len(args) > 2 else ()
        
        start_time = time.time()
        logging.info(f"Executing query: {query} with params: {params}")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            log_message = f"Query executed successfully. Duration: {duration:.4f} seconds."
            
            # KAN-465: Alert if query exceeds threshold
            if duration > config.QUERY_TIME_ALERT_THRESHOLD_SECONDS:
                logging.warning(f"LONG RUNNING QUERY: {log_message} (Threshold: {config.QUERY_TIME_ALERT_THRESHOLD_SECONDS}s)")
            else:
                logging.info(log_message)
            
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logging.error(f"Query failed after {duration:.4f} seconds. Query: {query}, Params: {params}, Error: {e}", exc_info=True)
            # KAN-475: Do not expose sensitive error details to the user.
            # The error is logged here, and a generic message will be returned by the calling function.
            raise
    return wrapper
