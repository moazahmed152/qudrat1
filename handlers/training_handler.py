from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import t_lessons_keyboard, t_rules_keyboard, t_question_keyboard
from utils.database import save_progress

async def handle_training_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # اختيار باب
    if data.startswith("tchapter:"):
        _, chapter_id = data.split(":")
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        await query.edit_message_text(
            f"📗 {chapter['chapter_name']} - اختر الدرس:",
            reply_markup=t_lessons_keyboard(chapter_id, chapter["lessons"])
        )
        return

    # اختيار درس
    if data.startswith("tlesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        await query.edit_message_text(
            f"📖 {lesson['lesson_name']} - اختر القاعدة:",
            reply_markup=t_rules_keyboard(chapter_id, lesson_id, lesson["rules"])
        )
        return

    # اختيار قاعدة للتدريب
    if data.startswith("trule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"training.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)

        qs = rule.get("questions", [])
        if not qs:
            await query.edit_message_text("⚠️ لا يوجد أسئلة تدريب حالياً.")
            return

        context.user_data["t_questions"] = qs
        context.user_data["t_index"] = 0
        context.user_data["t_score"] = 0

        q = qs[0]
        await query.edit_message_text(f"❓ {q['q']}", reply_markup=t_question_keyboard(q["id"], q["options"]))
        return

    # إجابة سؤال تدريب
    if data.startswith("tans:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)
        idx = context.user_data.get("t_index", 0)
        qs = context.user_data.get("t_questions", [])
        if idx >= len(qs):
            await query.edit_message_text("✅ انتهى التدريب.")
            return
        q = qs[idx]
        correct = (opt_idx == q["answer"])

        if correct:
            context.user_data["t_score"] += 1
            await query.edit_message_text("✅ إجابة صحيحة!")
        else:
            await query.edit_message_text(f"❌ خطأ.\n📺 الشرح: {q.get('explanation')}")

        idx += 1
        context.user_data["t_index"] = idx

        if idx < len(qs):
            nq = qs[idx]
            await query.message.reply_text(f"❓ {nq['q']}", reply_markup=t_question_keyboard(nq["id"], nq["options"]))
        else:
            score = context.user_data.get("t_score", 0)
            total = len(qs)
            save_progress(query.from_user.id, f"training:last_result", f"{score}/{total}")
            await query.message.reply_text(f"📊 خلصت التدريب!\nنتيجتك: {score}/{total}")
        return
