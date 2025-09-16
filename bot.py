# bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, valid_keys , REMINDER_MESSAGE
from utils.database import load_students, save_students, update_last_active
from utils.keyboards import main_menu_reply
import handlers.foundation_handler as fh
import handlers.training_handler as th
import handlers.homework_handler as hh
from utils.database import save_progress
from utils.progress import calculate_progress

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    students = load_students()
    sid = str(user.id)
    if sid not in students.get("data", {}):
        # ask for product key (simple flow)
        await update.message.reply_text("🔑 ادخل Product Key (مطلوب مرة واحدة فقط):")
        context.user_data["awaiting_key"] = True
        return
    # registered -> show main menu
    await update.message.reply_text("أهلاً بك! اختر من القائمة:", reply_markup=main_menu_reply())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sid = str(user.id)
    students = load_students()

    # if awaiting key
    if context.user_data.get("awaiting_key"):
        key = update.message.text.strip()
        if key in students.get("valid_keys", []):
            # register user
            students["data"].setdefault(sid, {})
            students["data"][sid]["product_key"] = key
            students["data"][sid].setdefault("progress", {})
            students["data"][sid].setdefault("badges", [])
            save_students(students)
            context.user_data["awaiting_key"] = False
            await update.message.reply_text("✅ تم الربط! اهلاً بك 🎉", reply_markup=main_menu_reply())
            return
        else:
            await update.message.reply_text("❌ المفتاح غير صحيح. جرب تاني:")
            return

    # handle main menu texts
    text = update.message.text
    if text == "📘 تأسيس":
        # show chapters from foundation module files
        # collect chapters by scanning folder
        import os, importlib
        chapters = []
        for fname in os.listdir("foundation"):
            if fname.endswith(".py") and not fname.startswith("__"):
                modname = fname[:-3]
                mod = importlib.import_module(f"foundation.{modname}")
                ch = getattr(mod, "CHAPTER", None)
                if ch:
                    chapters.append({"chapter_id": ch["chapter_id"], "chapter_name": ch["chapter_name"]})
        # send inline keyboard via handlers' keyboard
        from utils.keyboards import chapters_keyboard
        await update.message.reply_text("اختر الباب:", reply_markup=chapters_keyboard(chapters))
        return

    if text == "📗 تدريب":
        # show training chapters analogously
        import os, importlib
        chapters = []
        for fname in os.listdir("training"):
            if fname.endswith(".py") and not fname.startswith("__"):
                modname = fname[:-3]
                mod = importlib.import_module(f"training.{modname}")
                ch = getattr(mod, "TRAINING_CHAPTER", None)
                if ch:
                    chapters.append({"chapter_id": ch["chapter_id"], "chapter_name": ch["chapter_name"]})
        from utils.keyboards import chapters_keyboard
        await update.message.reply_text("اختر باب التدريب:", reply_markup=chapters_keyboard(chapters))
        return

    if text == "/stats" or text == "📊 إحصائياتي":
        progress = calculate_progress(user.id)
        await update.message.reply_text(f"📊 تقدمك الحالي: {progress}%")
        return

    if text == "🔀 سؤال عشوائي":
        # choose random example from content (simple approach: pick from foundation/chapter1)
        import random, importlib
        try:
            mod = importlib.import_module("foundation.chapter1")
            ch = getattr(mod, "CHAPTER")
            lesson = random.choice(ch["lessons"])
            rule = random.choice(lesson["rules"])
            ex_idx = random.randint(1, len(rule["examples_videos"]))
            url = rule["examples_videos"][ex_idx-1]
            await update.message.reply_text(f"🔀 سؤال عشوائي:\n{url}")
            return
        except Exception:
            await update.message.reply_text("لا يمكن جلب سؤال عشوائي الآن.")
            return

    await update.message.reply_text("اختيار غير معروف، استخدم القائمة.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("stats", lambda u,c: c.application.create_task(start_cmd(u,c))))
    # Callback handlers for foundation / examples / homework / training
    app.add_handler(CallbackQueryHandler(fh.handle_callback, pattern="^(chapter:|lesson:|rule:|explain:|example:|got:example:|redo:example:|homework:).+"))
    app.add_handler(CallbackQueryHandler(th.handle_training_callback, pattern="^(train:|tans:).+"))
    app.add_handler(CallbackQueryHandler(hh.start_homework, pattern="^homework:.+"))
    app.add_handler(CallbackQueryHandler(hh.handle_hw_answer, pattern="^hwans:.+"))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
