from utils.database import load_students
from config import TOTAL_LESSONS_COUNT

def calculate_progress(user_id):
    students = load_students()
    student = students.get(str(user_id), {})
    progress = student.get("progress", {})
    done = len([v for v in progress.values() if v == "done"])
    pct = int((done / TOTAL_LESSONS_COUNT) * 100) if TOTAL_LESSONS_COUNT > 0 else 0
    return pct
