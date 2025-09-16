import json
import os
from config import STUDENTS_FILE, DEFAULT_VALID_KEYS


def _load_students():
    """تحميل بيانات الطلبة من ملف JSON"""
    if not os.path.exists(STUDENTS_FILE):
        return {}
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_students(data):
    """حفظ بيانات الطلبة في ملف JSON"""
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_user_key(user_id, key=None):
    """
    التحقق من الـ Product Key للطالب.
    - لو الطالب مسجل قبل كده، يرجّع True.
    - لو دخل مفتاح جديد صحيح، يتخزن له مرة واحدة ويرجّع True.
    - لو دخل مفتاح غلط، يرجّع False.
    """
    data = _load_students()
    uid = str(user_id)

    # لو الطالب عنده مفتاح مسجل قبل كده
    if uid in data and data[uid].get("key"):
        return True

    # لو المستخدم دخل مفتاح جديد
    if key:
        if key in DEFAULT_VALID_KEYS:
            data[uid] = {"key": key}
            _save_students(data)
            return True
        else:
            return False

    # لو مفيش حاجة
    return False
