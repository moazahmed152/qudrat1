from config import TOTAL_LESSONS_COUNT
from utils.database import get_progress

def calculate_progress(user_id: int) -> int:
    progress_map = get_progress(user_id) or {}
    completed = sum(1 for v in progress_map.values() if (str(v).strip().lower() in {"done","true","1"} or v))
    total = TOTAL_LESSONS_COUNT or 1
    pct = int((completed / total) * 100)
    return max(0, min(100, pct))

def progress_bar(pct: int, width: int = 20) -> str:
    filled = int(width * pct / 100)
    return "█" * filled + "░" * (width - filled)
