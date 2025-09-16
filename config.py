# config.py
import os

# توكن البوت من Railway (Environment Variable)
TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")  # خلي بالك من الحروف

# Product Keys المسموح بيها (من Environment Variables)
# لو مفيش متغير في Railway، هيفضل ياخد القيم الافتراضية دي
DEFAULT_VALID_KEYS = os.getenv("VALID_KEYS", "ABC123,XYZ789").split(",")

# رسالة التذكير اليومية
REMINDER_MESSAGE = "📚 متنساش تكمل مذاكرتك النهارده!"

# Paths
STUDENTS_FILE = "data/students.json"
CONTENT_DIR = "foundation"
TRAINING_DIR = "training"

# إعدادات عامة
TOTAL_LESSONS_COUNT = 50  # تستخدم لحساب النسبة؛ عدّل لو عايز
