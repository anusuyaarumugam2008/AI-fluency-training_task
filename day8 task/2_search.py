
"""Search library policy documents stored in Chroma."""

from lc_config import get_vectorstore


def search_library(question):
    store = get_vectorstore()

    results = store.similarity_search_with_score(
        question,
        k=3,
    )

    if not results:
        print("No matching documents found.")
        return

    print(f"\nQuestion: {question}")
    print("\nRelevant library information:")

    for index, (document, score) in enumerate(results, start=1):
        source = document.metadata.get("source", "unknown")

        print(f"\nResult {index}")
        print(f"Source: {source}")
        print(f"Distance: {score:.4f}")
        print("Content:")
        print(document.page_content)


if __name__ == "__main__":
    questions = [
        "How many days can I borrow a book?",
        "What is the fine for returning a book late?",
        "What time does the library open on Saturday?",
    ]

    for question in questions:
        search_library(question)
        print("\n" + "=" * 50)