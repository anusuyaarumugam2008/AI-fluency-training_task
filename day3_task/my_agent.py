import json

from config import client, MODEL
from my_tools import (
    get_soil_moisture,
    get_weather,
    get_crop_information,
    calculator,
)


SYSTEM_PROMPT = """
You are a Smart Agriculture Assistant.

You help farmers make decisions using available farm information.

Available tools:
1. get_soil_moisture
2. get_weather
3. get_crop_information
4. calculator

Use a tool whenever current farm information or a calculation is required.

Do not invent sensor values.
Explain the result clearly and give practical advice.
"""


tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_soil_moisture",
            "description": "Gets the current simulated soil moisture percentage.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets simulated weather information including rain probability.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_crop_information",
            "description": "Gets crop type, growth stage, and farm information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculates a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    },
]


def run_tool(name, arguments):
    if name == "get_soil_moisture":
        return get_soil_moisture()

    if name == "get_weather":
        return get_weather()

    if name == "get_crop_information":
        return get_crop_information()

    if name == "calculator":
        return calculator(arguments["expression"])

    return "Unknown tool."


def ask_agent(question):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}

            print(f"\n[TOOL CALL] {name}")
            print(f"[ARGUMENTS] {arguments}")

            result = run_tool(name, arguments)

            print(f"[TOOL RESULT] {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )


if __name__ == "__main__":
    print("SMART AGRICULTURE ASSISTANT")
    print("-" * 40)

    question = input("Farmer question: ")

    answer = ask_agent(question)

    print("\nAssistant:")
    print(answer)