from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_progress


async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    progress = get_progress(user_id) or {}

    total_done = sum(1 for v in progress.values() if v == "done")
    total_items = 50  # عدّل حسب عدد الدروس/الأسئلة
    pct = int((total_done / total_items) * 100) if total_items else 0

    await update.message.reply_text(
        f"📊 تقدمك الحالي:\n"
        f"✅ منجز: {total_done}/{total_items}\n"
        f"📈 النسبة: {pct}%"
    )
