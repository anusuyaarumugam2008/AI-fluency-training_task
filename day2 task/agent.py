import json

from config import client, MODEL
from tools import (
    TOOLS,
    get_soil_moisture,
    get_weather,
    get_crop_information,
    calculator,
)


def run_tool(name, arguments):
    if name == "get_soil_moisture":
        return get_soil_moisture()

    if name == "get_weather":
        return get_weather()

    if name == "get_crop_information":
        return get_crop_information()

    if name == "calculator":
        return {
            "result": calculator(arguments["expression"])
        }

    return {"error": f"Unknown tool: {name}"}


def react_agent(question):
    messages = [
        {
            "role": "system",
            "content": """
You are a Smart Agriculture ReAct assistant.

For questions requiring farm information, use the available tools.
Think about what information is needed, take an appropriate action
using a tool, observe the result, and then provide a final answer.

Do not invent sensor or weather values.
Explain the important observations and give practical advice.
""",
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    print("\nUSER QUESTION:")
    print(question)

    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        # No more tools needed
        if not message.tool_calls:
            print("\nFINAL ANSWER:")
            print(message.content)
            return

        # Add assistant tool-call message
        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments or "{}"
            )

            print("\nACTION:")
            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")

            result = run_tool(tool_name, arguments)

            print("OBSERVATION:")
            print(result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    print("\nAgent stopped after maximum steps.")


if __name__ == "__main__":

    print("=" * 70)
    print("SMART AGRICULTURE ASSISTANT - ReAct AGENT")
    print("=" * 70)

    question = """
The tomato crop is at flowering stage.
Should I irrigate now?
Check the current soil moisture and weather conditions before
giving your recommendation.
"""

    react_agent(question)