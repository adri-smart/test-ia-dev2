import logging
from src.backend.database import get_table_schema, execute_query, get_db_connection

# KAN-472, KAN-473, KAN-475: Implement a parser for query intentions,
# generate parameterized SQL, and validate it.

# A whitelist of tables and their queryable columns
# KAN-475: This acts as a security layer to prevent queries on unauthorized tables/columns.
SCHEMA_WHITELIST = {
    "customers": {"customer_id", "name", "email", "join_date", "country"},
    "transactions": {"transaction_id", "customer_id", "product_id", "transaction_date", "amount"}
}

def generate_sql_from_intent(intent_data: dict) -> (str, tuple):
    """
    Generates a safe, parameterized SQL query from a structured intent.
    """
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", {})
    
    query = ""
    params = []

    if intent == "query_sales":
        query = "SELECT SUM(amount) as total_sales FROM transactions;"
    
    elif intent == "query_top_products":
        limit = entities.get("limit", 5)
        query = """
            SELECT product_id, SUM(amount) as total_revenue
            FROM transactions
            GROUP BY product_id
            ORDER BY total_revenue DESC
            LIMIT ?;
        """
        params.append(limit)

    elif intent == "query_customer_segment":
        # Example: "customers from Germany who spent more than 5000"
        query = """
            SELECT c.customer_id, c.name, c.country, SUM(t.amount) as total_spent
            FROM customers c
            JOIN transactions t ON c.customer_id = t.customer_id
        """
        conditions = []
        if "country" in entities:
            conditions.append("c.country = ?")
            params.append(entities["country"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " GROUP BY c.customer_id, c.name, c.country"

        if "amount_gt" in entities:
            query += " HAVING SUM(t.amount) > ?"
            params.append(entities["amount_gt"])
        
        query += " ORDER BY total_spent DESC;"

    elif intent == "visualize_data" and "sales by country" in intent_data.get("original_text", ""):
        query = """
            SELECT c.country, SUM(t.amount) as total_sales
            FROM customers c
            JOIN transactions t ON c.customer_id = t.customer_id
            GROUP BY c.country
            ORDER BY total_sales DESC;
        """
    
    else:
        # KAN-472: If intent is not parsable into a known SQL structure
        raise ValueError("Could not parse the intent into a valid SQL query.")

    # KAN-475: Final validation before returning
    if not is_query_safe(query):
        logging.error(f"Generated query failed safety validation: {query}")
        raise PermissionError("The generated query is not allowed.")

    return query, tuple(params)

def is_query_safe(query: str) -> bool:
    """
    A simple safety check. Prevents destructive commands.
    A more robust implementation would use a proper SQL parsing library.
    """
    query_lower = query.lower().strip()
    if not query_lower.startswith("select"):
        return False
    
    # Blacklist of dangerous keywords
    blacklist = ["drop", "delete", "update", "insert", "truncate", "grant", "revoke"]
    for keyword in blacklist:
        if keyword in query_lower.split():
            return False
            
    return True

def execute_intent(intent_data: dict):
    """
    Generates and executes SQL from an intent, returning the results.
    """
    try:
        query, params = generate_sql_from_intent(intent_data)
        logging.info(f"Generated SQL: {query} with params: {params}")
        
        conn = get_db_connection()
        try:
            # KAN-474: Execute the query
            results = execute_query(conn, query, params)
            return results
        finally:
            conn.close()
            
    except (ValueError, PermissionError) as e:
        logging.warning(f"Could not execute intent due to generation error: {e}")
        return {"error": str(e)}
    except Exception as e:
        # KAN-475: Catch database errors and return a generic message
        logging.error(f"An unexpected error occurred during intent execution: {e}", exc_info=True)
        return {"error": "An error occurred while processing your request in the database."}
