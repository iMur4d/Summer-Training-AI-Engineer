import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from supabase import create_client, Client

load_dotenv()

# --- Data layer: Supabase client (demo project, "ideas" table) ---
supabase_url = os.environ["DEMO_SUPABASE_URL"]
supabase_key = os.environ["DEMO_SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)


# --- Tool definition ---
# @tool reads this function's type hints (for the parameter schema) and
# its docstring (for the description) to build the schema the LLM sees.
# The docstring is instructions to the model, not documentation for you -
# word it as "when should I call this."
@tool
def search_similar_ideas(query: str) -> str:
    """Search the ideas database for existing ideas similar to the given query.
    Use this whenever the user describes a new idea, to check whether
    something similar already exists before treating it as novel."""
    response = (
        supabase.table("ideas")
        .select("idea_text")
        .ilike("idea_text", f"%{query}%")
        .execute()
    )
    rows = response.data
    if not rows:
        return f"No similar ideas found for '{query}'."
    lines = [f"- {row['idea_text']}" for row in rows]
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


if __name__ == "__main__":
    question = "I have an idea for a recycling rewards app - has something like this been tried before?"
    answer = run_agent(question)
    print("\nFinal answer:\n", answer)
