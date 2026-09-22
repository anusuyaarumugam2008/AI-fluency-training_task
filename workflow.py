from tools import get_attendance

def workflow(question):
    question = question.lower()

    if "alice" in question:
        return f"Alice attendance is {get_attendance('Alice')}%"

    elif "bob" in question:
        return f"Bob attendance is {get_attendance('Bob')}%"

    elif "charlie" in question:
        return f"Charlie attendance is {get_attendance('Charlie')}%"

    return "Student not found"


if __name__ == "__main__":
    print(workflow("What is Alice attendance?"))
    print(workflow("What is Bob attendance?"))
    print(workflow("What is Charlie attendance?"))