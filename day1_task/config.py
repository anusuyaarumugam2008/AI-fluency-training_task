import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to .env")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Private farm data
FARM_DATA = {
    "crop": "Tomato",
    "soil_moisture": 28,
    "temperature": 32,
    "soil_ph": 6.5,
    "rain_probability": 10,
    "water_tank": 60
}

QUESTIONS = [
    "What is the current soil moisture of the tomato field?",
    "Should I irrigate the tomato crop today?",
    "The soil moisture is 28% and rain probability is 10%. How much water should I provide if the recommended amount is 20 litres?",
    "Give me a two-line message encouraging farmers to use smart irrigation."
]