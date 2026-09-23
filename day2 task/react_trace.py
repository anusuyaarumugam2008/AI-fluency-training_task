from agent import react_agent


print("=" * 70)
print("SMART AGRICULTURE - ReAct TRACE")
print("=" * 70)

question = """
The tomato crop is at the flowering stage.
The farmer wants to know whether irrigation should be considered now.

Use the available agriculture tools to check:
1. Soil moisture
2. Weather conditions

Then explain what the observations mean and give practical guidance.
"""

react_agent(question)