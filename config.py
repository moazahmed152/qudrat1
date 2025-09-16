# config.py
import os

# توكن البوت من Railway (Environment Variable)
TELEGRAM_BOT_TOKEN = os.getenv("Token")  # خلي بالك من الحروف

# Product Keys المسموح بيها
DEFAULT_VALID_KEYS = ["a", "b"]

# رسالة التذكير اليومية
REMINDER_MESSAGE = "📚 متنساش تكمل مذاكرتك النهارده!"

# Paths
STUDENTS_FILE = "data/students.json"
CONTENT_DIR = "foundation"
TRAINING_DIR = "training"

# إعدادات عامة
TOTAL_LESSONS_COUNT = 50  # تستخدم لحساب النسبة؛ عدّل لو عايز
