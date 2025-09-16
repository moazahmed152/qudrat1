# utils/progress.py

from config import TOTAL_LESSONS_COUNT

def calculate_progress(completed_lessons: int) -> float:
    """
    يحسب نسبة التقدم للطالب
    :param completed_lessons: عدد الدروس اللي الطالب خلصها
    :return: نسبة التقدم %
    """
    if TOTAL_LESSONS_COUNT == 0:
        return 0.0
    progress = (completed_lessons / TOTAL_LESSONS_COUNT) * 100
    return round(progress, 2)
