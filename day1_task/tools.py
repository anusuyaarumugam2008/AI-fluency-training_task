import ast
import operator
from config import FARM_DATA


# -----------------------------
# Tool 1: Get Farm Data
# -----------------------------

def get_farm_data(parameter):
    parameter = parameter.lower().strip()

    data = {
        "crop": FARM_DATA["crop"],
        "soil_moisture": FARM_DATA["soil_moisture"],
        "temperature": FARM_DATA["temperature"],
        "soil_ph": FARM_DATA["soil_ph"],
        "rain_probability": FARM_DATA["rain_probability"],
        "water_tank": FARM_DATA["water_tank"]
    }

    if parameter not in data:
        return {
            "error": f"Unknown parameter: {parameter}"
        }

    return {
        "parameter": parameter,
        "value": data[parameter]
    }


# -----------------------------
# Tool 2: Calculator
# -----------------------------

allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = allowed_operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator not allowed")

                return operation(left, right)

            raise ValueError("Invalid expression")

        result = evaluate(tree)

        return {
            "expression": expression,
            "result": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# -----------------------------
# Tool definitions for LLM
# -----------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_farm_data",
            "description": (
                "Get private farm data such as crop, soil moisture, "
                "temperature, soil pH, rain probability, or water tank level."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "parameter": {
                        "type": "string",
                        "enum": [
                            "crop",
                            "soil_moisture",
                            "temperature",
                            "soil_ph",
                            "rain_probability",
                            "water_tank"
                        ]
                    }
                },
                "required": ["parameter"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "safe_calculate",
            "description": (
                "Perform safe arithmetic calculations using numbers "
                "and operators such as +, -, *, and /."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def execute_tool(name, arguments):

    if name == "get_farm_data":
        return get_farm_data(arguments["parameter"])

    if name == "safe_calculate":
        return safe_calculate(arguments["expression"])

    return {
        "error": f"Unknown tool: {name}"
    }