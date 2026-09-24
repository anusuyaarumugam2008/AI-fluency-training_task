from config import client, MODEL, QUESTIONS


def ask_chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful general agriculture assistant. "
                    "Answer the user's question clearly. "
                    "You do not have access to any private farm database."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("=" * 60)
    print("PLAIN CHATBOT")
    print("=" * 60)

    for i, question in enumerate(QUESTIONS, 1):

        print(f"\nQ{i}: {question}")

        answer = ask_chatbot(question)

        print("Answer:", answer)