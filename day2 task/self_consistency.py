from collections import Counter

from config import client, MODEL


QUESTION = """
A tomato irrigation system delivers 20 litres of water per minute.
If the system runs for 45 minutes, how many litres of water are delivered?
"""


def ask(question, temperature):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a Smart Agriculture Assistant."
            },
            {
                "role": "user",
                "content": f"""
Solve this agriculture calculation carefully.

Show a short calculation and clearly state the final numerical answer.

Question:
{question}
"""
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content


def extract_answer(text):
    """
    Extract the final numerical answer from the response.
    """
    import re

    numbers = re.findall(r"\b\d+(?:\.\d+)?\b", text)

    if numbers:
        return numbers[-1]

    return "UNKNOWN"


print("=" * 70)
print("SELF-CONSISTENCY EXPERIMENT")
print("=" * 70)

print("\nQUESTION:")
print(QUESTION)

# ---------------------------------------
# Temperature 0 baseline
# ---------------------------------------

print("\n" + "=" * 70)
print("TEMPERATURE 0 BASELINE")
print("=" * 70)

baseline = ask(QUESTION, 0)

print("\nBASELINE ANSWER:")
print(baseline)

print("\nEXTRACTED ANSWER:")
print(extract_answer(baseline))


# ---------------------------------------
# Multiple non-zero temperature runs
# ---------------------------------------

print("\n" + "=" * 70)
print("MULTIPLE RUNS - TEMPERATURE 0.8")
print("=" * 70)

answers = []

for i in range(5):

    result = ask(QUESTION, 0.8)
    answer = extract_answer(result)

    answers.append(answer)

    print(f"\nRUN {i + 1}")
    print("-" * 40)
    print(result)
    print(f"Extracted answer: {answer}")


# ---------------------------------------
# Majority vote
# ---------------------------------------

counts = Counter(answers)

print("\n" + "=" * 70)
print("MAJORITY VOTE")
print("=" * 70)

print("\nAnswer counts:")

for answer, count in counts.items():
    print(f"{answer}: {count}")

majority_answer = counts.most_common(1)[0][0]

print(f"\nMAJORITY ANSWER: {majority_answer}")

print(f"BASELINE ANSWER: {extract_answer(baseline)}")

if majority_answer == extract_answer(baseline):
    print("\nRESULT: Majority answer matches temperature-0 answer.")
else:
    print("\nRESULT: Majority answer differs from temperature-0 answer.")