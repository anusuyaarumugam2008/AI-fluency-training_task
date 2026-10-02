import os
import time

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------
# Load API key
# ---------------------------------------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Please check your .env file."
    )

client = Groq(api_key=api_key)


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------
MODEL = "openai/gpt-oss-20b"


# ---------------------------------------------------------
# Student Study Assistant system prompt
# ---------------------------------------------------------
SYSTEM_PROMPT = """
You are a Student Study Assistant.

Your job is to help students understand academic topics
clearly and simply.

Rules:
1. Explain difficult topics using simple language.
2. Give examples when they improve understanding.
3. Break complicated concepts into smaller steps.
4. Do not invent facts.
5. If a question is unclear, ask for clarification.
6. Keep answers focused on the student's question.
7. When appropriate, provide a short practice question.
8. Do not simply give an answer when explaining a concept;
   help the student understand the reasoning.
"""


# ---------------------------------------------------------
# NON-STREAMING REQUEST
# ---------------------------------------------------------
def non_streaming_request(prompt):

    print("\n" + "=" * 60)
    print("NON-STREAMING REQUEST")
    print("=" * 60)

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
        max_completion_tokens=300,
        stream=False
    )

    end_time = time.perf_counter()

    answer = response.choices[0].message.content

    total_time = end_time - start_time

    print("\nPrompt:")
    print(prompt)

    print("\nAnswer:")
    print(answer)

    print("\nPerformance:")
    print(f"Total time: {total_time:.3f} seconds")

    if response.usage:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Completion tokens: {completion_tokens}")
        print(f"Total tokens: {total_tokens}")

        if total_time > 0:
            tokens_per_second = completion_tokens / total_time
            print(f"Tokens/sec: {tokens_per_second:.2f}")

    return answer


# ---------------------------------------------------------
# STREAMING REQUEST
# ---------------------------------------------------------
def streaming_request(prompt):

    print("\n" + "=" * 60)
    print("STREAMING REQUEST")
    print("=" * 60)

    start_time = time.perf_counter()
    first_token_time = None

    stream = client.chat.completions.create(
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
        max_completion_tokens=300,
        stream=True
    )

    full_answer = ""

    print("\nPrompt:")
    print(prompt)

    print("\nAnswer:")

    for chunk in stream:

        text = chunk.choices[0].delta.content

        if text:

            if first_token_time is None:
                first_token_time = time.perf_counter()

            print(text, end="", flush=True)
            full_answer += text

    end_time = time.perf_counter()

    total_time = end_time - start_time

    if first_token_time is not None:
        ttft = first_token_time - start_time
    else:
        ttft = 0

    estimated_tokens = len(full_answer.split())

    if total_time > 0:
        tokens_per_second = estimated_tokens / total_time
    else:
        tokens_per_second = 0

    print("\n\nPerformance:")
    print(f"TTFT: {ttft:.3f} seconds")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Estimated tokens: {estimated_tokens}")
    print(f"Estimated tokens/sec: {tokens_per_second:.2f}")

    return full_answer


# ---------------------------------------------------------
# SYSTEM PROMPT OVERRIDE TEST
# ---------------------------------------------------------
def system_prompt_override_test(prompt):

    print("\n" + "=" * 60)
    print("SYSTEM PROMPT OVERRIDE TEST")
    print("=" * 60)

    custom_system_prompt = """
You are a Student Study Assistant.

For this test:
- Answer using exactly TWO short sentences.
- Use very simple language.
- Do not provide a long explanation.
"""

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        reasoning_effort="low",
        messages=[
            {
                "role": "system",
                "content": custom_system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=300,
        stream=False
    )

    end_time = time.perf_counter()

    answer = response.choices[0].message.content

    print("\nProgram system prompt:")
    print(custom_system_prompt)

    print("\nUser prompt:")
    print(prompt)

    print("\nModel response:")
    print(answer)

    print(f"\nTotal time: {end_time - start_time:.3f} seconds")

    return answer


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():

    print("\n")
    print("=" * 60)
    print("STUDENT STUDY ASSISTANT")
    print("=" * 60)

    # Prompt 1
    prompt1 = (
        "Explain photosynthesis to a school student "
        "using simple language."
    )

    non_streaming_request(prompt1)

    # Prompt 2
    prompt2 = (
        "Explain the difference between artificial intelligence "
        "and machine learning with a simple example."
    )

    streaming_request(prompt2)

    # Prompt 3
    prompt3 = (
        "Explain what a Python variable is and give "
        "two simple examples."
    )

    non_streaming_request(prompt3)

    # Repeat Prompt 1
    print("\n")
    print("=" * 60)
    print("REPEATING PROMPT 1")
    print("=" * 60)

    non_streaming_request(prompt1)

    # System prompt override
    override_prompt = (
        "What is machine learning?"
    )

    system_prompt_override_test(override_prompt)


# ---------------------------------------------------------
# Start program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()