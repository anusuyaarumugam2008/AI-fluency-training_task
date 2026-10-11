
"""LangGraph workflow for routing library questions."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# Define the information passed between graph nodes
class LibraryState(TypedDict):
    question: str
    desk: str
    reply: str


# Node 1: Decide which desk should handle the question
def classify_question(state: LibraryState):
    question = state["question"].lower()

    if any(word in question for word in (
        "fine", "late", "overdue", "renew"
    )):
        desk = "circulation"

    elif any(word in question for word in (
        "borrow", "return", "book", "loan"
    )):
        desk = "borrowing"

    elif any(word in question for word in (
        "open", "hours", "hour", "time", "saturday", "sunday"
    )):
        desk = "hours"

    else:
        desk = "general"

    return {"desk": desk}


# Node 2: Handle a circulation question
def circulation_desk(state: LibraryState):
    return {
        "reply": (
            "Please check fines_and_renewals.md or contact "
            "the circulation desk."
        )
    }


# Node 3: Handle a borrowing question
def borrowing_desk(state: LibraryState):
    return {
        "reply": (
            "Please check borrowing_rules.md or ask "
            "the circulation desk."
        )
    }


# Node 4: Handle an opening-hours question
def hours_desk(state: LibraryState):
    return {
        "reply": (
            "Please check library_hours.md for the current "
            "opening-hours policy."
        )
    }


# Node 5: Handle other questions
def general_desk(state: LibraryState):
    return {
        "reply": "Please ask the librarian for further assistance."
    }


# Choose the next node based on the classification
def choose_desk(state: LibraryState):
    return state["desk"]


# Build the LangGraph workflow
builder = StateGraph(LibraryState)

builder.add_node("classify", classify_question)
builder.add_node("circulation", circulation_desk)
builder.add_node("borrowing", borrowing_desk)
builder.add_node("hours", hours_desk)
builder.add_node("general", general_desk)

builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    choose_desk,
    {
        "circulation": "circulation",
        "borrowing": "borrowing",
        "hours": "hours",
        "general": "general",
    },
)

builder.add_edge("circulation", END)
builder.add_edge("borrowing", END)
builder.add_edge("hours", END)
builder.add_edge("general", END)

graph = builder.compile()


if __name__ == "__main__":
    questions = [
        "What is the late-return fine?",
        "How long can I borrow a book?",
        "What time does the library open on Saturday?",
        "Can you help me find a research topic?",
    ]

    print("Smart Library Assistant — LangGraph")
    
    for question in questions:
        result = graph.invoke({
            "question": question,
            "desk": "",
            "reply": "",
        })

        print(f"\nQuestion: {question}")
        print(f"Assigned desk: {result['desk']}")
        print(f"Reply: {result['reply']}")

    print("\nWorkflow diagram:")
    print(graph.get_graph().draw_mermaid())