from config import client, MODEL, QUESTIONS


def direct_prompt(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Smart Agriculture Assistant. "
                    "Give practical, clear advice to farmers. "
                    "Use the provided farm information when relevant."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content


print("=" * 60)
print("SMART AGRICULTURE ASSISTANT - DIRECT PROMPTING")
print("=" * 60)

for i, question in enumerate(QUESTIONS, start=1):
    print(f"\nQUESTION {i}")
    print("-" * 60)
    print(question)

    answer = direct_prompt(question)

    print("\nANSWER:")
    print(answer)