from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN, DEFAULT_VALID_KEYS
from utils.database import ensure_user, load_students, save_students
from utils.keyboards import main_menu_reply, chapters_keyboard, t_chapters_keyboard
from handlers.foundation_handler import handle_callback as foundation_callback
from handlers.training_handler import handle_training_callback
from handlers.homework_handler import handle_homework_callback
from utils.progress import calculate_progress, progress_bar
import importlib, os

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sid = str(user.id)
    ensure_user(user.id)
    students = load_students()

    # أول مرة → اطلب Product Key
    if not students["data"].get(sid, {}).get("product_key"):
        context.user_data["awaiting_key"] = True
        await update.message.reply_text("🔑 ادخل الـ Product Key (مرّة واحدة فقط):")
        return

    await update.message.reply_text("👋 أهلاً بيك! اختر من القائمة:", reply_markup=main_menu_reply())

# /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pct = calculate_progress(update.effective_user.id)
    bar = progress_bar(pct)
    await update.message.reply_text(f"📊 تقدمك: {pct}%\n{bar}")

# نصوص عامة + إدخال الـ Key + قوائم رئيسية
async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    user = update.effective_user
    sid = str(user.id)

    # مرحلة إدخال الـ Key
    if context.user_data.get("awaiting_key"):
        key = text
        if key in DEFAULT_VALID_KEYS:
            students = load_students()
            students["data"].setdefault(sid, {"progress": {}, "badges": [], "product_key": None})
            students["data"][sid]["product_key"] = key
            save_students(students)
            context.user_data["awaiting_key"] = False
            await update.message.reply_text("✅ تم التسجيل بنجاح!", reply_markup=main_menu_reply())
        else:
            await update.message.reply_text("❌ المفتاح غير صحيح. جرّب تاني:")
        return

    # القايمة الرئيسية
    if text == "📘 تأسيس":
        chapters = []
        for fname in os.listdir("foundation"):
            if fname.endswith(".py") and not fname.startswith("__"):
                mod = importlib.import_module(f"foundation.{fname[:-3]}")
                ch = getattr(mod, "CHAPTER", None)
                if ch:
                    chapters.append({"chapter_id": ch["chapter_id"], "chapter_name": ch["chapter_name"]})
        if not chapters:
            await update.message.reply_text("لسه مفيش أبواب تأسيس مضافة.")
            return
        await update.message.reply_text("اختر الباب:", reply_markup=chapters_keyboard(chapters))
        return

    if text == "📗 تدريب":
        t_chs = []
        for fname in os.listdir("training"):
            if fname.endswith(".py") and not fname.startswith("__"):
                mod = importlib.import_module(f"training.{fname[:-3]}")
                ch = getattr(mod, "CHAPTER", None)
                if ch:
                    t_chs.append({"chapter_id": ch["chapter_id"], "chapter_name": ch["chapter_name"]})
        if not t_chs:
            await update.message.reply_text("لسه مفيش أبواب تدريب مضافة.")
            return
        await update.message.reply_text("اختر الباب التدريبي:", reply_markup=t_chapters_keyboard(t_chs))
        return

    if text == "📊 إحصائياتي" or text == "/stats":
        await stats(update, context)
        return

    # fallback → رجّع القايمة
    await update.message.reply_text("استخدم القايمة لو سمحت:", reply_markup=main_menu_reply())

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    # تأسيس (شرح/أمثلة/واجب)
    app.add_handler(CallbackQueryHandler(foundation_callback, pattern="^(chapter:|lesson:|rule:|explain:|example:|got:example:|redo:example:)"))
    # تدريب (أسئلة تدريب)
    app.add_handler(CallbackQueryHandler(handle_training_callback, pattern="^(tchapter:|tlesson:|trule:|tans:)"))
    # واجب
    app.add_handler(CallbackQueryHandler(handle_homework_callback, pattern="^(homework:|hans:)"))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
