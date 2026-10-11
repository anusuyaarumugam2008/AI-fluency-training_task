
"""Agentic Smart Library Assistant with tools and conversation memory."""

import ast
import operator

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore


# Connect to the existing Chroma library database
store = get_vectorstore()


# Sample fees used for demonstrating tool calls
COURSE_BOOK_FEES = {
    "PYTHON101": 250,
    "AI202": 400,
    "DBMS110": 300,
}

ALLOWED_OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


# Tool 1: Search library policy documents
@tool
def search_library_policy(query: str) -> str:
    """Search library documents about borrowing, fines, renewals, and hours."""

    documents = store.similarity_search(query, k=3)

    if not documents:
        return "No matching library policy documents were found."

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"{doc.page_content}"
        for doc in documents
    )


# Tool 2: Look up a sample course-book fee
@tool
def lookup_course_book_fee(course_code: str) -> str:
    """Look up a sample fee using PYTHON101, AI202, or DBMS110."""

    code = course_code.strip().upper()
    fee = COURSE_BOOK_FEES.get(code)

    if fee is None:
        return f"Unknown sample course code: {code}"

    return f"The sample book fee for {code} is Rs. {fee}."


# Tool 3: Safely calculate simple arithmetic
@tool
def calculator(expression: str) -> str:
    """Calculate arithmetic expressions using numbers and +, -, *, or /."""

    def evaluate(node):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return node.value

        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in ALLOWED_OPERATIONS
        ):
            return ALLOWED_OPERATIONS[type(node.op)](
                evaluate(node.left),
                evaluate(node.right),
            )

        raise ValueError(
            "Only numbers and +, -, *, / operations are allowed."
        )

    try:
        tree = ast.parse(expression, mode="eval")
        return str(evaluate(tree.body))
    except Exception as error:
        return f"Calculation error: {error}"


# Give the tools to the language model
tools = [
    search_library_policy,
    lookup_course_book_fee,
    calculator,
]

model = get_model().bind_tools(tools)


SYSTEM_PROMPT = """
You are the Smart Library Assistant for a college.

Rules:
1. Use search_library_policy for questions about library rules.
2. Use lookup_course_book_fee for the sample course-book fee codes.
3. Use calculator for arithmetic.
4. Use tools when they are helpful.
5. Cite the source filename when policy information provides one.
6. If the library documents do not support an answer, say you do not know.
7. Do not invent library policies or real fees.
8. Keep answers clear and concise.
"""


# Agent node: decide whether to answer or call a tool
def assistant_node(state: MessagesState):
    response = model.invoke(
        [("system", SYSTEM_PROMPT)] + state["messages"]
    )
    return {"messages": [response]}


# Construct the LangGraph agent
builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")

builder.add_conditional_edges(
    "assistant",
    tools_condition,
)

builder.add_edge("tools", "assistant")

# Store conversation history in memory, separated by thread ID
memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)


def ask(question: str, thread_id: str = "student-1"):
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 10,
    }

    result = graph.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config,
    )

    answer = result["messages"][-1].content

    print(f"\nQuestion: {question}")
    print(f"Answer: {answer}")

    return answer


if __name__ == "__main__":
    print("Smart Library Assistant — Agentic RAG")
    print("Type 'exit' to stop.")

    thread_id = "student-1"

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            ask(question, thread_id)
        except Exception as error:
            print(f"Something went wrong: {error}")