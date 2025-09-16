# exercises/training_exercises.py
import importlib

def get_training_chapter(chapter_id):
    try:
        mod = importlib.import_module(f"training.{chapter_id}")
        return getattr(mod, "TRAINING_CHAPTER", None)
    except Exception:
        return None

def get_training_lesson(chapter_id, lesson_id):
    chapter = get_training_chapter(chapter_id)
    for lesson in chapter["lessons"]:
        if lesson["lesson_id"] == lesson_id:
            return lesson
    return None

def get_training_rule(chapter_id, lesson_id, rule_id):
    lesson = get_training_lesson(chapter_id, lesson_id)
    for rule in lesson["rules"]:
        if rule["rule_id"] == rule_id:
            return rule
    return None

def get_training_questions(chapter_id, lesson_id, rule_id):
    rule = get_training_rule(chapter_id, lesson_id, rule_id)
    if not rule:
        return []
    return rule.get("questions", [])
