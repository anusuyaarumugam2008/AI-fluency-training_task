# Task 2: Reasoning and Acting in Smart Agriculture

## 1. Introduction

This project compares three approaches for a Smart Agriculture Assistant:

1. Direct Prompting
2. Chain-of-Thought-style Prompting
3. ReAct (Reasoning and Acting)

A self-consistency experiment is also performed to study how repeated
non-zero-temperature responses affect answer consistency.

The implementation uses Groq through the OpenAI-compatible Python API.

---

## 2. Scenario

The scenario is a tomato farm.

The tomato crop is at the flowering stage.

The simulated farm information is:

- Farm area: 1 acre
- Soil moisture: 30%
- Irrigation threshold: 35%
- Temperature: 31°C
- Humidity: 68%
- Rain probability: 70%
- Expected rainfall: 12 mm

The assistant is expected to help with irrigation, weather-related
decisions, crop conditions, and simple agricultural calculations.

---

## 3. Tools Used

The ReAct agent has access to the following tools:

### get_soil_moisture()

Returns:

- Current soil moisture
- Irrigation threshold

### get_weather()

Returns:

- Temperature
- Humidity
- Rain probability
- Expected rainfall

### get_crop_information()

Returns:

- Crop type
- Growth stage
- Farm area

### calculator(expression)

Performs simple arithmetic calculations.

For example:

20 × 45 = 900 litres

---

# 4. Direct Prompting

Direct prompting sends the user's question directly to the language model
without explicitly requiring tool use or a multi-step reasoning process.

Example questions include:

- What factors should be checked before irrigation?
- How much water is delivered by an irrigation system?
- What can cause yellow tomato leaves?
- Should irrigation be considered when rain is expected?

### Observation

Direct prompting is simple and fast.

The model can provide useful agricultural explanations and calculations,
but it does not automatically obtain live or external farm information
unless that information is included in the prompt.

---

# 5. Chain-of-Thought-Style Prompting

The second approach asks the model to solve a problem using a short,
numbered reasoning process.

The prompt asks the model to:

1. Identify important information.
2. Apply the relevant calculation or reasoning.
3. State the final answer.

### Example

For an irrigation calculation:

20 litres/minute × 45 minutes

= 900 litres

### Observation

The step-by-step format makes the calculation easier to follow and
compare with a direct answer.

It is especially useful for multi-step calculations and questions where
several factors need to be considered.

---

# 6. ReAct Agent

The ReAct approach combines reasoning with actions through tools.

The agent can:

1. Receive the user question.
2. Decide which information is needed.
3. Call an appropriate tool.
4. Observe the tool result.
5. Use the result to produce the final answer.

For example, for the irrigation question, the agent can call:

get_soil_moisture()

and:

get_weather()

The returned observations are then supplied back to the model.

### Example Trace

USER QUESTION:

Should I irrigate the tomato crop now?

ACTION:

get_soil_moisture()

OBSERVATION:

Soil moisture = 30%
Irrigation threshold = 35%

ACTION:

get_weather()

OBSERVATION:

Rain probability = 70%
Expected rainfall = 12 mm

FINAL ANSWER:

The decision should consider both the soil moisture being below the
threshold and the high probability of rainfall. The farmer should
consider the expected rainfall and crop requirements before deciding
whether immediate irrigation is necessary.

### Observation

ReAct provides a visible action and observation trace.

It is more suitable when the answer depends on information that must be
retrieved from tools rather than only from the language model.

---

# 7. Comparison

| Aspect | Direct Prompting | CoT-Style Prompting | ReAct |
|---|---|---|---|
| Reasoning depth | Basic | More structured | Structured with actions |
| Tool usage | No | No | Yes |
| External information | Only information in prompt | Only information in prompt | Can retrieve through tools |
| Transparency | Low to moderate | Higher because steps are requested | High because actions and observations are visible |
| Speed | Fast | Usually slightly slower | Slower because tools add steps |
| Cost | Lower | Potentially higher | Potentially higher |
| Consistency | Depends on temperature | Can vary | Depends on model and tool selection |
| Best suited for | Simple questions | Multi-step reasoning | Information retrieval and actions |

