from typing import TypedDict, List, Optional
import uuid

# KAN-477: Implement state management for the conversation.

class GraphState(TypedDict):
    """
    Represents the state of our conversation graph.
    """
    conversation_id: str
    
    # The history of messages in the conversation
    messages: List[tuple[str, str]] # List of (role, content) tuples

    # The structured output from the NLP service
    intent: dict

    # The result from a tool call (e.g., SQL query result)
    tool_result: Optional[dict]
    
    # The final response to be sent to the user
    final_response: Optional[dict]
