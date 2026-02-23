from flask import Blueprint, request, jsonify
from src.backend.agents.conversational_agent import run_agent
import logging
import uuid

# KAN-471: Integrate the NLP module into the backend request flow.
# The agent encapsulates this entire flow.

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/chat', methods=['POST'])
def chat():
    """
    Main endpoint for interacting with the conversational agent.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    message = data.get('message')
    conversation_id = data.get('conversation_id')
    # In a real app, you'd load message history from a DB based on conversation_id
    message_history = data.get('messages', []) 

    try:
        response = run_agent(conversation_id, message, message_history)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error during agent execution: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred."}), 500

@api_blueprint.route('/feedback', methods=['POST'])
def feedback():
    """
    Endpoint to receive user feedback on insights.
    KAN-489: Implement a mechanism for user feedback.
    """
    data = request.get_json()
    if not data or 'rating' not in data:
        return jsonify({"error": "Missing 'rating' in request body"}), 400
    
    insight_id = data.get('insight_id', str(uuid.uuid4())) # A unique ID for the insight/response
    rating = data.get('rating')
    comment = data.get('comment', '')

    # In a real application, this data would be stored in a database.
    logging.info(f"Received feedback for insight {insight_id}: Rating={rating}, Comment='{comment}'")

    return jsonify({"message": "Gracias por tu feedback"}), 200
