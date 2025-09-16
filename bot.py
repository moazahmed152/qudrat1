from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from auth import start_command, handle_product_key
from handlers.foundation_handler import handle_callback as foundation_callback
from handlers.training_handler import handle_callback as training_callback
from handlers.homework_handler import handle_homework_callback
from utils.database import load_students

async def stats(update, context):
    students = load_students()
    user_id = str(update.message.from_user.id)
    student = students.get(user_id, {})
    progress = student.get("progress", {})
    await update.message.reply_text(f"📊 تقدمك الحالي: {len(progress)} خطوة مكتملة.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_key))
    app.add_handler(CallbackQueryHandler(foundation_callback, pattern="^(foundation|lesson:|rule:|example:|got:|redo:)"))
    app.add_handler(CallbackQueryHandler(training_callback, pattern="^(training|tq:)"))
    app.add_handler(CallbackQueryHandler(handle_homework_callback, pattern="^(homework:|hans:)"))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
