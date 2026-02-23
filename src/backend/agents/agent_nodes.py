import logging
from src.backend.agents.graph_state import GraphState
from src.backend.services import nlp_service, sql_generator_service, clv_service, segmentation_service
from src.backend.cache import cache
import json

# This file defines the nodes of our LangGraph agent. Each node is a function
# that takes the current state and returns a dictionary to update the state.

def parse_intent_node(state: GraphState) -> dict:
    """
    Node that calls the NLP service to parse the user's latest message.
    (Corresponds to STORY-04-A, 04-B, 04-C)
    """
    logging.info("Node: parse_intent")
    last_message = state["messages"][-1][1]
    
    # Use the NLP service to get intent and entities
    intent_data = nlp_service.extract_intent_and_entities(last_message)
    
    return {"intent": intent_data}

def execute_tool_node(state: GraphState) -> dict:
    """
    Node that executes a tool based on the parsed intent.
    This acts as a router to different services.
    (Corresponds to STORY-06.3)
    """
    logging.info("Node: execute_tool")
    intent_data = state["intent"]
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", {})
    original_text = intent_data.get("original_text", "")

    # Check cache first
    cache_key = json.dumps(intent_data, sort_keys=True)
    cached_result = cache.get(cache_key)
    if cached_result:
        return {"tool_result": cached_result}

    result = None
    
    if intent in ["query_sales", "query_top_products", "query_customer_segment"]:
        result = sql_generator_service.execute_intent(intent_data)
    
    elif intent == "visualize_data":
        # For visualization, we need both the data and a hint for the chart type
        data = sql_generator_service.execute_intent(intent_data)
        chart_type = entities.get("chart_type", "bar") # Default to bar chart
        result = {"data": data, "chart_type": chart_type}

    elif intent == "query_clv":
        customer_id = entities.get("customer_id")
        if customer_id:
            # KAN-485: Call the CLV calculation service
            clv = clv_service.calculate_basic_clv(customer_id)
            result = {"clv": clv, "customer_id": customer_id}
        else:
            result = {"error": "Please specify a customer ID to calculate CLV."}
    
    # Add more tool calls here based on other intents
    # e.g., segmentation_service calls

    if result:
        cache.set(cache_key, result)

    return {"tool_result": result}

def generate_response_node(state: GraphState) -> dict:
    """
    Node that generates a final, user-facing response based on the tool result.
    (Corresponds to STORY-09.1)
    """
    logging.info("Node: generate_response")
    intent_data = state["intent"]
    tool_result = state.get("tool_result")
    
    response = {}

    if not tool_result or "error" in tool_result:
        response_text = tool_result.get("error", "I'm sorry, I couldn't process that request.")
        response = {"text": response_text}
    
    elif intent_data["intent"] == "greeting":
        response = {"text": "Hello! How can I help you with your customer analytics today?"}

    elif intent_data["intent"] == "query_clv":
        clv = tool_result.get("clv", 0)
        customer_id = tool_result.get("customer_id")
        response_text = f"The calculated Customer Lifetime Value (CLV) for customer {customer_id} is €{clv:,.2f}."
        response = {"text": response_text}

    elif intent_data["intent"] == "visualize_data":
        # KAN-488: Prepare data for visualization
        chart_type = tool_result.get("chart_type", "bar")
        data = tool_result.get("data", [])
        
        if not data:
            response = {"text": "I couldn't find any data to visualize."}
        else:
            # Assuming data is a list of dicts, e.g., [{'country': 'USA', 'total_sales': 1000}]
            labels = [item[list(item.keys())[0]] for item in data]
            values = [item[list(item.keys())[1]] for item in data]
            
            response = {
                "text": f"Here is the {chart_type} chart you requested.",
                "visualization": {
                    "type": chart_type,
                    "data": {
                        "labels": labels,
                        "datasets": [{
                            "label": list(data[0].keys())[1].replace('_', ' ').title(),
                            "data": values,
                        }]
                    }
                }
            }
    
    else:
        # Generic response for other data queries
        # KAN-476: Transform data to natural language insight
        response_text = "Here are the results of your query:\n"
        # A more sophisticated version would analyze the data and generate a summary.
        # For now, we just format the JSON.
        if isinstance(tool_result, list) and len(tool_result) > 0 and 'total_sales' in tool_result[0]:
             response_text = f"The total sales are €{tool_result[0]['total_sales']:,.2f}."
        else:
            response_text += json.dumps(tool_result, indent=2)
        response = {"text": response_text}

    return {"final_response": response}
