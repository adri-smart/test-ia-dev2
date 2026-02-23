import pandas as pd
import logging
from src.backend.database import get_db_connection, execute_query

# KAN-480, KAN-481, KAN-482, KAN-483: Implement customer segmentation logic.

def get_customers_who_bought_a_not_b(product_a: str, product_b: str):
    """
    Finds customers who purchased product A but did not purchase product B.
    This directly addresses the use case in KAN-483.
    """
    query = """
        SELECT DISTINCT t1.customer_id
        FROM transactions t1
        WHERE t1.product_id = ?
        AND NOT EXISTS (
            SELECT 1
            FROM transactions t2
            WHERE t2.customer_id = t1.customer_id
            AND t2.product_id = ?
        );
    """
    params = (product_a, product_b)
    
    conn = get_db_connection()
    try:
        results = execute_query(conn, query, params)
        if not results:
            return f"No customers found who bought {product_a} but not {product_b}."
        return results
    finally:
        conn.close()

def get_segment_details(segment_name: str):
    """
    Provides a drill-down view of customers within a specific segment.
    This is a mock for KAN-482. A real implementation would have more complex segment definitions.
    """
    if segment_name.lower() == 'high_value':
        # "High Value" defined as customers who have spent over 1000 in total.
        query = """
            SELECT c.customer_id, c.name, SUM(t.amount) as total_spent
            FROM customers c
            JOIN transactions t ON c.customer_id = t.customer_id
            GROUP BY c.customer_id
            HAVING total_spent > 1000
            ORDER BY total_spent DESC;
        """
        conn = get_db_connection()
        try:
            # KAN-482: The query itself performs the drill-down.
            # The performance criteria (<2s for 1k customers) depends on DB indexing.
            results = execute_query(conn, query)
            return results
        finally:
            conn.close()
    return f"Segment '{segment_name}' is not defined."

def get_segment_metrics(segment_name: str):
    """
    Calculates aggregate metrics for a given segment.
    This is a mock for KAN-481.
    """
    if segment_name.lower() == 'high_value':
        query = """
            WITH HighValueCustomers AS (
                SELECT customer_id
                FROM transactions
                GROUP BY customer_id
                HAVING SUM(amount) > 1000
            )
            SELECT
                COUNT(DISTINCT t.customer_id) as num_customers,
                SUM(t.amount) as total_revenue,
                AVG(t.amount) as average_ticket_size
            FROM transactions t
            WHERE t.customer_id IN (SELECT customer_id FROM HighValueCustomers);
        """
        conn = get_db_connection()
        try:
            # KAN-481: Calculate aggregated metrics
            results = execute_query(conn, query)
            return results[0] if results else {}
        finally:
            conn.close()
    return f"Metrics for segment '{segment_name}' are not defined."
