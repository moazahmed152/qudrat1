import os

# توكن البوت (حطه على Railway باسم Token أو TOKEN)
TELEGRAM_BOT_TOKEN = os.getenv("Token") or os.getenv("TOKEN")

# Product Keys (من ENV لو موجودة بصيغة ABC123,XYZ789 وإلا افتراضي)
DEFAULT_VALID_KEYS = [k.strip() for k in os.getenv("VALID_KEYS", "ABC123,XYZ789").split(",") if k.strip()]

# رسالة التذكير اليومية (لو هتضيف Reminder بعدين)
REMINDER_MESSAGE = "📚 متنساش تكمل مذاكرتك النهارده!"

# ملفات بيانات
STUDENTS_FILE = "data/students.json"   # قاعدة بيانات الطلبة (JSON)

# العدد الكلي للعناصر لحساب التقدم (عدّل حسب حجم المحتوى)
TOTAL_LESSONS_COUNT = 50
