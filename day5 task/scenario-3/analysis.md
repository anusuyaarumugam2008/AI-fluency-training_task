# Scenario 3: Customer Support Assistant

## 1. Scenario

For this scenario, I created a Customer Support Assistant using the Groq API.

The assistant is designed to answer common customer-support questions using simple, polite and practical language.

The assistant follows these rules:

- Be polite and professional.
- Use simple language.
- Give practical next steps.
- Do not invent order numbers, refunds, prices or policies.
- Ask for missing information when necessary.
- Keep answers concise.
- Do not blame the customer.

The Python program demonstrates non-streaming requests, streaming requests, repeated requests, performance measurement and a system-prompt override test.

Ollama was not installed on my system, so the working implementation was completed using the Groq API.

---

## 2. Ollama Explanation

Ollama is a local model-serving platform that allows language models to be run and managed on a computer.

The Day 5 task describes Ollama as a server that can be reached through different interfaces, including the command line, REST API and OpenAI-compatible endpoint.

The main parts involved are:

1. The Ollama command-line interface, which can be used to manage and interact with models.
2. The Ollama server, which receives requests and runs the model.
3. The model itself, which generates the requested response.

In a normal Ollama setup, a request is sent to the local server, the server processes the prompt using the selected model, and the generated response is returned to the application.

For this project, Ollama was not installed, so I did not perform local Ollama measurements or claim that the model was actually served through Ollama.

---

## 3. Modelfile Explanation

A Modelfile is used by Ollama to define a customized model configuration.

For the Customer Support Assistant, the planned Modelfile can contain a base model, parameter values and a system prompt.

Example:

    FROM llama3.2:3b

    PARAMETER temperature 0.3
    PARAMETER num_ctx 2048

    SYSTEM """
    You are a Customer Support Assistant.

    Be polite and professional.
    Use simple language.
    Give practical next steps.
    Do not invent customer information or policies.
    Ask for missing information when necessary.
    Keep answers concise.
    """

The `FROM` instruction specifies the base model.

The `temperature` parameter controls the variability of generated responses. A value such as `0.3` is suitable for a support assistant that should provide relatively focused answers.

The `num_ctx` parameter controls the context available to the model.

The `SYSTEM` instruction defines the default behaviour of the Customer Support Assistant.

A custom model is based on an existing model together with configuration and instructions. Creating a custom configuration does not necessarily mean that an entirely new set of model weights has been trained.

Because Ollama was not installed for this implementation, this Modelfile was documented but not executed with `ollama create`.

---

## 4. System Prompt Override

The Day 5 task asks the program to demonstrate what happens when a program supplies its own system prompt to a model that already has a default system prompt.

In my Groq implementation, the Python program supplies the system prompt directly.

The normal system prompt defines the Customer Support Assistant behaviour.

For the override test, the program used:

    You are a Customer Support Assistant.

    For this test:
    - Answer using exactly TWO short sentences.
    - Use simple language.
    - Be polite.
    - Do not give a long explanation.

The user prompt was:

    A customer says: "I was charged twice for the same order.
    What should I do?"

The model responded:

    I'm sorry you were charged twice. Please send me your
    order number and I'll correct it right away.

The response followed the two-sentence instruction.

This demonstrates that the application can provide its own system instructions for a particular request.

---

## 5. /api/generate vs /api/chat

Ollama provides different API interfaces.

`/api/generate` is intended for generating a response from a prompt.

`/api/chat` is intended for conversational interactions using messages such as system, user and assistant messages.

The chat approach is useful when an application needs to represent conversation history and different message roles.

The OpenAI-compatible endpoint provides an interface that follows a commonly used API format.

This can make it easier for an application to move between different model-serving systems because the application can use a familiar request structure.

My working implementation used the Groq chat-completions API rather than Ollama's `/api/generate` or `/api/chat` endpoints.

---

## 6. Streaming

Streaming means that the response is returned progressively while the model is generating it.

Instead of waiting for the complete response, the application can display pieces of the response as they arrive.

This makes the application feel more responsive because the user can start reading the answer earlier.

Streaming does not necessarily reduce the total amount of model generation required.

It mainly changes when the user begins seeing the answer.

---

## 7. TTFT and Total Time

TTFT means Time To First Token.

It measures the time between starting the request and receiving the first generated output.

Total time measures how long the complete request takes from beginning to end.

For example, a streaming request may have a small TTFT, allowing the customer to see the beginning of the answer quickly, while the complete answer takes longer to finish.

Therefore, streaming can improve perceived responsiveness without necessarily reducing total generation time.

---

## 8. num_ctx, OLLAMA_KEEP_ALIVE and OLLAMA_NUM_PARALLEL

`num_ctx` controls the amount of context available to the model.

A larger context means that more tokens can be considered during a request, but it also increases memory requirements.

`OLLAMA_KEEP_ALIVE` controls how long a model remains loaded in memory after a request.

Keeping a model loaded can reduce the delay caused by repeatedly loading the model.

`OLLAMA_NUM_PARALLEL` controls the number of parallel requests that an Ollama server can process.

The KV cache stores information from tokens that have already been processed during generation.

As context size increases, the KV cache can require more memory.

My implementation used Groq rather than Ollama, so I did not directly measure these Ollama settings.

---

## 9. KV Cache and PagedAttention

The KV cache stores intermediate key and value information used by transformer attention during generation.

A simple serving system can use a significant amount of GPU memory for KV-cache data when several requests are active.

PagedAttention addresses this memory-management problem by dividing KV-cache memory into fixed-size blocks and managing those blocks using a block table.

