# exercises/training_exercises.py
from training.chapter1 import TRAINING_CHAPTER

def get_training_questions(chapter_id, lesson_id, rule_id):
    if TRAINING_CHAPTER["chapter_id"] != chapter_id:
        return []
    for lesson in TRAINING_CHAPTER["lessons"]:
        if lesson["lesson_id"] == lesson_id:
            for rule in lesson["rules"]:
                if rule["rule_id"] == rule_id:
                    return rule.get("questions", [])
    return []
