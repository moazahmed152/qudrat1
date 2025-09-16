import os

# توكن البوت من Railway (Environment Variable)
TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")

# Product Keys
DEFAULT_VALID_KEYS = ["a", "XYZ789"]

# رسالة التذكير
REMINDER_MESSAGE = "📚 متنساش تكمل مذاكرتك النهارده!"

# المسارات
STUDENTS_FILE = "data/students.json"
CONTENT_DIR = "foundation"
TRAINING_DIR = "training"

# عدد الدروس الكلي
TOTAL_LESSONS_COUNT = 50
