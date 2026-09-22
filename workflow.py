import re
from config import FARM_DATA


def get_course_or_farm_value(question):
    question_lower = question.lower()

    if "soil moisture" in question_lower:
        return f"The current soil moisture is {FARM_DATA['soil_moisture']}%."

    if "temperature" in question_lower:
        return f"The current temperature is {FARM_DATA['temperature']}°C."

    if "ph" in question_lower:
        return f"The current soil pH is {FARM_DATA['soil_ph']}."

    if "rain" in question_lower:
        return (
            f"The current rain probability is "
            f"{FARM_DATA['rain_probability']}%."
        )

    return None


def irrigation_decision(question):
    question_lower = question.lower()

    if "irrigate" in question_lower or "irrigation" in question_lower:

        moisture = FARM_DATA["soil_moisture"]
        rain = FARM_DATA["rain_probability"]

        if moisture < 30 and rain < 30:
            return (
                "YES. Irrigation is recommended because "
                "soil moisture is below 30% and rain probability is low."
            )
        else:
            return "NO. Irrigation is not recommended based on the current rules."

    return None


def water_calculation(question):
    question_lower = question.lower()

    if "20 litres" in question_lower or "20 liters" in question_lower:

        moisture = FARM_DATA["soil_moisture"]
        rain = FARM_DATA["rain_probability"]

        if moisture < 30 and rain < 30:
            recommended = 20
            return (
                f"The recommended water amount is {recommended} litres "
                f"because soil moisture is {moisture}% and rain probability "
                f"is {rain}%."
            )

    return None


def workflow(question):

    answer = get_course_or_farm_value(question)

    if answer:
        return answer

    answer = irrigation_decision(question)

    if answer:
        return answer

    answer = water_calculation(question)

    if answer:
        return answer

    if "two-line" in question.lower() or "two line" in question.lower():

        return (
            "Smart irrigation helps farmers save water and improve crop growth.\n"
            "Using farm data can support better irrigation decisions."
        )

    return (
        "I cannot answer this question because no matching "
        "rule is available."
    )


if __name__ == "__main__":

    QUESTIONS = [
        "What is the current soil moisture of the tomato field?",
        "Should I irrigate the tomato crop today?",
        "The soil moisture is 28% and rain probability is 10%. "
        "How much water should I provide if the recommended amount is 20 litres?",
        "Give me a two-line message encouraging farmers to use smart irrigation."
    ]

    print("=" * 60)
    print("RULE-BASED WORKFLOW")
    print("=" * 60)

    for i, question in enumerate(QUESTIONS, 1):

        print(f"\nQ{i}: {question}")

        answer = workflow(question)

        print("Answer:", answer)