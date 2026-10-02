# Scenario 1: Smart Agriculture Assistant

## 1. Scenario

For this task, I created a Smart Agriculture Assistant. The assistant is designed to provide simple and practical guidance to farmers about crop health, irrigation, soil and common agricultural problems.

The assistant was given a fixed behaviour through a system prompt. The system prompt tells the model to give clear answers, consider crop health and farming conditions, avoid inventing exact chemical dosages, identify missing information and recommend a local agricultural expert when necessary.

The practical implementation was completed using the Groq API because Ollama was not installed on the system.

---

# 2. Explanation of Concepts

## 2.1 What is Ollama?

Ollama is a local model-serving system that allows a language model to run on a computer and be accessed by applications.

The three important parts are:

1. The Ollama command-line interface (CLI)
2. The Ollama server/API
3. The model files stored locally

The CLI allows a user to create, run and inspect models. The server receives requests from programs and sends them to the loaded language model. The model files contain the model information and weights required to generate responses.

A request can be sent through the command line or through the REST API. The server receives the request, loads the required model into memory if necessary, processes the prompt and returns the generated response.

For this project, I did not install Ollama. Therefore, I did not directly measure local Ollama model loading or storage behaviour.

---

## 2.2 What is a Modelfile?

A Modelfile is a configuration file used with Ollama to create a customized model configuration.

For the Smart Agriculture Assistant, the planned Modelfile contains:

```text
FROM llama3.2:3b

PARAMETER temperature 0.3
PARAMETER num_ctx 2048

SYSTEM """
You are a Smart Agriculture Assistant.

Your job is to help farmers with simple, practical agricultural guidance.

Rules:
1. Give clear and easy-to-understand answers.
2. Consider crop health, soil, water, weather, and common farming practices.
3. Do not invent exact pesticide or chemical dosages.
4. If important information is missing, clearly say what information is needed.
5. Keep answers concise and practical.
"""