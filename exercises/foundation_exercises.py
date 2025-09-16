# exercises/foundation_exercises.py
from foundation.chapter1 import CHAPTER

def get_homework_for_rule(chapter_id, lesson_id, rule_id):
    # يرَجع قائمة الأسئلة للواجب
    if CHAPTER["chapter_id"] != chapter_id:
        return []
    for lesson in CHAPTER["lessons"]:
        if lesson["lesson_id"] == lesson_id:
            for rule in lesson["rules"]:
                if rule["rule_id"] == rule_id:
                    return rule.get("homework", [])
    return []
