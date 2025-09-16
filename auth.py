from telegram import Update
from telegram.ext import ContextTypes
from config import DEFAULT_VALID_KEYS
from utils.database import save_student, load_students
from utils.keyboards import main_menu_keyboard

# أمر البداية
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    students = load_students()
    user_id = str(update.message.from_user.id)

    # لو الطالب موجود قبل كده ومفتاحه صحيح → يفتح المنيو
    if user_id in students and students[user_id].get("key_valid", False):
        await update.message.reply_text(
            f"👋 أهلاً {students[user_id].get('name', 'طالب')}, رجعت من جديد.",
            reply_markup=main_menu_keyboard()
        )
    else:
        # أول مرة → يطلب المفتاح
        await update.message.reply_text("🔑 من فضلك أدخل مفتاح الدخول:")

# التحقق من المفتاح
async def handle_product_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    students = load_students()

    # لو الطالب عنده مفتاح صحيح قبل كده → يخليه يدخل مباشرة
    if user_id in students and students[user_id].get("key_valid", False):
        await update.message.reply_text(
            "✅ أنت مسجل بالفعل. تقدر تدخل على القايمة.",
            reply_markup=main_menu_keyboard()
        )
        return

    # المفتاح اللي كتبه الطالب
    key = update.message.text.strip()

    # التحقق
    if key in DEFAULT_VALID_KEYS:
        save_student(user_id, {
            "name": update.message.from_user.full_name,
            "key_valid": True,
            "progress": {}
        })
        await update.message.reply_text(
            "✅ مفتاح صحيح! أهلاً بيك.",
            reply_markup=main_menu_keyboard()
        )
    else:
        await update.message.reply_text("❌ مفتاح غير صحيح، حاول تاني.")
