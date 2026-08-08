import os
import sqlite3
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# --- Data layer: local SQLite file ---
# Swapped from Supabase for Week 5: same table shape, but no network, auth,
# or row-level-security config to fight - keeps focus on agent mechanics,
# which don't depend on what's behind the tool.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ideas.db")


def get_connection() -> sqlite3.Connection:
    """A fresh connection per call - sqlite3 connections aren't safe to share
    across threads, and LangGraph's ToolNode can run tools concurrently."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        (count,) = conn.execute("SELECT COUNT(*) FROM ideas").fetchone()
        if count == 0:
            conn.executemany(
                "INSERT INTO ideas (idea_text) VALUES (?)",
                [
                    ("Build a mobile app that connects local farmers directly with restaurants",),
                    ("Create a subscription box for recycled office supplies",),
                    ("A community recycling rewards program using QR codes",),
                    ("An app that matches volunteers with local nonprofits",),
                ],
            )


init_db()


# Common words that would match almost every row if searched on their own -
# excluding them keeps word-level matching meaningful instead of matching everything.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "for", "and", "or", "to",
    "of", "in", "on", "with", "that", "this", "does", "exist", "something",
    "like", "has", "have", "been", "app", "idea",
}


# --- Tool definition ---
# @tool reads this function's type hints (for the parameter schema) and
# its docstring (for the description) to build the schema the LLM sees.
# The docstring is instructions to the model, not documentation for you -
# word it as "when should I call this."
@tool
def search_similar_ideas(query: str) -> str:
    """Search the ideas database for existing ideas similar to the given query.
    Use this whenever the user describes a new idea, to check whether
    something already exists before treating it as novel."""
    # Word-level matching instead of one exact-phrase substring: a row matches
    # if it contains ANY meaningful word from the query, closer to how a
    # person would search a database than requiring the whole phrase verbatim.
    words = [w for w in query.lower().split() if w not in STOPWORDS and len(w) > 2]
    if not words:
        return f"No similar ideas found for '{query}'."

    where_clause = " OR ".join(["idea_text LIKE ?"] * len(words))
    params = [f"%{word}%" for word in words]

    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT idea_text FROM ideas WHERE {where_clause}",
            params,
        ).fetchall()
    if not rows:
        return f"No similar ideas found for '{query}'."
    lines = [f"- {row[0]}" for row in rows]
    return f"Found {len(rows)} similar idea(s):\n" + "\n".join(lines)


# All tools available to the agent live in this list.
# Adding a second tool later (Week 3) is just: write it, append it here.
tools = [search_similar_ideas]
tools_by_name = {t.name: t for t in tools}

# --- LLM setup ---
# bind_tools() attaches the tool schemas to every request this model makes,
# so the model can choose to emit a tool call instead of a plain reply.
llm = ChatGoogleGenerativeAI(
    model=os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite"),
    api_key=os.environ["GEMINI_API_KEY"],
)
llm_with_tools = llm.bind_tools(tools)


def run_agent(user_input: str) -> str:
    """
    One full turn of the tool-calling loop:
      1. Send the user's message to the LLM (tool schemas are attached via bind_tools).
      2. Check whether the LLM's response requested a tool call.
      3. If so, run the real Python function locally and feed the result back
         as a ToolMessage.
      4. Ask the LLM again - now it has the tool's answer and can respond for real.
      5. If no tool was requested, the first response is already the final answer.
    """
    messages = [
        SystemMessage(content=(
            "You are an assistant that helps analyze submitted ideas. "
            "You have access to a tool, search_similar_ideas, that queries an "
            "internal database of previously submitted ideas. Whenever the user "
            "describes an idea or asks whether something similar has been tried "
            "before, you MUST call search_similar_ideas first with a short keyword "
            "query before answering. Do not answer from general knowledge alone - "
            "always check the internal database first."
        )),
        HumanMessage(content=user_input),
    ]

    ai_message = llm_with_tools.invoke(messages)
    messages.append(ai_message)

    # This is step 1 of "how do I verify the tool was actually called":
    # tool_calls is empty unless the model explicitly requested one.
    if ai_message.tool_calls:
        for call in ai_message.tool_calls:
            print(f"[tool call requested] {call['name']}(args={call['args']})")

            tool_fn = tools_by_name[call["name"]]
            result = tool_fn.invoke(call["args"])

            print(f"[tool result] {result}")

            # ToolMessage links the result back to the specific call via tool_call_id,
            # so the LLM knows which of its requests this answers.
            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))

        final_response = llm_with_tools.invoke(messages)
        return final_response.content

    return ai_message.content


def final_text(content) -> str:
    """
    Gemini's thinking-enabled models return content as a list of blocks
    ({'type': 'thinking', ...}, {'type': 'text', ...}) instead of a plain
    string. Pull out just the visible answer.
    """
    if isinstance(content, str):
        return content
    return "\n".join(block["text"] for block in content if block.get("type") == "text")


if __name__ == "__main__":
    question = input("Enter your idea or question: ")
    answer = run_agent(question)
    print("\nFinal answer:\n", final_text(answer))
