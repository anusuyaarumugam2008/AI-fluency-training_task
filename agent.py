import json

from config import client, MODEL
from tools import TOOLS, execute_tool


SYSTEM_PROMPT = """
You are a Smart Agriculture AI Agent.

You have access to private farm data through tools.

Rules:
1. Never guess private farm values.
2. Always use get_farm_data when the user asks about farm data.
3. Use safe_calculate when arithmetic is required.
4. For irrigation decisions, check soil moisture and rain probability.
5. Give a clear final answer after using the required tools.
6. If no tool is required, answer normally.
"""


def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    tool_trace = []

    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # If no tool is required
        if not message.tool_calls:
            return message.content, tool_trace

        # Add assistant message
        messages.append(message)

        # Execute tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_trace.append({
                "tool": tool_name,
                "arguments": arguments
            })

            result = execute_tool(
                tool_name,
                arguments
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Agent reached the maximum number of steps.", tool_trace


if __name__ == "__main__":

    questions = [
        "What is the current soil moisture of the tomato field?",
        "Should I irrigate the tomato crop today?",
        "What is the temperature of the farm?",
        "Give me a two-line message encouraging farmers to use smart irrigation."
    ]

    print("=" * 60)
    print("SMART AGRICULTURE AI AGENT")
    print("=" * 60)

    for i, question in enumerate(questions, 1):

        print(f"\nQ{i}: {question}")

        answer, trace = run_agent(question)

        print("Answer:", answer)

        print("\nTool Trace:")

        if trace:
            for item in trace:
                print(
                    f"- {item['tool']} "
                    f"{item['arguments']}"
                )
        else:
            print("- No tools used")