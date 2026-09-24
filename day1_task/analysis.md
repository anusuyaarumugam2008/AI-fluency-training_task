# Smart Agriculture Assistant

## 1. Introduction

This project compares three approaches for solving a smart agriculture problem:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent

The scenario uses private farm data such as crop type, soil moisture, temperature, soil pH, rain probability, and water tank level.

The main goal is to understand how the three approaches differ in flexibility, decision-making, private-data access, tool usage, multi-step task handling, automation, and reliability.

---

# 2. Scenario

The selected scenario is a Smart Agriculture Assistant.

The private farm data used in this project is:

| Parameter | Value |
|---|---:|
| Crop | Tomato |
| Soil Moisture | 28% |
| Temperature | 32°C |
| Soil pH | 6.5 |
| Rain Probability | 10% |
| Water Tank | 60% |

The assistant can answer questions related to the farm and irrigation.

---

# 3. Plain Chatbot

The plain chatbot uses a Large Language Model through the Groq API.

It does not receive the private farm database and does not have access to external tools.

Therefore, it can answer general agriculture questions, but it cannot reliably provide private farm values.

For example, when asked for the exact soil moisture, the chatbot does not have access to the private value of 28%.

### Strengths

- Simple implementation
- Natural language interaction
- Good for general questions
- No tool setup is required

### Limitations

- Cannot reliably access private farm data
- May provide an incorrect value when private data is unavailable
- Cannot perform controlled farm-data operations

---

# 4. Rule-Based Workflow

The rule-based workflow uses predefined Python conditions.

For example:

```python
if soil_moisture < 30 and rain_probability < 30:
    irrigation = "YES"