# utils/database.py
import json
import os
from config import STUDENTS_FILE


def load_students():
    """تحميل بيانات الطلاب من ملف JSON"""
    if not os.path.exists(STUDENTS_FILE):
        return {}
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_students(students: dict):
    """حفظ بيانات الطلاب في ملف JSON"""
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


def save_progress(user_id: int, key: str, value: str):
    """تحديث تقدم الطالب (progress)"""
    students = load_students()
    user_id = str(user_id)

    if user_id not in students:
        students[user_id] = {"progress": {}}

    if "progress" not in students[user_id]:
        students[user_id]["progress"] = {}

    students[user_id]["progress"][key] = value
    save_students(students)


def get_progress(user_id: int, key: str):
    """قراءة تقدم الطالب (progress)"""
    students = load_students()
    user_id = str(user_id)

    if user_id not in students:
        return None

    return students[user_id].get("progress", {}).get(key)
