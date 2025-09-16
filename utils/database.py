# utils/database.py
import json
from datetime import datetime
from pathlib import Path
from threading import Lock

DATA_FILE = "data/students.json"
_lock = Lock()

def _ensure_file():
    p = Path(DATA_FILE)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"data": {}, "valid_keys": []}, f, ensure_ascii=False, indent=2)

def load_students():
    _ensure_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_students(obj):
    _ensure_file()
    tmp = DATA_FILE + ".tmp"
    with _lock:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        Path(tmp).replace(DATA_FILE)

def update_last_active(user_id):
    students = load_students()
    sid = str(user_id)
    if sid in students["data"]:
        students["data"][sid]["last_active"] = datetime.utcnow().isoformat()
        save_students(students)

def save_progress(user_id, key, value="done"):
    students = load_students()
    sid = str(user_id)
    if sid not in students["data"]:
        students["data"][sid] = {"progress": {}, "badges": [], "product_key": None}
    progress = students["data"][sid].get("progress", {})
    progress[key] = value
    students["data"][sid]["progress"] = progress
    save_students(students)

def get_progress(user_id):
    students = load_students()
    return students["data"].get(str(user_id), {}).get("progress", {})

def get_badges(user_id):
    students = load_students()
    return students["data"].get(str(user_id), {}).get("badges", [])

def add_badge(user_id, badge_key):
    students = load_students()
    sid = str(user_id)
    if sid not in students["data"]:
        students["data"][sid] = {"progress": {}, "badges": [], "product_key": None}
    badges = students["data"][sid].get("badges", [])
    if badge_key not in badges:
        badges.append(badge_key)
        students["data"][sid]["badges"] = badges
        save_students(students)
