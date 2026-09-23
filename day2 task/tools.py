import ast
import operator


# -----------------------------
# Simulated agriculture data
# -----------------------------

FARM_DATA = {
    "soil_moisture": 30,
    "temperature": 31,
    "humidity": 68,
    "rain_probability": 70,
    "expected_rainfall_mm": 12,
    "crop": "tomato",
    "growth_stage": "flowering",
    "area_acres": 1,
    "irrigation_threshold": 35,
}


def get_soil_moisture():
    return {
        "soil_moisture_percent": FARM_DATA["soil_moisture"],
        "irrigation_threshold_percent": FARM_DATA["irrigation_threshold"],
    }


def get_weather():
    return {
        "temperature_c": FARM_DATA["temperature"],
        "humidity_percent": FARM_DATA["humidity"],
        "rain_probability_percent": FARM_DATA["rain_probability"],
        "expected_rainfall_mm": FARM_DATA["expected_rainfall_mm"],
    }


def get_crop_information():
    return {
        "crop": FARM_DATA["crop"],
        "growth_stage": FARM_DATA["growth_stage"],
        "area_acres": FARM_DATA["area_acres"],
    }


# -----------------------------
# Safe calculator
# -----------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculator(expression):
    """
    Safely evaluate simple arithmetic expressions.
    Example: calculator("20 * 45")
    """

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            operation = ALLOWED_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not allowed.")

            return operation(
                evaluate(node.left),
                evaluate(node.right)
            )

        raise ValueError("Invalid arithmetic expression.")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


# -----------------------------
# Tool schemas for Groq
# -----------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_soil_moisture",
            "description": "Get current soil moisture and irrigation threshold.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather and rain forecast information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_crop_information",
            "description": "Get crop type, growth stage and farm area.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform simple arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A simple arithmetic expression such as 20 * 45.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]