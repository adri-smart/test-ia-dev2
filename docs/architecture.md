# KAN-496: System Architecture

This document provides a detailed overview of the technical architecture for the Customer Analysis Conversational Agent.

## 1. Guiding Principles

*   **Modularity**: Components are designed to be independent and reusable.
*   **Scalability**: The architecture should support growth in data volume and user load.
*   **Maintainability**: Code is clean, well-documented, and easy to understand.
*   **Security**: Security is a primary concern, especially in handling data and external API access.

## 2. System Components

The system is composed of a frontend client, a backend application, a database, and a caching layer.



### 2.1. Frontend

*   **Description**: A lightweight, single-page web application that serves as the user interface.
*   **Technology**: HTML, CSS, Vanilla JavaScript.
*   **Responsibilities**:
    *   Rendering the chat interface (KAN-487).
    *   Sending user messages to the backend API.
    *   Displaying agent responses, including text and visualizations.
    *   Rendering dynamic charts using **Chart.js** (KAN-488).
    *   Providing a user feedback mechanism (stars and comments) (KAN-489).

### 2.2. Backend

*   **Description**: A Python-based server that orchestrates the entire conversational flow and business logic.
*   **Technology**: Flask, LangGraph, LangChain, Pandas.
*   **Components**:
    *   **API Server (Flask)**: Exposes RESTful endpoints (`/chat`, `/feedback`) for the frontend. It handles incoming HTTP requests and manages user sessions.
    *   **Conversational Agent (LangGraph)**: This is the brain of the system. It's a stateful graph that manages the conversation flow (KAN-477). It routes user input to the appropriate tool or service based on its current state and the user's intent (KAN-478, KAN-479).
    *   **Services**: A collection of specialized Python modules:
        *   **NLP Service**: Parses natural language to identify intent and extract entities (e.g., dates, product names) (KAN-470).
        *   **SQL Generator Service**: Securely constructs parameterized SQL queries from the NLP output. It validates queries against a schema whitelist to prevent SQL injection (KAN-472, KAN-475).
        *   **Data Analysis Services (CLV, Segmentation)**: Contain the business logic for calculating metrics like Customer Lifetime Value (KAN-485) and performing customer segmentation (KAN-480).
        *   **Insight Generation Service**: Transforms numerical data from query results into natural language descriptions and actionable recommendations (KAN-476).
    *   **External API Integration**: A secure connector to communicate with Large Language Models (e.g., Gemini Enterprise or OpenAI) for advanced NLP tasks (KAN-466).

### 2.3. Database

*   **Description**: A relational database that stores all customer and transactional data.
*   **Technology**: SQLite (for simplicity in this POC). Can be easily swapped for PostgreSQL or other production-grade databases.
*   **Responsibilities**:
    *   Storing customer profiles, transaction history, and product information.
    *   Executing SQL queries sent by the backend.
    *   The connection is configured securely via environment variables (KAN-467).

### 2.4. Cache

*   **Description**: An in-memory data store used to cache the results of frequent or computationally expensive queries.
*   **Technology**: Redis.
*   **Responsibilities**:
    *   Storing responses to common questions to reduce latency (KAN-490).
    *   Reducing load on the database and external APIs.
    *   Implementing a configurable Time-to-Live (TTL) for cache entries.

## 3. Data and Control Flow

1.  A user types a message into the **Frontend** chat and clicks "Send".
2.  The frontend sends a POST request to the backend's `/chat` endpoint.
3.  The **Flask API Server** receives the request and passes it to the **Conversational Agent (LangGraph)**.
4.  The agent's **NLP Service** node processes the text to determine intent and entities.
5.  Based on the intent, the agent transitions to another node. For a data query, this is the **SQL Generator Service**.
6.  The SQL Generator creates a safe, parameterized SQL query and executes it against the **Database**.
7.  The query results are passed to the **Data Analysis Service** (e.g., CLV) or the **Insight Generation Service**.
8.  The service processes the data and generates a final response, which may include text, a data payload for a chart, or both.
9.  The agent returns this structured response to the API server.
10. The API server forwards the response to the **Frontend**.
11. The frontend displays the text response and, if visualization data is present, renders a chart using Chart.js.
