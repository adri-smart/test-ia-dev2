import pytest
from src.backend.services import sql_generator_service

# KAN-473: QA Cases for SQL generation.

def test_generate_sql_for_total_sales():
    """Test Case 1: Simple total sales query."""
    intent = {"intent": "query_sales", "entities": {}}
    query, params = sql_generator_service.generate_sql_from_intent(intent)
    assert "SELECT SUM(amount) as total_sales FROM transactions;" in query
    assert params == ()

def test_generate_sql_for_top_products():
    """Test Case 2: Top products with a limit."""
    intent = {"intent": "query_top_products", "entities": {"limit": 10}}
    query, params = sql_generator_service.generate_sql_from_intent(intent)
    assert "LIMIT ?" in query
    assert params == (10,)

def test_generate_sql_for_customer_segment():
    """Test Case 3: Complex customer segment query."""
    intent = {
        "intent": "query_customer_segment",
        "entities": {"country": "Germany", "amount_gt": 5000}
    }
    query, params = sql_generator_service.generate_sql_from_intent(intent)
    assert "WHERE c.country = ?" in query
    assert "HAVING SUM(t.amount) > ?" in query
    assert params == ("Germany", 5000)

def test_prevent_unsafe_sql():
    """Test Case 4: Prevention of SQL Injection / unsafe queries."""
    # This should fail the safety check
    with pytest.raises(PermissionError):
        sql_generator_service.is_query_safe("DROP TABLE users;")

    # This should pass
    assert sql_generator_service.is_query_safe("SELECT * FROM users;") == True

    # Malicious intent should still generate a safe, parameterized query
    intent = {
        "intent": "query_customer_segment",
        "entities": {"country": "' OR 1=1; --"}
    }
    query, params = sql_generator_service.generate_sql_from_intent(intent)
    assert params == ("' OR 1=1; --",)
    assert "OR 1=1" not in query # The malicious part should only be in params
