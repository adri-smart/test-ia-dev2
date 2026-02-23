import logging
from langgraph.graph import StateGraph, END
from src.backend.agents.graph_state import GraphState
from src.backend.agents import agent_nodes
import uuid

# KAN-478: Implement transitions between states in the conversational graph.

def should_execute_tool(state: GraphState) -> str:
    """
    Conditional edge logic. Decides whether to execute a tool or generate a simple response.
    """
    intent = state["intent"].get("intent")
    if intent in ["greeting", "unknown"]:
        # If it's a simple greeting or unknown intent, go straight to generating a response
        return "generate_response"
    else:
        # Otherwise, execute a tool
        return "execute_tool"

def create_agent_graph():
    """
    Builds the LangGraph agent.
    """
    graph = StateGraph(GraphState)

    # Add nodes to the graph
    graph.add_node("parse_intent", agent_nodes.parse_intent_node)
    graph.add_node("execute_tool", agent_nodes.execute_tool_node)
    graph.add_node("generate_response", agent_nodes.generate_response_node)

    # Define the entry point
    graph.set_entry_point("parse_intent")

    # Define the edges (transitions)
    graph.add_conditional_edges(
        "parse_intent",
        should_execute_tool,
        {
            "execute_tool": "execute_tool",
            "generate_response": "generate_response"
        }
    )
    graph.add_edge("execute_tool", "generate_response")
    graph.add_edge("generate_response", END)

    # Compile the graph into a runnable app
    agent = graph.compile()
    logging.info("Conversational agent graph compiled successfully.")
    return agent

# Create a single instance of the agent
conversational_agent = create_agent_graph()

def run_agent(conversation_id: str, message: str, existing_messages: list):
    """
    Runs the conversational agent for a single turn.
    """
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    # Append the new user message to the history
    current_messages = existing_messages + [("user", message)]
    
    # KAN-477: The state is managed by passing it through the graph.
    initial_state = {
        "conversation_id": conversation_id,
        "messages": current_messages,
    }
    
    final_state = conversational_agent.invoke(initial_state)
    
    response_data = final_state.get("final_response", {"text": "I'm sorry, something went wrong."})
    
    # Append the agent's response to the history for the next turn
    response_data["conversation_id"] = conversation_id
    response_data["messages"] = current_messages + [("assistant", response_data.get("text", ""))]

    return response_data
# LangChain/OpenAI Configuration (used as a stand-in for Gemini Enterprise)
# KAN-466: This file helps manage credentials securely without hardcoding them.
OPENAI_API_KEY="your_openai_api_key_here"

# Redis Cache Configuration (KAN-490)
REDIS_HOST=localhost
REDIS_PORT=6379
