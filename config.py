
# config.py
import os

# توكن البوت من Railway (Environment Variable)
TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")

# Product Keys المسموح بيها
DEFAULT_VALID_KEYS = ["ABC123", "XYZ789"]

# رسالة التذكير اليومية
REMINDER_MESSAGE = "📚 متنساش تكمل مذاكرتك النهارده!"





# Paths
STUDENTS_FILE = "data/students.json"
CONTENT_DIR = "foundation"
TRAINING_DIR = "training"

# إعدادات عامة
TOTAL_LESSONS_COUNT = 50  # تستخدم لحساب النسبة؛ عدّل لو عايز
