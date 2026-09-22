
from tools import get_attendance
def agent(question):
    if "alice" in question.lower():
        return f"Alice attendance is {get_attendance('Alice')}%"

    elif "bob" in question.lower():
        return f"Bob attendance is {get_attendance('Bob')}%"

    elif "charlie" in question.lower():
        return f"Charlie attendance is {get_attendance('Charlie')}%"

    return "Student not found"

if __name__ == "__main__":
    print(agent("What is Alice attendance?"))
    print(agent("What is Bob attendance?"))
    print(agent("What is Charlie attendance?"))