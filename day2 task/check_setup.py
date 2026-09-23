"""
Check the Groq API connection.
"""

from config import client, MODEL, PROVIDER


print("=" * 60)
print("SMART AGRICULTURE ASSISTANT - SETUP CHECK")
print("=" * 60)

print("Provider :", PROVIDER)
print("Model    :", MODEL)

print("\nCalling Groq...")

try:

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": (
                    "Reply with exactly these two words: "
                    "SETUP OK"
                )
            }
        ],

        temperature=0,

        max_tokens=50
    )

    answer = response.choices[0].message.content.strip()

    print("\nModel replied:")
    print(answer)

    print("\nSetup check completed successfully.")

except Exception as error:

    print("\nERROR:")
    print(error)