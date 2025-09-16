import json
import os
from config import STUDENTS_FILE


def _load():
    if not os.path.exists(STUDENTS_FILE):
        return {}
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_progress(user_id, key, value):
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {}
    data[uid][key] = value
    _save(data)


def get_progress(user_id):
    data = _load()
    return data.get(str(user_id), {})
