
# config.py
import os

TOKEN = os.getenv("Token")  # لازم تضيف BOT_TOKEN في Railway Variables
BUNNY_API_KEY = os.getenv("BUNNY_API_KEY")


# مفاتيح جاهزة للتجربة - استخدم ملف data/students.json.valid_keys لاحقًا أو DB
DEFAULT_VALID_KEYS = ["KEY123", "KEY456", "KEY789"]

# رسالة التذكير اليومية
REMINDER_MESSAGE = "👋 افتكر تكمل دروسك النهاردة! يلا نذاكر 💪"

# Paths
STUDENTS_FILE = "data/students.json"
CONTENT_DIR = "foundation"
TRAINING_DIR = "training"

# إعدادات عامة
TOTAL_LESSONS_COUNT = 50  # تستخدم لحساب النسبة؛ عدّل لو عايز
