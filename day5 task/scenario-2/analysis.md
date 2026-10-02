# Scenario 2: Student Study Assistant

## 1. Scenario

For this scenario, I created a Student Study Assistant using the Groq API.

The assistant is designed to help students understand academic concepts using simple language. It can explain difficult topics, provide examples, break complicated ideas into smaller steps, and encourage students to understand the reasoning.

The Python program demonstrates non-streaming requests, streaming requests, repeated prompts, performance measurements, and a system-prompt override test.

Ollama was not installed on the system, so the practical implementation was completed using Groq.

---

# 2. Ollama Explanation

Ollama is a local model-serving platform that allows language models to be run and managed on a computer.

Important parts of an Ollama setup include:

- Ollama CLI
- Ollama server/API
- Local language models
- Modelfiles for model configuration

The CLI can be used to manage models and start model interactions.

The Ollama server provides an API through which applications can send prompts and receive model responses.

A local model can therefore be used by a Python application without sending every request to an external model provider.

For this project, Ollama was not installed, so local Ollama performance was not measured.

---

# 3. Modelfile Explanation

A Modelfile is used with Ollama to define a customized model configuration.

The planned Student Study Assistant Modelfile contains:

```text
FROM llama3.2:3b

PARAMETER temperature 0.3
PARAMETER num_ctx 2048

SYSTEM """
You are a Student Study Assistant.

Your job is to help students understand academic topics
clearly and simply.

Rules:
1. Explain difficult topics using simple language.
2. Give examples when useful.
3. Break complicated concepts into smaller steps.
4. Do not invent facts.
5. If a question is unclear, ask for clarification.
6. Keep answers focused on the student's question.
7. When appropriate, provide a short practice question.
8. Help students understand the reasoning instead of
   simply giving an answer.
"""