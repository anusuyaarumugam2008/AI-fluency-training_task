import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")

if PROVIDER == "groq":
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")


def banner(text):
    print("=" * 50)
    print(text)
    print("=" * 50)