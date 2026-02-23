from flask import Flask
from flask_cors import CORS
from src.backend.api.routes import api_blueprint
from src.backend.database import initialize_database
from src.backend.logger import setup_logging
import logging

def create_app():
    """
    Creates and configures the Flask application.
    """
    # KAN-464: Configure base infrastructure and project repository.
    # This script acts as the entry point for the backend application.
    
    # Initialize logging as the first step
    setup_logging()
    
    app = Flask(__name__)
    
    # Enable CORS to allow frontend to communicate with the backend
    CORS(app)

    # Register the API blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        # Initialize the database
        initialize_database()

    @app.route('/')
    def index():
        return "El backend del Agente Conversacional está en funcionamiento."

    logging.info("Aplicación Flask creada y configurada.")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
