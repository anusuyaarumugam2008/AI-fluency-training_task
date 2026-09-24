print("CHECK 1: Python is running")

from config import client, MODEL

print("CHECK 2: Config loaded")
print("MODEL:", MODEL)
print("CHECK 3: Connecting to Groq...")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: SETUP OK"
        }
    ],
    temperature=0
)

print("CHECK 4: Response received")
print(response.choices[0].message.content)