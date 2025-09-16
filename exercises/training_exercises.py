# exercises/training_exercises.py
import importlib

def get_training_chapter(chapter_id):
    """
    جلب بيانات الباب التدريبي بناءً على chapter_id
    """
    try:
        mod = importlib.import_module(f"training.{chapter_id}")
        return getattr(mod, "TRAINING_CHAPTER", None)
    except Exception:
        return None

def get_training_lesson(chapter_id, lesson_id):
    """
    جلب بيانات الدرس بناءً على lesson_id داخل باب معين
    """
    chapter = get_training_chapter(chapter_id)
    if not chapter:
        return None
    for lesson in chapter.get("lessons", []):
        if lesson.get("lesson_id") == lesson_id:
            return lesson
    return None

def get_training_rule(chapter_id, lesson_id, rule_id):
    """
    جلب قاعدة معينة داخل درس محدد
    """
    lesson = get_training_lesson(chapter_id, lesson_id)
    if not lesson:
        return None
    for rule in lesson.get("rules", []):
        if rule.get("rule_id") == rule_id:
            return rule
    return None

def get_training_questions(chapter_id, lesson_id, rule_id):
    """
    جلب جميع أسئلة قاعدة معينة
    """
    rule = get_training_rule(chapter_id, lesson_id, rule_id)
    if not rule:
        return []
    return rule.get("questions", [])
