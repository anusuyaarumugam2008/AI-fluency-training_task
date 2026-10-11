
"""RAG chain for answering questions about library policies."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from lc_config import get_model, get_vectorstore


# Load the saved library documents
store = get_vectorstore()
retriever = store.as_retriever(search_kwargs={"k": 3})


# Format retrieved documents with their source filenames
def format_documents(documents):
    if not documents:
        return "No relevant library documents were found."

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"{doc.page_content}"
        for doc in documents
    )


# Tell the model how to answer
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful college Smart Library Assistant. "
            "Answer using only the supplied library context. "
            "Mention the source filename when possible. "
            "If the answer is not in the context, say you do not know "
            "and suggest asking the librarian.\n\n"
            "Library context:\n{context}",
        ),
        ("human", "{question}"),
    ]
)


# Build the RAG pipeline
rag_chain = (
    {
        "context": retriever | RunnableLambda(format_documents),
        "question": RunnablePassthrough(),
    }
    | prompt
    | get_model()
    | StrOutputParser()
)


if __name__ == "__main__":
    print("Smart Library Assistant — RAG")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk a library question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = rag_chain.invoke(question)
            print("\nAnswer:", answer)
        except Exception as error:
            print("\nSomething went wrong:", error)