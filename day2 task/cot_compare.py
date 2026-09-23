from config import client, MODEL


QUESTIONS = [
    "An irrigation system delivers 20 litres of water per minute. "
    "If it runs for 45 minutes, how many litres of water are delivered?",

    "A tomato farm has soil moisture of 30% and an irrigation threshold "
    "of 35%. Rain probability is 70% and expected rainfall is 12 mm. "
    "What factors should the farmer consider before irrigating?",

    "Tomato plants are at the flowering stage and some leaves are yellow. "
    "What are possible causes and what should the farmer check first?"
]


def ask_model(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Smart Agriculture Assistant. "
                    "Give practical and clear answers to farmers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def direct_prompt(question):
    prompt = f"""
Answer the following question directly and concisely.

Question:
{question}
"""

    return ask_model(prompt)


def cot_prompt(question):
    prompt = f"""
Solve the following question carefully.

Use a concise numbered reasoning process:

1. Identify the important information.
2. Apply the relevant calculation or agricultural reasoning.
3. State the final answer clearly.

Question:
{question}
"""

    return ask_model(prompt)


print("=" * 70)
print("SMART AGRICULTURE")
print("DIRECT PROMPTING vs CHAIN-OF-THOUGHT")
print("=" * 70)


for i, question in enumerate(QUESTIONS, start=1):

    print(f"\n\nQUESTION {i}")
    print("-" * 70)
    print(question)

    print("\nDIRECT PROMPTING")
    print("-" * 70)

    direct_answer = direct_prompt(question)
    print(direct_answer)

    print("\nCHAIN-OF-THOUGHT STYLE")
    print("-" * 70)

    cot_answer = cot_prompt(question)
    print(cot_answer)

    print("\n" + "=" * 70)