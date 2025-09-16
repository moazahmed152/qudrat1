import json
from config import STUDENTS_FILE

def load_students():
    try:
        with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_students(students):
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

def save_student(user_id, data):
    students = load_students()
    students[str(user_id)] = {**students.get(str(user_id), {}), **data}
    save_students(students)

def save_progress(user_id, key, value):
    students = load_students()
    student = students.get(str(user_id), {"progress": {}})
    progress = student.get("progress", {})
    progress[key] = value
    student["progress"] = progress
    students[str(user_id)] = student
    save_students(students)
