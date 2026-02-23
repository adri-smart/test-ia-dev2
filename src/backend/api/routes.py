from flask import Blueprint, request, jsonify
from src.backend.agents.conversational_agent import run_agent
from src.backend.database import get_db_connection, execute_query
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
        return jsonify({"error": "Falta el campo 'message' en el cuerpo de la solicitud"}), 400

    message = data.get('message')
    conversation_id = data.get('conversation_id')
    # In a real app, you'd load message history from a DB based on conversation_id
    message_history = data.get('messages', []) 

    try:
        response = run_agent(conversation_id, message, message_history)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error durante la ejecución del agente: {e}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno."}), 500

@api_blueprint.route('/feedback', methods=['POST'])
def feedback():
    """
    Endpoint to receive user feedback on insights.
    KAN-489: Implement a mechanism for user feedback.
    """
    data = request.get_json()
    if not data or 'rating' not in data:
        return jsonify({"error": "Falta el campo 'rating' en el cuerpo de la solicitud"}), 400
    if 'insight_id' not in data:
        return jsonify({"error": "Falta el campo 'insight_id' en el cuerpo de la solicitud"}), 400

    # KAN-489: Almacenar feedback en la base de datos
    feedback_id = str(uuid.uuid4())
    insight_id = data.get('insight_id')
    conversation_id = data.get('conversation_id') # KAN-477: Para mantener contexto
    rating = data.get('rating')
    comment = data.get('comment', '')

    logging.info(f"Recibido feedback para insight {insight_id}: Rating={rating}, Comment='{comment}'")

    conn = None
    try:
        conn = get_db_connection()
        query = """
            INSERT INTO feedback (feedback_id, insight_id, conversation_id, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (feedback_id, insight_id, conversation_id, rating, comment)
        execute_query(conn, query, params)
        
        return jsonify({"message": "Gracias por tu feedback"}), 200
    except Exception as e:
        logging.error(f"Error al guardar feedback: {e}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno al procesar tu feedback."}), 500
    finally:
        if conn:
            conn.close()
