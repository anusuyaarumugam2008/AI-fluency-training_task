"""
Day 5 - Scenario 3
Customer Support Assistant

Groq-based implementation.
Demonstrates:
1. Non-streaming request
2. Streaming request
3. Repeated prompt
4. System prompt override
5. Performance measurements
"""

import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add your API key to the .env file."
    )

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


SYSTEM_PROMPT = """
You are a Customer Support Assistant.

Your job is to help customers with simple and clear answers.

Rules:
1. Be polite and professional.
2. Use simple language.
3. Give practical next steps.
4. Do not invent order numbers, refunds, prices, or policies.
5. If important information is missing, ask the customer for it.
6. Keep answers concise.
7. Never blame the customer.
"""


def non_streaming_request(prompt):
    """Send a normal request and return the complete answer."""

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300,
        stream=False
    )

    end_time = time.perf_counter()

    answer = response.choices[0].message.content

    total_time = end_time - start_time

    usage = response.usage

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    tokens_per_second = (
        completion_tokens / total_time
        if total_time > 0
        else 0
    )

    print("\n" + "=" * 60)
    print("NON-STREAMING REQUEST")
    print("=" * 60)

    print("\nPrompt:")
    print(prompt)

    print("\nAnswer:")
    print(answer)

    print("\nPerformance:")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Tokens/sec: {tokens_per_second:.2f}")

    return answer


def streaming_request(prompt):
    """Send a streaming request and measure TTFT and total time."""

    start_time = time.perf_counter()
    first_token_time = None

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300,
        stream=True
    )

    print("\n" + "=" * 60)
    print("STREAMING REQUEST")
    print("=" * 60)

    print("\nPrompt:")
    print(prompt)

    print("\nAnswer:")

    full_answer = ""

    for chunk in response:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content

        if delta:
            if first_token_time is None:
                first_token_time = time.perf_counter()

            print(delta, end="", flush=True)
            full_answer += delta

    end_time = time.perf_counter()

    if first_token_time is not None:
        ttft = first_token_time - start_time
    else:
        ttft = 0

    total_time = end_time - start_time

    print("\n")

    print("Performance:")
    print(f"TTFT: {ttft:.3f} seconds")
    print(f"Total time: {total_time:.3f} seconds")

    return full_answer


def system_prompt_override_test(prompt):
    """
    Demonstrate that the application's system prompt
    can provide different instructions.
    """

    override_prompt = """
You are a Customer Support Assistant.

For this test:
- Answer using exactly TWO short sentences.
- Use simple language.
- Be polite.
- Do not give a long explanation.
"""

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": override_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=100,
        stream=False
    )

    end_time = time.perf_counter()

    answer = response.choices[0].message.content

    total_time = end_time - start_time

    print("\n" + "=" * 60)
    print("SYSTEM PROMPT OVERRIDE TEST")
    print("=" * 60)

    print("\nProgram system prompt:")
    print(override_prompt.strip())

    print("\nUser prompt:")
    print(prompt)

    print("\nModel response:")
    print(answer)

    print(f"\nTotal time: {total_time:.3f} seconds")

    return answer


def main():

    print("\n" + "=" * 60)
    print("CUSTOMER SUPPORT ASSISTANT")
    print("=" * 60)

    # Scenario prompt 1
    prompt1 = (
        "My package has not arrived yet. "
        "What information should I provide to customer support?"
    )

    non_streaming_request(prompt1)

    # Scenario prompt 2
    prompt2 = (
        "I received a damaged product. "
        "What should I do next?"
    )

    streaming_request(prompt2)

    # Scenario prompt 3
    prompt3 = (
        "I forgot my order number. "
        "Can customer support still help me?"
    )

    non_streaming_request(prompt3)

    # Run one prompt again
    print("\n" + "=" * 60)
    print("REPEATED REQUEST")
    print("=" * 60)

    non_streaming_request(prompt1)

    # System prompt override
    override_prompt = (
        "A customer says: 'I was charged twice for the same order. "
        "What should I do?'"
    )

    system_prompt_override_test(override_prompt)


if __name__ == "__main__":
    main()