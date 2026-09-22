from config import ATTENDANCE

def get_attendance(name):
    return ATTENDANCE.get(name, "Not Found")