"""
Shared configuration for the Smart Agriculture Assistant.

This project uses Groq through its OpenAI-compatible API.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GROQ CONFIGURATION
# =========================================================

PROVIDER = "groq"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL = os.getenv(
    "MODEL",
    "openai/gpt-oss-20b"
)


if not GROQ_API_KEY:

    raise SystemExit(
        "\nERROR: GROQ_API_KEY was not found.\n\n"
        "Create a .env file containing:\n\n"
        "PROVIDER=groq\n"
        "GROQ_API_KEY=your_key_here\n"
        "MODEL=openai/gpt-oss-20b\n"
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = OpenAI(

    api_key=GROQ_API_KEY,

    base_url="https://api.groq.com/openai/v1"
)


# =========================================================
# SIMULATED FARM DATA
# =========================================================

FARM_DATA = {

    "crop": "tomato",

    "growth_stage": "flowering",

    "soil_moisture": 30,

    "soil_moisture_unit": "%",

    "temperature": 31,

    "temperature_unit": "C",

    "humidity": 68,

    "humidity_unit": "%",

    "rain_probability": 70,

    "rain_probability_unit": "%",

    "rainfall_expected": 12,

    "rainfall_unit": "mm",

    "irrigation_threshold": 35,

    "field_area": 1,

    "field_area_unit": "acre"
}


# =========================================================
# QUESTIONS FOR THE EXPERIMENT
# =========================================================

QUESTIONS = [

    (
        "A farmer has 1 acre of tomato plants. "
        "The field contains 30% soil moisture. "
        "The farmer wants to know whether irrigation should "
        "be considered. What factors should be checked "
        "before making the decision?"
    ),

    (
        "A farmer has 1 acre of tomato plants. "
        "An irrigation system delivers 20 litres per minute. "
        "If the farmer operates it for 45 minutes, "
        "how many litres of water are delivered?"
    ),

    (
        "Tomato plants are showing yellow leaves. "
        "What are some possible causes, and what should "
        "the farmer check first?"
    ),

    (
        "The farm has 30% soil moisture and rain is expected soon. "
        "Should irrigation be considered immediately? "
        "Explain the factors that should be considered."
    )
]


# =========================================================
# DISPLAY HELPER
# =========================================================

def banner(title):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)

    print(
        f"Provider: {PROVIDER} | "
        f"Model: {MODEL}"
    )

    print("=" * 80)