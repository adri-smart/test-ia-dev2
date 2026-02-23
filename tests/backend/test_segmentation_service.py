import pytest
from unittest.mock import patch
from src.backend.services import segmentation_service

# KAN-483: QA Cases for customer segmentation use case.

@patch('src.backend.services.segmentation_service.execute_query')
def test_get_customers_who_bought_a_not_b(mock_execute_query):
    """
    Tests the scenario for finding customers who bought product A but not B.
    """
    # Mock the database response
    mock_execute_query.return_value = [{'customer_id': 'C001'}, {'customer_id': 'C005'}]
    
    result = segmentation_service.get_customers_who_bought_a_not_b('P01', 'P02')
    
    # Assert that the correct query was constructed
    expected_query = """
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
    mock_execute_query.assert_called_with(pytest.anything(), expected_query.strip(), ('P01', 'P02'))
    
    # Assert that the result is correct
    customer_ids = [res['customer_id'] for res in result]
    assert 'C001' in customer_ids
    assert 'C005' in customer_ids

@patch('src.backend.services.segmentation_service.execute_query')
def test_get_customers_who_bought_a_not_b_no_results(mock_execute_query):
    """
    Tests the scenario where no customers match the criteria.
    """
    mock_execute_query.return_value = []
    
    result = segmentation_service.get_customers_who_bought_a_not_b('P03', 'P04')
    
    assert "No customers found" in result
