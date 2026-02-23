from src.backend.services import nlp_service

# KAN-469, KAN-470: Unit tests for NLP intent and entity extraction.

def test_extract_intent_sales_query():
    """Test for identifying a sales query intent."""
    text = "what were our total sales last month?"
    result = nlp_service.extract_intent_and_entities(text)
    assert result['intent'] == 'query_sales'

def test_extract_intent_and_entities_top_products():
    """Test for top products intent with a limit entity."""
    text = "show me the top 10 best-selling products"
    result = nlp_service.extract_intent_and_entities(text)
    assert result['intent'] == 'query_top_products'
    assert result['entities']['limit'] == 10

def test_extract_intent_and_entities_customer_segment():
    """Test for customer segmentation intent with multiple entities."""
    text = "find customers from germany who spent more than 5000"
    result = nlp_service.extract_intent_and_entities(text)
    assert result['intent'] == 'query_customer_segment'
    assert result['entities']['country'] == 'Germany'
    assert result['entities']['amount_gt'] == 5000

def test_extract_intent_visualize():
    """Test for visualization intent with chart type."""
    text = "can you plot a bar chart of revenue by region"
    result = nlp_service.extract_intent_and_entities(text)
    assert result['intent'] == 'visualize_data'
    assert result['entities']['chart_type'] == 'bar'

def test_extract_intent_greeting():
    """Test for a simple greeting."""
    text = "hey there"
    result = nlp_service.extract_intent_and_entities(text)
    assert result['intent'] == 'greeting'
