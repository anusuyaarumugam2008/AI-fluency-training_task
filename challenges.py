from agent import run_agent
from workflow import workflow


QUESTION = """
I can use only 25 litres of water today.
Should I irrigate the tomato crop, and what should I do
based on the current farm conditions?
"""


print("=" * 60)
print("CHALLENGE QUESTION")
print("=" * 60)

print("\nQuestion:")
print(QUESTION)

print("\n--- RULE-BASED WORKFLOW ---")

workflow_answer = workflow(QUESTION)

print(workflow_answer)

print("\n--- AI AGENT ---")

agent_answer, trace = run_agent(QUESTION)

print(agent_answer)

print("\nTool Trace:")

for item in trace:
    print(
        f"- {item['tool']} "
        f"{item['arguments']}"
    )