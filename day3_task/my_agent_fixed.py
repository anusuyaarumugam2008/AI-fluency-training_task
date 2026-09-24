from my_agent import ask_agent


questions = [
    "The soil moisture is 30%. What should I check before irrigating my tomato crop?",
    "My irrigation system provides 20 liters per minute. How much water will it provide in 45 minutes?",
    "The soil moisture is 30% and rain probability is high. Should irrigation be considered immediately?"
]


def main():
    print("=" * 60)
    print("SMART AGRICULTURE ASSISTANT - DEMO")
    print("=" * 60)

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}:")
        print(question)

        answer = ask_agent(question)

        print("\nAnswer:")
        print(answer)
        print("-" * 60)


if __name__ == "__main__":
    main()