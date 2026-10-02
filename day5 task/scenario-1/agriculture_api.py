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
# Groq model
# ---------------------------------------------------------
MODEL = "openai/gpt-oss-20b"


# ---------------------------------------------------------
# Smart Agriculture Assistant system prompt
# ---------------------------------------------------------
SYSTEM_PROMPT = """
You are a Smart Agriculture Assistant.

Your job is to help farmers with simple and practical
agricultural guidance.

Rules:
1. Give clear and easy-to-understand answers.
2. Consider crop health, soil, water, weather and
   common farming practices.
3. Do not invent exact pesticide or chemical dosages.
4. If important information is missing, say what
   information is needed.
5. Keep answers concise and practical.
6. Recommend consulting a local agricultural expert
   when necessary.
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

    if first_token_time:
        ttft = first_token_time - start_time
    else:
        ttft = 0

    # Approximate output token count
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


# ---------------------------------------------------------
# SYSTEM PROMPT OVERRIDE TEST
# ---------------------------------------------------------
def system_prompt_override_test(prompt):

    print("\n" + "=" * 60)
    print("SYSTEM PROMPT OVERRIDE TEST")
    print("=" * 60)

    custom_system_prompt = """
You are a Smart Agriculture Assistant.

For this test:
- Reply using exactly TWO short sentences.
- Keep the answer simple.
- Do not provide a long explanation.
"""

    start_time = time.perf_counter()

   
    response = client.chat.completions.create(
        model=MODEL,
        reasoning_effort="low",        messages=[
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


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():

    print("\n")
    print("=" * 60)
    print("SMART AGRICULTURE ASSISTANT")
    print("=" * 60)

    # -----------------------------------------------------
    # Prompt 1
    # -----------------------------------------------------
    prompt1 = (
        "My tomato plants have yellow leaves. "
        "What are some common causes I should check?"
    )

    non_streaming_request(prompt1)

    # -----------------------------------------------------
    # Prompt 2
    # -----------------------------------------------------
    prompt2 = (
        "What information should a farmer collect before "
        "deciding how often to irrigate a vegetable crop?"
    )

    streaming_request(prompt2)

    # -----------------------------------------------------
    # Prompt 3
    # -----------------------------------------------------
    prompt3 = (
        "My rice crop is showing brown spots on the leaves. "
        "What information would you need before suggesting "
        "possible causes?"
    )

    non_streaming_request(prompt3)

    # -----------------------------------------------------
    # Repeat Prompt 1
    # -----------------------------------------------------
    print("\n")
    print("=" * 60)
    print("REPEATING PROMPT 1")
    print("=" * 60)

    non_streaming_request(prompt1)

    # -----------------------------------------------------
    # System prompt override
    # -----------------------------------------------------
    override_prompt = (
        "My tomato plants have yellow leaves. "
        "What should I check first?"
    )

    system_prompt_override_test(override_prompt)


# ---------------------------------------------------------
# Start program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()