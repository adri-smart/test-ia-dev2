# KAN-463: Customer Analysis Conversational Agent

This project is an advanced conversational agent designed for customer analysis, built to fulfill the requirements of Epic KAN-463 and its associated user stories. The agent provides a natural language interface for complex data analysis tasks such as customer segmentation, Customer Lifetime Value (CLV) calculation, and generating business insights.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)

## Features

*   **Conversational Interface**: Interact with your data using natural language. (STORY-11)
*   **Customer Segmentation**: Segment customers based on various criteria. (STORY-07.1, STORY-17)
*   **CLV Calculation**: Calculate basic and projected Customer Lifetime Value. (STORY-08.2, STORY-18)
*   **Dynamic SQL Generation**: Translates natural language into safe, parameterized SQL queries. (STORY-05.2)
*   **Data-to-Insight**: Transforms raw data into human-readable insights. (STORY-09.1)
*   **Dynamic Visualizations**: Generates charts (bar, line, pie) on demand. (STORY-10)
*   **Caching**: Caches frequent queries for faster responses. (STORY-15)
*   **Logging & Monitoring**: Comprehensive logging for all database queries. (STORY-14)
*   **User Feedback**: Mechanism for users to rate the usefulness of insights. (STORY-16)

## Architecture

The application is built on a microservices-inspired backend and a lightweight vanilla JS frontend.

1.  **Frontend**: A single-page application providing the chat interface, visualization rendering (using Chart.js), and feedback forms.
2.  **Backend (Flask)**:
    *   **API Layer**: A Flask server that exposes a `/chat` endpoint.
    *   **Agent (LangGraph)**: The core of the application, orchestrating the conversation flow. It decides which tool or service to call based on the user's input.
    *   **Services**: A collection of modules responsible for specific business logic:
        *   `NLPService`: Parses user intent and extracts entities.
        *   `SQLGeneratorService`: Constructs and validates SQL queries.
        *   `CLVService`: Performs CLV calculations.
        *   `SegmentationService`: Manages customer segmentation logic.
    *   **Database**: An SQLite database for storing customer and transaction data.
    *   **Cache**: A Redis cache to store results of frequent queries.

See the full details in the [Architecture Document](./docs/architecture.md).

## Tech Stack

*   **Backend**: Python, Flask, LangGraph, LangChain, Pandas
*   **Frontend**: HTML, CSS, Vanilla JavaScript, Chart.js
*   **Database**: SQLite
*   **Caching**: Redis
*   **Testing**: Pytest
*   **Infrastructure**: Terraform (IaC)

## Project Structure

```
.
├── data/                     # Sample CSV data
├── docs/                     # Project documentation
├── infra/                    # Terraform infrastructure-as-code
├── src/
│   ├── backend/              # Flask backend application
│   └── frontend/             # HTML/JS/CSS frontend
├── tests/                    # Pytest tests
├── .env.example              # Example environment variables
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the `.env.example` file to `.env` and fill in the required values (like your OpenAI API key).
    ```bash
    cp .env.example .env
    ```

5.  **Initialize the database:**
    The application will automatically create and seed the SQLite database from the CSV files in `/data` on first run.

## Running the Application

1.  **Start the backend server:**
    ```bash
    python -m src.backend.app
    ```
    The server will start on `http://127.0.0.1:5000`.

2.  **Open the frontend:**
    Open the `src/frontend/index.html` file in your web browser. You can now start chatting with the agent.

## Running Tests

To run the test suite, use `pytest`:

```bash
pytest
```

## Environment Variables

The following environment variables are required. See `.env.example`.

*   `OPENAI_API_KEY`: Your API key for the OpenAI service (used as a stand-in for Gemini).
*   `REDIS_HOST`: Host for the Redis cache (defaults to `localhost`).
*   `REDIS_PORT`: Port for the Redis cache (defaults to `6379`).

## API Endpoints

*   `POST /chat`
    *   Handles chat interactions with the agent.
    *   **Request Body**: `{"conversation_id": "...", "message": "..."}`
    *   **Response Body**: `{"response": "...", "visualization": {...}, "conversation_id": "..."}`

*   `POST /feedback`
    *   Submits user feedback on an insight.
    *   **Request Body**: `{"insight_id": "...", "rating": 5, "comment": "..."}`
