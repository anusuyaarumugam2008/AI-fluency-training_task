import json


def get_soil_moisture():
    """
    Returns simulated soil moisture information for the farm.
    """
    data = {
        "soil_moisture_percent": 30,
        "irrigation_threshold_percent": 35,
        "unit": "percent"
    }

    return json.dumps(data)


def get_weather():
    """
    Returns simulated weather information.
    """
    data = {
        "temperature_c": 31,
        "humidity_percent": 68,
        "rain_probability_percent": 70,
        "expected_rainfall_mm": 12
    }

    return json.dumps(data)


def get_crop_information():
    """
    Returns information about the tomato crop.
    """
    data = {
        "crop": "tomato",
        "growth_stage": "flowering",
        "farm_area_acres": 1,
        "common_issue": "yellow leaves"
    }

    return json.dumps(data)


def calculator(expression):
    """
    Performs a simple mathematical calculation.
    """

    allowed = set("0123456789+-*/(). ")

    if not all(char in allowed for char in expression):
        return "Invalid mathematical expression."

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as error:
        return f"Calculation error: {error}"


TOOLS = {
    "get_soil_moisture": get_soil_moisture,
    "get_weather": get_weather,
    "get_crop_information": get_crop_information,
    "calculator": calculator,
}