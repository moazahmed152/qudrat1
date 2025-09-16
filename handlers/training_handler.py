from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import t_lessons_keyboard, t_rules_keyboard, t_question_keyboard
from utils.database import save_progress

async def handle_training_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("tchapter:"):
        _, chapter_id = data.split(":", 1)
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        await query.edit_message_text(f"🎯 {chapter['chapter_name']}", reply_markup=t_lessons_keyboard(chapter_id, chapter["lessons"]))
        return

    if data.startswith("tlesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        await query.edit_message_text(f"📗 {lesson['lesson_name']}", reply_markup=t_rules_keyboard(chapter_id, lesson_id, lesson["rules"]))
        return

    if data.startswith("trule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)
        questions = rule.get("questions", [])
        if not questions:
            await query.edit_message_text("لا توجد أسئلة حالياً لهذه القاعدة.")
            return
        context.user_data["t_questions"] = questions
        context.user_data["t_index"] = 0
        context.user_data["t_score"] = 0
        q = questions[0]
        await query.edit_message_text(f"❓ {q['question_text']}", reply_markup=t_question_keyboard(q["question_id"], q["options"]))
        return

    if data.startswith("tans:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)
        idx = context.user_data.get("t_index", 0)
        qs = context.user_data.get("t_questions", [])
        if idx >= len(qs):
            await query.edit_message_text("انتهى التدريب.")
            return
        q = qs[idx]
        correct = (opt_idx == q["answer_index"])

        if correct:
            context.user_data["t_score"] = context.user_data.get("t_score", 0) + 1
            await query.edit_message_text("✅ إجابة صحيحة!")
        else:
            await query.edit_message_text(f"❌ إجابة خاطئة.\n📺 الشرح: {q.get('explanation_video')}")

        # التالي
        idx += 1
        context.user_data["t_index"] = idx

        if idx < len(qs):
            nq = qs[idx]
            await query.message.reply_text(f"❓ {nq['question_text']}", reply_markup=t_question_keyboard(nq["question_id"], nq["options"]))
        else:
            score = context.user_data.get("t_score", 0)
            total = len(qs)
            pct = (score / total) * 100
            # احفظ النتيجة
            save_progress(query.from_user.id, f"training:last_result", f"{score}/{total}")

            # مستوى
            if pct >= 80:
                level_msg = "🎉 ممتاز! مستواك عالي جدًا"
            elif pct >= 50:
                level_msg = "👍 جيد، محتاج مراجعة بسيطة"
            else:
                level_msg = "⚠️ محتاج تراجع القاعدة دي تاني"

            await query.message.reply_text(f"🎉 خلصت التدريب!\nنتيجتك: {score}/{total}\n{level_msg}")
        return
