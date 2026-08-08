"""
Week 5 - Day 3: the Day 2 manual tool-calling loop, rebuilt as a LangGraph
StateGraph with thread-based memory via a checkpointer.

Same LLM, same tool (imported from main.py, not rewritten) - what changes is
how the loop is expressed: main.py's `if ai_message.tool_calls:` check
becomes a conditional edge between two graph nodes, and the messages list
you had to manage by hand is now persisted automatically per thread_id.
"""

import os
import uuid
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from main import search_similar_ideas, get_connection  # reuse the Day 2 tool + DB access as-is

load_dotenv()


def validate_idea_input(text: str) -> str | None:
    """
    Deterministic pre-check, NOT a tool - runs before the graph is ever
    invoked. Validation is a hard system constraint, not something the LLM
    should get to opt out of by simply not calling a tool.
    Returns None if valid, or an error message string if invalid.
    """
    if not text or not text.strip():
        return "Idea text cannot be empty."
    if len(text.strip()) < 10:
        return "Idea text is too short - please describe your idea in more detail."
    return None


@tool
def save_knowledge(idea_text: str) -> str:
    """Save a new idea to the internal ideas database, permanently, so future
    searches can find it. Only call this AFTER using search_similar_ideas and
    confirming this idea is not already recorded."""
    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO ideas (idea_text) VALUES (?)", (idea_text,))
        new_id = cursor.lastrowid
    return f"Saved new idea (id={new_id}): {idea_text}"


tools = [search_similar_ideas, save_knowledge]

llm = ChatGoogleGenerativeAI(
    model=os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite"),
    api_key=os.environ["GEMINI_API_KEY"],
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = (
    "You are an assistant that helps analyze submitted ideas. "
    "You have two tools. First, search_similar_ideas queries an internal "
    "database of previously submitted ideas - whenever the user describes an "
    "idea, you MUST call this first with a short keyword query before saying "
    "anything else. Do not answer from general knowledge alone - always check "
    "the internal database first. Second, save_knowledge permanently records "
    "a new idea - call this only after search_similar_ideas confirms the idea "
    "is not already in the database. If a similar idea already exists, do not "
    "save it again; tell the user it already exists instead."
)


def call_model(state: MessagesState):
    """
    Agent node: equivalent to the first llm_with_tools.invoke(...) call in
    main.py's run_agent(). Whatever it returns gets appended to state["messages"]
    automatically (that's what MessagesState's reducer does).
    """
    messages = state["messages"]
    # Prepend the system prompt only once - it shouldn't pile up on every turn
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# --- Graph wiring ---
# ToolNode and tools_condition are LangGraph prebuilts that do exactly what
# main.py's manual "for call in ai_message.tool_calls: ... invoke ... ToolMessage"
# block did by hand - same mechanics, now packaged as a reusable node + router.
builder = StateGraph(MessagesState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)  # -> "tools" or END
builder.add_edge("tools", "agent")

# InMemorySaver checkpoints state after every node, keyed by thread_id -
# this is what replaces manually carrying a `messages` list between calls.
graph = builder.compile(checkpointer=InMemorySaver())


def final_text(message) -> str:
    """
    Gemini's thinking-enabled models return content as a list of blocks
    ({'type': 'thinking', ...}, {'type': 'text', ...}) instead of a plain
    string. Pull out just the visible answer.
    """
    content = message.content
    if isinstance(content, str):
        return content
    return "\n".join(block["text"] for block in content if block.get("type") == "text")


def submit_idea(text: str, thread_id: str):
    """Runs validation before the graph even sees the input - a bad idea
    never reaches the LLM or costs an API call."""
    error = validate_idea_input(text)
    if error:
        print(f"[REJECTED by validation] {error}")
        return

    result = graph.invoke(
        {"messages": [HumanMessage(content=text)]},
        config={"configurable": {"thread_id": thread_id}},
    )
    print("Agent:", final_text(result["messages"][-1]))


if __name__ == "__main__":
    # One thread_id for the whole session - every message you type here
    # shares memory via the checkpointer. Restart the script to get a fresh
    # thread_id and confirm memory does NOT carry over from a previous run.
    thread_id = f"session-{uuid.uuid4().hex[:8]}"
    print(f"Conversation thread: {thread_id}")
    print("Type your idea, ask about it later, type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        submit_idea(user_input, thread_id)
        print()
