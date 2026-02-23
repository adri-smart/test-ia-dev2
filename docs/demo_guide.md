# KAN-496: POC Demonstration Guide

This guide provides a step-by-step script for demonstrating the key functionalities of the Customer Analysis Conversational Agent to stakeholders.

### Objective
To showcase the agent's ability to understand natural language, perform complex data analysis, generate insights, and present them in an intuitive way.

### Prerequisites
1.  The application is running locally (backend and frontend).
2.  The `index.html` file is open in a browser.
3.  The chat interface is visible and ready for input.

---

### Demo Script

#### Part 1: Introduction & Simple Interaction (Greeting)

*   **Spoken Narrative**: "Welcome. This is a demonstration of our new conversational agent for customer analytics. You can interact with it using plain English, just like you're talking to a human analyst. Let's start with a simple greeting."
*   **Action**: Type `Hello` into the chat and press Enter.
*   **Expected Result**: The agent responds with a friendly greeting (e.g., "Hello! How can I help you with your customer data today?").
*   **Key Takeaway**: The agent can handle basic conversational turns.

#### Part 2: Basic Data Retrieval (Total Sales)

*   **Spoken Narrative**: "Now, let's ask a straightforward business question. I want to know our total sales revenue."
*   **Action**: Type `What are the total sales?` and press Enter.
*   **Expected Result**: The agent processes the query, runs a SQL query in the background, and responds with a clear, concise answer, like: "The total sales revenue is €XX,XXX.XX."
*   **Key Takeaway**: The agent can translate a natural language question into a database query and return a factual answer.

#### Part 3: Customer Segmentation (Drill-Down)

*   **Spoken Narrative**: "This is useful, but the real power comes from segmentation. Let's find a specific group of customers. I'm interested in our high-value customers from Germany."
*   **Action**: Type `Show me customers from Germany who have spent more than 5000` and press Enter.
*   **Expected Result**: The agent returns a list or a summary of the customers who match these criteria. For example: "Found 3 customers from Germany who spent over €5000: Customer A, Customer B, Customer C."
*   **Key Takeaway**: The agent can handle multi-condition queries and filter data based on complex criteria. This demonstrates STORY-07.1 and STORY-07.3.

#### Part 4: Dynamic Visualization (Sales by Country)

*   **Spoken Narrative**: "A list is good, but a visual is often better. Let's ask the agent to visualize this data. I want to see a breakdown of sales by country."
*   **Action**: Type `Generate a bar chart of sales by country` and press Enter.
*   **Expected Result**: The agent responds with a short message ("Here is the bar chart for sales by country.") and renders a bar chart directly in the chat interface, showing each country and its corresponding sales total.
*   **Key Takeaway**: The agent can generate dynamic visualizations on demand, transforming raw data into easily digestible charts. This demonstrates STORY-10.

#### Part 5: Advanced Analytics (CLV Calculation)

*   **Spoken Narrative**: "Let's move to more advanced predictive analytics. I want to know the Customer Lifetime Value for a specific customer."
*   **Action**: Type `What is the CLV for customer C001?` and press Enter.
*   **Expected Result**: The agent calculates the CLV using its internal model and responds: "The calculated Customer Lifetime Value (CLV) for customer C001 is €XXXX.XX."
*   **Key Takeaway**: The agent has predictive capabilities and can run analytical models like CLV on the fly. This demonstrates STORY-08.2.

#### Part 6: User Feedback Mechanism

*   **Spoken Narrative**: "Finally, to ensure the system improves over time, we've built in a feedback mechanism. If I found that last insight useful, I can rate it."
*   **Action**:
    1.  Hover over the last response from the agent.
    2.  Click on the 5-star rating system that appears. Select 5 stars.
    3.  An optional comment box appears. Type `Very helpful!` and click "Send Feedback".
*   **Expected Result**: A confirmation message appears, such as "Thank you for your feedback!". The feedback is stored in the backend.
*   **Key Takeaway**: The system gathers user feedback to measure the quality of insights and enable future improvements. This demonstrates STORY-16.

#### Part 7: Conclusion

*   **Spoken Narrative**: "As you can see, this agent provides a powerful yet simple interface to unlock deep insights from our customer data. It handles everything from simple lookups to complex segmentations and predictive analytics, all through natural conversation. Thank you."
