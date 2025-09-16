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
    """حفظ تقدم المستخدم (مفتاح = value)."""
    s = load_students()
    sid = str(user_id)
    s["data"].setdefault(sid, {"progress": {}, "badges": [], "product_key": None})

    if key.startswith("example:"):
        # لو المفتاح مثال -> نحفظه في لستة
        done = set(s["data"][sid]["progress"].get("completed_examples", []))
        done.add(key)
        s["data"][sid]["progress"]["completed_examples"] = list(done)
    else:
        s["data"][sid]["progress"][key] = value

    save_students(s)

def get_progress(user_id: int):
    """ترجع progress بتاع المستخدم."""
    return load_students()["data"].get(str(user_id), {}).get("progress", {})

def load_progress(user_id: int):
    """ترجع كل بيانات المستخدم (progress + badges + product_key)."""
    s = load_students()
    return s["data"].get(str(user_id), {})