This approach can reduce memory fragmentation and improve memory utilization when many requests are being served.

Prefix caching can provide another benefit when the same beginning of a prompt is repeatedly used.

For example, a customer-support application may repeatedly send the same system instructions. Reusing cached information from the common prefix can avoid unnecessary repeated computation.

---

## 10. Static vs Continuous Batching

Static batching groups requests together before processing them.

The requests in the batch are selected at a particular time and processed together.

Continuous batching allows requests to enter and leave the processing schedule dynamically.

This is useful for serving many users because different requests can have different prompt and generation lengths.

Important performance measurements include:

### Throughput

Throughput describes how much work the server completes over a period of time.

### TTFT

TTFT is the time until the first generated token is received.

### TPOT

TPOT means Time Per Output Token. It describes the time required to generate output tokens after generation has started.

### P95 latency

P95 latency is the latency value below which approximately 95 percent of requests fall.

Increasing throughput can sometimes increase individual-request latency because more requests compete for available resources.

Therefore, a serving system needs to balance throughput, TTFT, TPOT and tail latency.

---

# 11. Ollama vs vLLM

| Basis for comparison | Ollama | vLLM |
|---|---|---|
| Built for | Local model use and simpler serving | High-throughput model serving |
| Typical users | Individual developers and smaller applications | Applications serving many concurrent users |
| Hardware | Can run models on supported local hardware | Commonly used with capable GPU server hardware |
| Several requests | Can serve multiple requests | Designed for efficient concurrent serving |
| Memory management | Provides local model serving and memory management | Uses techniques such as efficient KV-cache management and PagedAttention |
| Batching | Supports serving requests | Designed for high-throughput batching |
| Setup effort | Relatively simple for local experimentation | More focused on production-style serving |
| Model configuration | Uses Modelfiles | Focuses on serving and deployment |
| Single-user scenario | Suitable for local model experimentation | Can be used when high-throughput serving is required |
| Large shared deployment | May require additional infrastructure | Designed for larger concurrent workloads |

The comparison is conceptual for this project because vLLM was not installed or tested.

---

# 12. Actual Observations

The Customer Support Assistant was successfully executed using the Groq API.

The program performed several requests.

### Prompt 1

The first prompt was:

    My package has not arrived yet.
    What information should I provide to customer support?

The program generated a customer-support response.

### Prompt 2

The streaming request used:

    I received a damaged product.
    What should I do next?

The program displayed the answer progressively as the response was streamed.

### Prompt 3

Another prompt asked:

    I forgot my order number.
    Can customer support still help me?

The model generated a response using the Customer Support Assistant instructions.

### Repeated request

The first package-delivery prompt was run again.

This was included to compare repeated requests as required by the task.

Because the implementation used the Groq API rather than a local Ollama server, I did not claim local model-load measurements using `ollama ps` or `/api/ps`.

---

# 13. Performance Observations

The program recorded token and timing information for the API requests.

The final system-prompt override request produced these observed results:

| Measurement | Observed value |
|---|---:|
| Total time | 0.674 seconds |
| Completion tokens | 136 |
| Total tokens | 309 |
| Tokens/sec | 457.93 |

The system-prompt override response followed the requested two-sentence format.

The observed response was:

    I'm sorry you were charged twice. Please send me your
    order number and I'll correct it right away.

The timing values are measurements from this particular API run. They can change depending on network conditions, API server load, prompt length, output length and other runtime conditions.

---

# 14. Streaming Observation

The streaming test demonstrated that the model output can be displayed progressively.

The main advantage of streaming is that the customer does not have to wait for the entire answer before seeing any response.

This is useful in a customer-support application because a user can immediately see that the assistant has started processing the request.

The total generation work is not necessarily reduced by streaming.

---

# 15. System Prompt Behaviour

The normal system prompt instructed the model to behave as a Customer Support Assistant.

The override test supplied a different system prompt requiring exactly two short sentences.

The resulting answer followed the override instructions.

This demonstrates why application-level system instructions are useful: an application can change the behaviour required for a particular request without changing the underlying model itself.

---

# 16. Suitability

For a small customer-support assistant used by an individual or for a demonstration, a simple model-serving setup can be sufficient.

Ollama can be useful when the goal is to run a model locally and experiment with model configuration through a Modelfile and local REST APIs.

If the application needs to serve many users simultaneously, the serving system must manage GPU memory, KV caches, scheduling, batching and latency.

A system such as vLLM is designed for high-throughput model serving and can provide techniques intended for concurrent workloads.

For this project, Groq was used because Ollama was not installed.

Therefore, the practical measurements in this project are Groq API measurements rather than measurements from an Ollama server.

---

# 17. Conclusion

The Customer Support Assistant demonstrates how an LLM can be configured to follow a fixed role and provide consistent support-oriented responses.

The implementation demonstrated:

1. Non-streaming requests.
2. Streaming requests.
3. Multiple customer-support prompts.
4. A repeated request.
5. Token and timing measurements.
6. A system-prompt override test.
7. TTFT measurement for streaming.
8. Tokens-per-second measurement.

The experiment showed that system prompts can control the behaviour and response format of an LLM.

Ollama provides a local model-serving approach with Modelfiles and REST APIs.

For larger deployments with many concurrent users, memory management, scheduling and batching become increasingly important. Technologies designed for high-throughput serving, such as vLLM, address these types of requirements.

For this implementation, Groq was used instead of Ollama because Ollama was not installed. Consequently, Ollama-specific runtime measurements such as model loading through `ollama ps` were not available and have not been presented as observed results.