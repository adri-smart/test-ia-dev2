import re
import logging

# KAN-469, KAN-470: Implement basic NLP to extract intent and entities.
# This is a simplified mock implementation. In a real-world scenario,
# this would use LangChain with a powerful LLM like Gemini or GPT.

def extract_intent_and_entities(text: str) -> dict:
    """
    Parses natural language text to identify a primary intent and key entities.
    Returns a structured dictionary with the findings.
    """
    text = text.lower()
    
    # Intent patterns
    intents = {
        "query_sales": r"total sales|revenue",
        "query_top_products": r"top.*products|best-selling",
        "query_customer_segment": r"customers who|list all customers|find customers",
        "query_clv": r"clv|customer lifetime value",
        "visualize_data": r"chart|plot|graph|visualize",
        "greeting": r"hello|hi|hey",
    }

    # Default intent
    result = {"intent": "unknown", "entities": {}, "original_text": text}

    for intent, pattern in intents.items():
        if re.search(pattern, text):
            result["intent"] = intent
            break

    # Entity extraction
    # This is highly simplified. A real implementation would use a NER model.
    
    # Extract numbers (for limits or amounts)
    numbers = re.findall(r'\d+', text)
    if numbers:
        if "top" in text:
            result["entities"]["limit"] = int(numbers[0])
        elif "more than" in text or "spent over" in text:
            result["entities"]["amount_gt"] = int(numbers[0])

    # Extract countries (example)
    countries = ["germany", "usa", "spain", "china", "japan", "uk"]
    for country in countries:
        if country in text:
            result["entities"]["country"] = country.capitalize()

    # Extract chart types
    chart_types = ["bar", "line", "pie"]
    for chart_type in chart_types:
        if chart_type in text:
            result["entities"]["chart_type"] = chart_type
            break
    
    # Extract customer ID
    customer_id_match = re.search(r'customer (id )?([a-z0-9]+)', text)
    if customer_id_match:
        result["entities"]["customer_id"] = customer_id_match.group(2).upper()

    logging.info(f"NLP processing for '{text}': {result}")
    return result
