"""
Week 5 - Day 4: observing how the agent plans and executes a multi-step task.

Reuses the Day 3 graph as-is (no code changes to the agent itself) - the only
difference is graph.stream() instead of graph.invoke(), which yields output
after every node runs instead of only the final result. That's what makes
each planning/execution step visible instead of just the end answer.
"""

import uuid
from day3_langgraph import graph, validate_idea_input, final_text
from langchain_core.messages import HumanMessage

COMPLEX_TASK = (
    "I have three ideas I want you to check and record if they don't already "
    "exist in the database: 1) a subscription box for eco-friendly cleaning "
    "products, 2) an app connecting local farmers directly with restaurants, "
    "3) a smart mailbox that alerts you when packages arrive. For each one, "
    "search first, and only save it if it is genuinely new."
)


def run_with_trace(text: str, thread_id: str):
    error = validate_idea_input(text)
    if error:
        print(f"[REJECTED by validation] {error}")
        return

    config = {"configurable": {"thread_id": thread_id}}
    step = 0

    for update in graph.stream({"messages": [HumanMessage(content=text)]}, config=config):
        for node_name, node_output in update.items():
            step += 1
            print(f"\n--- Step {step}: node '{node_name}' ---")
            for message in node_output["messages"]:
                if getattr(message, "tool_calls", None):
                    for call in message.tool_calls:
                        print(f"  PLAN: call {call['name']}(args={call['args']})")
                elif message.__class__.__name__ == "ToolMessage":
                    print(f"  RESULT: {message.content}")
                else:
                    text_content = final_text(message)
                    if text_content:
                        print(f"  FINAL ANSWER: {text_content}")


if __name__ == "__main__":
    print("Enter a multi-part task (e.g. \"check these 3 ideas: ...\"), or press Enter to use the default example.\n")
    user_task = input("Task: ").strip()
    run_with_trace(user_task or COMPLEX_TASK, f"planning-{uuid.uuid4().hex[:8]}")
