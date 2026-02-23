import sqlite3
import pandas as pd
import os
import logging
from src.backend import config
from src.backend.logger import log_db_query

# KAN-467: Configure and manage the database connection.

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"La conexión a la base de datos falló: {e}", exc_info=True)
        raise

def initialize_database():
    """
    Initializes the database by creating tables and seeding them with data from CSV files.
    This function is idempotent and will not re-insert data if the tables are not empty.
    """
    db_conn = get_db_connection()
    try:
        # Check if tables are already populated
        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        if cursor.fetchone() is not None:
            cursor.execute("SELECT COUNT(*) FROM customers")
            if cursor.fetchone()[0] > 0:
                logging.info("La base de datos ya ha sido inicializada y poblada.")
                return

        logging.info("Base de datos no encontrada o vacía. Inicializando nueva base de datos...")
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                join_date TEXT,
                country TEXT
            )
        ''')
        logging.info("Tabla 'customers' creada o ya existe.")

        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                customer_id TEXT,
                product_id TEXT,
                transaction_date TEXT,
                amount REAL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        logging.info("Tabla 'transactions' creada o ya existe.")

        # KAN-489: Tabla para feedback de usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id TEXT PRIMARY KEY,
                insight_id TEXT NOT NULL,
                conversation_id TEXT,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        logging.info("Tabla 'feedback' creada o ya existe.")

        # KAN-484: Prepare and validate historical data
        # Load data from CSV and insert into tables
        customers_df = pd.read_csv(config.CUSTOMER_DATA_PATH)
        # Simple validation: drop duplicates and nulls
        customers_df.drop_duplicates(subset=['customer_id'], inplace=True)
        customers_df.dropna(inplace=True)
        customers_df.to_sql('customers', db_conn, if_exists='append', index=False)
        logging.info(f"Se cargaron {len(customers_df)} registros en la tabla 'customers'.")

        transactions_df = pd.read_csv(config.TRANSACTION_DATA_PATH)
        # Simple validation
        transactions_df.drop_duplicates(subset=['transaction_id'], inplace=True)
        transactions_df.dropna(inplace=True)
        transactions_df.to_sql('transactions', db_conn, if_exists='append', index=False)
        logging.info(f"Se cargaron {len(transactions_df)} registros en la tabla 'transactions'.")

        db_conn.commit()
        logging.info("Base de datos inicializada y poblada exitosamente.")
    except Exception as e:
        db_conn.rollback()
        logging.error(f"La inicialización de la base de datos falló: {e}", exc_info=True)
    finally:
        db_conn.close()


@log_db_query
def execute_query(conn, query, params=()):
    """
    Executes a given SQL query with parameters in a safe manner.
    KAN-474: Execute and validate results of SQL queries.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        # For SELECT queries, fetch and return results
        if query.strip().upper().startswith("SELECT"):
            results = [dict(row) for row in cursor.fetchall()]
            return results
        # For INSERT, UPDATE, DELETE, commit and return affected rows
        else:
            conn.commit()
            return {"affected_rows": cursor.rowcount}
    except sqlite3.Error as e:
        # KAN-475: The decorator will log the detailed error. Here we re-raise
        # to be handled by the service layer, which will return a generic message.
        logging.error(f"Error al ejecutar la consulta: {e}")
        raise Exception("La ejecución de la consulta a la base de datos falló.")

def get_table_schema(table_name):
    """
    Retrieves the schema (column names) for a given table.
    Used for query validation.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = {row['name'] for row in cursor.fetchall()}
        return schema
    finally:
        conn.close()