These approaches are not interchangeable.

Direct prompting is useful for simple questions.

CoT-style prompting is useful when a structured solution is helpful.

ReAct is useful when the assistant needs information from external tools
before producing an answer.

---

# 8. Self-Consistency Experiment

The self-consistency experiment uses the following calculation:

A tomato irrigation system delivers 20 litres per minute and runs for
45 minutes.

Expected answer:

20 × 45 = 900 litres

The experiment uses:

- Temperature 0 for the baseline.
- Temperature 0.8 for five independent runs.

The five answers are recorded by the program.

The majority answer is then calculated using a vote over the extracted
numerical answers.

### Result

The expected correct answer is:

**900 litres**

The temperature-0 result can be compared with the majority answer from
the five non-zero-temperature runs.

### Interpretation

If the majority answer matches the temperature-0 answer, the repeated
runs show consistency for this particular calculation.

If different answers occur, the majority vote can provide a way to select
the most frequently occurring result, but frequency alone does not prove
that an answer is correct.

---

# 9. Observations

### Direct Prompting

- Simple to implement.
- Fast for straightforward questions.
- Does not automatically retrieve farm data.
- Results depend on the information supplied in the prompt.

### CoT-Style Prompting

- Gives a more structured solution.
- Useful for calculations and multi-step problems.
- Requires additional prompt instructions.
- May require more output tokens.

### ReAct

- Can use external tools.
- Produces an action-observation trace.
- Useful when current farm information is required.
- Adds additional model calls and therefore can increase latency and cost.
- Tool selection can affect the final answer.

### Self-Consistency

- Repeats the same problem at a non-zero temperature.
- Allows comparison of different generated answers.
- Majority voting can show whether answers are consistent.
- Repetition increases the number of model calls.

---

# 10. Reliability

Reliability depends on the type of question.

For a simple arithmetic calculation, a direct or structured prompt may be
sufficient.

For a question requiring current farm conditions, relying only on the
model's internal knowledge is less appropriate because the model does not
automatically know the current sensor values.

The ReAct approach addresses this by obtaining the simulated farm data
through tools.

However, ReAct does not guarantee correctness. Incorrect tool selection,
incorrect interpretation of observations, or incorrect final reasoning can
still produce an incorrect answer.

---

# 11. Limitations

This project uses simulated agriculture data rather than real farm sensors.

The weather information is also simulated.

The calculator supports only simple arithmetic expressions.

The project does not directly control real irrigation equipment.

The experiment also uses a small number of self-consistency runs, so the
results should not be treated as a statistical evaluation of the model.

---

# 12. When Each Approach Is Appropriate

### Direct Prompting

Appropriate for:

- Simple questions
- General explanations
- Short answers
- Tasks where all required information is already available

### CoT-Style Prompting

Appropriate for:

- Multi-step calculations
- Problems requiring several reasoning stages
- Situations where a structured solution is useful

### ReAct

Appropriate for:

- Tool-based applications
- Sensor information
- Weather information
- External data retrieval
- Tasks where the assistant must act based on observations

---

# 13. Conclusion

The Smart Agriculture Assistant demonstrates three different ways of
solving problems with a language model.

Direct prompting provides a simple baseline.

CoT-style prompting provides a more structured approach to multi-step
problems.

ReAct extends the assistant with tools so that it can retrieve farm
information before producing an answer.

The self-consistency experiment demonstrates how multiple non-zero-
temperature responses can be compared using majority voting.

For a practical agriculture assistant, the choice of approach depends on
the task. Questions requiring only explanation can use direct prompting,
while structured calculations can benefit from step-by-step prompting.
Questions requiring farm observations or external information are suitable
for a tool-using ReAct workflow.