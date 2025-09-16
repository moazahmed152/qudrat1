import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN
from handlers.foundation_handler import handle_callback as foundation_callback
from handlers.homework_handler import handle_homework_callback
from handlers.training_handler import handle_training_callback
from handlers.stats_handler import handle_stats
from utils.keyboards import main_menu_keyboard
from auth import check_user_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# /start
async def start(update, context):
    user_id = update.effective_user.id
    if not check_user_key(user_id):
        await update.message.reply_text("🔑 من فضلك أدخل مفتاح الدخول أولاً:")
        return

    await update.message.reply_text(
        "👋 أهلاً بيك!\nاختر من القايمة:",
        reply_markup=main_menu_keyboard()
    )


# ردود النصوص
async def handle_message(update, context):
    text = update.message.text.strip()

    # لو المستخدم دخل مفتاح المنتج
    user_id = update.effective_user.id
    if not check_user_key(user_id, text):
        return

    if text == "🏠 القائمة الرئيسية":
        await update.message.reply_text("📌 رجعتك للقائمة الرئيسية", reply_markup=main_menu_keyboard())
        return

    await update.message.reply_text("⚠️ الاختيار غير صحيح.")


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", handle_stats))
    app.add_handler(CallbackQueryHandler(foundation_callback, pattern="^(chapter:|lesson:|rule:|example:|got:|redo:|explain:)"))
    app.add_handler(CallbackQueryHandler(homework_handler, pattern="^(homework:|hans:)"))
    app.add_handler(CallbackQueryHandler(training_handler, pattern="^(training:|hans:)"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
