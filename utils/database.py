import json
from pathlib import Path
from config import STUDENTS_FILE

def _ensure():
    p = Path(STUDENTS_FILE)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"data": {}}, f, ensure_ascii=False, indent=2)

def load_students():
    _ensure()
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_students(obj):
    _ensure()
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def ensure_user(user_id: int):
    s = load_students()
    sid = str(user_id)
    s["data"].setdefault(sid, {"progress": {}, "badges": [], "product_key": None})
    save_students(s)

def save_progress(user_id: int, key: str, value="done"):
    s = load_students()
    sid = str(user_id)
    s["data"].setdefault(sid, {"progress": {}, "badges": [], "product_key": None})
    s["data"][sid]["progress"][key] = value
    save_students(s)

def get_progress(user_id: int):
    return load_students()["data"].get(str(user_id), {}).get("progress", {})
