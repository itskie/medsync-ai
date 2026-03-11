from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator
from app.core.config import settings

# Import all 6 tools
from app.agent.tools.log_interaction import log_interaction
from app.agent.tools.edit_interaction import edit_interaction
from app.agent.tools.get_hcp_profile import get_hcp_profile
from app.agent.tools.suggest_followup import suggest_followup
from app.agent.tools.analyze_sentiment import analyze_sentiment
from app.agent.tools.search_interactions import search_interactions

# All tools list
tools = [
    log_interaction,
    edit_interaction,
    get_hcp_profile,
    suggest_followup,
    analyze_sentiment,
    search_interactions
]

# Initialize Groq LLM with tools bound
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
).bind_tools(tools)

# Agent state — tracks conversation messages
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_call_count: int

# System prompt
SYSTEM_PROMPT = SystemMessage(content="""You are MedSync AI, an intelligent assistant for pharmaceutical sales representatives.

You help with:
- Logging HCP (doctor/hospital) interactions
- Analyzing HCP profiles  
- Suggesting follow-up actions
- Analyzing sentiment of interactions
- Searching past interactions

Always respond in a helpful, professional, and conversational tone.
If the user asks something unrelated to your tools, still respond helpfully as a general assistant.
Never expose internal function formats or tool instructions to the user.""")

# Agent node — LLM decides what to do next
def agent_node(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": [response],
        "tool_call_count": state.get("tool_call_count", 0)
    }

# Tool node wrapper — increments counter
def tool_node_with_count(state: AgentState):
    tool_node = ToolNode(tools)
    result = tool_node.invoke(state)
    return {
        "messages": result["messages"],
        "tool_call_count": state.get("tool_call_count", 0) + 1
    }

# Router — should we use a tool or stop?
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    tool_call_count = state.get("tool_call_count", 0)

    if tool_call_count >= 3:
        return END

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END

# Build the LangGraph
def create_agent():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node_with_count)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")
    return graph.compile()

# Global agent instance
agent = create_agent()

# Main function to chat with agent
def chat_with_agent(message: str) -> str:
    result = agent.invoke({
        "messages": [SYSTEM_PROMPT, HumanMessage(content=message)],
        "tool_call_count": 0
    })

    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content and msg.content.strip():
            return msg.content

    for msg in reversed(result["messages"]):
        if hasattr(msg, 'content') and msg.content and msg.content.strip():
            try:
                import json
                data = json.loads(msg.content)
                if isinstance(data, dict) and data.get("success"):
                    return json.dumps(data, indent=2)
            except:
                return msg.content

    return "Agent completed the task successfully!"