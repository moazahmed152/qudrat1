# bot.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from auth import start_command, handle_message
from handlers.foundation_handler import handle_callback as foundation_callback
from handlers.training_handler import handle_callback as training_callback
from handlers.homework_handler import handle_homework_callback   # 👈 ضفت الاستيراد الصح

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start_command))

    # Foundation (تأسيس)
    app.add_handler(CallbackQueryHandler(foundation_callback, pattern="^(foundation:|example:|rule:)"))

    # Training (تدريب)
    app.add_handler(CallbackQueryHandler(training_callback, pattern="^(training:|tq:|tans:)"))

    # Homework (الواجب) 👈 هنا بدلنا الاسم الصح
    app.add_handler(CallbackQueryHandler(handle_homework_callback, pattern="^(homework:|hans:)"))

    # أي رسالة نصية (مفتاح المنتج أو حاجة تانية)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
