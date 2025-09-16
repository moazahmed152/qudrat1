from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import t_question_keyboard
from utils.database import save_progress

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "training":
        await query.edit_message_text("📝 التدريب لسه تحت الإنشاء (هنضيف أسئلة هنا).")
        return

    if data.startswith("tq:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)

        qs = context.user_data.get("t_questions", [])
        idx = context.user_data.get("t_index", 0)

        if idx >= len(qs):
            await query.edit_message_text("✔️ خلصت التدريب.")
            return

        q = qs[idx]
        correct = (opt_idx == q["answer"])

        if correct:
            context.user_data["t_score"] = context.user_data.get("t_score", 0) + 1
            await query.edit_message_text("✅ إجابة صحيحة!")
        else:
            await query.edit_message_text(f"❌ إجابة خاطئة.\n📺 الشرح: {q.get('explanation')}")

        idx += 1
        context.user_data["t_index"] = idx

        if idx < len(qs):
            nq = qs[idx]
            await query.message.reply_text(f"📝 {nq['q']}", reply_markup=t_question_keyboard(nq["id"], nq["options"]))
        else:
            score = context.user_data.get("t_score", 0)
            total = len(qs)
            pct = (score / total) * 100
            save_progress(user_id, "training:last_result", f"{score}/{total}")

            if pct >= 80:
                level_msg = "🎉 ممتاز! متفوق جدًا"
            elif pct >= 50:
                level_msg = "👍 جيد، محتاج مراجعة بسيطة"
            else:
                level_msg = "⚠️ محتاج تذاكر أكتر"

            await query.message.reply_text(f"📊 خلصت التدريب!\nنتيجتك: {score}/{total}\n{level_msg}")
