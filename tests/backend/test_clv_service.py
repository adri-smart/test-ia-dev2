import pytest
from unittest.mock import patch
from src.backend.services import clv_service

# KAN-485: QA Cases for CLV calculation

@pytest.fixture
def mock_transactions():
    """Fixture to provide sample transaction data."""
    return [
        {'amount': 100, 'transaction_date': '2022-01-01'},
        {'amount': 150, 'transaction_date': '2022-07-01'},
        {'amount': 120, 'transaction_date': '2023-01-01'},
    ]

@patch('src.backend.services.clv_service.execute_query')
def test_calculate_basic_clv_happy_path(mock_execute_query, mock_transactions):
    """
    1. Verificación del Cálculo Correcto y Rendimiento (Happy Path)
    """
    mock_execute_query.return_value = mock_transactions
    
    clv = clv_service.calculate_basic_clv('C001')
    
    # Manual calculation:
    # Avg Purchase Value = (100 + 150 + 120) / 3 = 123.33
    # Lifespan = 365 days = 1 year
    # Purchase Frequency = 3 purchases / 1 year = 3
    # Customer Lifetime = 1 year
    # CLV = 123.33 * 3 * 1 = 370
    # The function returns sum for single year, which is 370
    assert clv == pytest.approx(370.0)

@patch('src.backend.services.clv_service.execute_query')
def test_calculate_clv_for_customer_with_no_transactions(mock_execute_query):
    """
    4. Verificación de Cliente Sin Transacciones
    """
    mock_execute_query.return_value = []
    
    clv = clv_service.calculate_basic_clv('C999')
    
    assert clv == 0.0

@patch('src.backend.services.clv_service.execute_query')
def test_calculate_clv_for_single_transaction(mock_execute_query):
    """
    Test case for a customer with only one transaction.
    """
    mock_execute_query.return_value = [{'amount': 50, 'transaction_date': '2023-01-01'}]
    
    clv = clv_service.calculate_basic_clv('C002')
    
    # For a single transaction, our logic defaults to returning the total amount spent.
    assert clv == 50.0

def test_project_clv_for_segment():
    """
    Tests for KAN-486: Probar Caso de Uso: Proyección de Valor de Vida del Cliente
    """
    # Test case for 'Premium' segment
    premium_result = clv_service.project_clv_for_segment('Premium')
    assert premium_result['total'] == 1200
    assert len(premium_result['projection']) == 12

    # Test case for 'Estándar' segment
    standard_result = clv_service.project_clv_for_segment('Estándar')
    assert standard_result['total'] == 600
    assert len(standard_result['projection']) == 12

    # Test case for segment with insufficient data
    insufficient_data_result = clv_service.project_clv_for_segment('New')
    assert 'error' in insufficient_data_result
    assert insufficient_data_result['error'] == 'Datos insuficientes para la proyección'
