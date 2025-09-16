from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import t_question_keyboard
from utils.database import save_progress


async def handle_homework_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # بدء الواجب
    if data.startswith("homework:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)

        questions = rule.get("homework", [])
        if not questions:
            await query.edit_message_text("⚠️ لا يوجد واجب لهذه القاعدة حالياً.")
            return

        # حفظ حالة الطالب
        context.user_data["h_questions"] = questions
        context.user_data["h_index"] = 0
        context.user_data["h_score"] = 0

        # أول سؤال
        q = questions[0]
        await query.edit_message_text(
            f"📝 {q['q']}",
            reply_markup=t_question_keyboard(q["id"], q["options"])
        )
        return

    # التعامل مع الإجابة
    if data.startswith("hans:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)

        idx = context.user_data.get("h_index", 0)
        qs = context.user_data.get("h_questions", [])
        if idx >= len(qs):
            await query.edit_message_text("انتهى الواجب.")
            return

        q = qs[idx]
        correct = (opt_idx == q["answer"])

        if correct:
            context.user_data["h_score"] = context.user_data.get("h_score", 0) + 1
            await query.edit_message_text("✅ إجابة صحيحة!")
        else:
            await query.edit_message_text(
                f"❌ إجابة خاطئة.\n📺 الشرح: {q.get('explanation')}"
            )

        # التالي
        idx += 1
        context.user_data["h_index"] = idx

        if idx < len(qs):
            nq = qs[idx]
            await query.message.reply_text(
                f"📝 {nq['q']}",
                reply_markup=t_question_keyboard(nq["id"], nq["options"])
            )
        else:
            # نهاية الواجب → عرض النتيجة
            score = context.user_data.get("h_score", 0)
            total = len(qs)
            pct = (score / total) * 100

            save_progress(query.from_user.id, f"homework:last_result", f"{score}/{total}")

            if pct >= 80:
                level_msg = "🎉 ممتاز! مستواك عالي جدًا"
            elif pct >= 50:
                level_msg = "👍 جيد، محتاج مراجعة بسيطة"
            else:
                level_msg = "⚠️ محتاج تراجع القاعدة دي تاني"

            await query.message.reply_text(
                f"📊 خلصت الواجب!\nنتيجتك: {score}/{total}\n{level_msg}"
            )

            # تنظيف الحالة من user_data
            context.user_data.pop("h_questions", None)
            context.user_data.pop("h_index", None)
            context.user_data.pop("h_score", None)
        return
