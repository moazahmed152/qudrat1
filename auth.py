# auth.py
import json
from telegram import Update
from telegram.ext import ContextTypes
from config import DEFAULT_VALID_KEYS, STUDENTS_FILE
from utils.database import load_students, save_students
from utils.keyboards import main_menu_keyboard


# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    students = load_students()

    # لو مسجل قبل كده
    if str(user.id) in students:
        await update.message.reply_text(
            f"👋 أهلاً {user.first_name}!\nانت مسجل بالفعل.",
            reply_markup=main_menu_keyboard()
        )
        return

    # أول مرة يدخل
    await update.message.reply_text("🔑 من فضلك أدخل الـ Product Key:")
    context.user_data["awaiting_key"] = True


# أي رسالة نصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    students = load_students()
    text = update.message.text.strip()

    # لو مستني المفتاح
    if context.user_data.get("awaiting_key"):
        if text in DEFAULT_VALID_KEYS:
            # نسجل الطالب
            students[str(user.id)] = {
                "id": user.id,
                "name": user.full_name,
                "key": text,
                "progress": {}
            }
            save_students(students)

            context.user_data["awaiting_key"] = False

            await update.message.reply_text(
                f"✅ تم تسجيل المفتاح بنجاح يا {user.first_name}!",
                reply_markup=main_menu_keyboard()
            )
        else:
            await update.message.reply_text("❌ المفتاح غير صحيح. حاول تاني.")
    else:
        await update.message.reply_text("❓ استخدم /start للبدء.")
