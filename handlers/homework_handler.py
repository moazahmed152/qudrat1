from telegram import Update
from telegram.ext import ContextTypes
from utils.database import save_progress


async def handle_homework_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # بدء واجب جديد
    if data.startswith("homework:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)

        questions = rule.get("homework", [])
        if not questions:
            await query.message.reply_text("⚠️ لا يوجد واجب لهذه القاعدة.")
            return

        context.user_data["homework"] = {
            "qid": f"{chapter_id}:{lesson_id}:{rule_id}",
            "questions": questions,
            "current": 0,
            "score": 0,
        }

        q = questions[0]
        opts = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(q["options"])])
        await query.message.reply_text(f"📝 {q['q']}\n\n{opts}\n\n(اختر الإجابة برقمها)")
        return

    # التعامل مع إجابة الطالب
    if data.startswith("hans:"):
        _, qid, idx, ans = data.split(":")
        idx, ans = int(idx), int(ans)

        hw = context.user_data.get("homework", {})
        qs = hw.get("questions", [])
        if idx >= len(qs):
            return

        q = qs[idx]
        if ans == q["answer"]:
            hw["score"] += 1
            await query.message.reply_text("✅ إجابة صحيحة!")
        else:
            await query.message.reply_text(
                f"❌ إجابة خاطئة.\n📹 الشرح: {q['explanation']}"
            )

        # سؤال جديد أو نهاية
        hw["current"] += 1
        if hw["current"] < len(qs):
            nq = qs[hw["current"]]
            opts = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(nq["options"])])
            await query.message.reply_text(f"📝 {nq['q']}\n\n{opts}")
        else:
            # نهاية الواجب → عرض النتيجة
            score = hw["score"]
            total = len(qs)
            pct = (score / total) * 100

            save_progress(query.from_user.id, f"homework:{qid}", f"{score}/{total}")

            if pct >= 80:
                level_msg = "🎉 ممتاز! مستواك عالي جدًا"
            elif pct >= 50:
                level_msg = "👍 جيد، محتاج مراجعة بسيطة"
            else:
                level_msg = "⚠️ محتاج تراجع القاعدة دي تاني"

            await query.message.reply_text(
                f"📊 خلصت الواجب!\nنتيجتك: {score}/{total}\n{level_msg}"
            )

            # امسح بيانات الواجب من user_data
            context.user_data.pop("homework", None)
