from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import lessons_keyboard, rules_keyboard, rule_content_keyboard, example_feedback_keyboard
from utils.database import save_progress, load_progress

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # اختيار الباب
    if data.startswith("chapter:"):
        _, chapter_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        await query.edit_message_text(
            f"📘 {chapter['chapter_name']} - اختر الدرس:",
            reply_markup=lessons_keyboard(chapter_id, chapter["lessons"])
        )
        return

    # اختيار الدرس
    if data.startswith("lesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        await query.edit_message_text(
            f"📖 {lesson['lesson_name']} - اختر القاعدة:",
            reply_markup=rules_keyboard(chapter_id, lesson_id, lesson["rules"])
        )
        return

    # اختيار القاعدة
    if data.startswith("rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        completed = load_progress(query.from_user.id).get("completed_examples", [])
        await query.edit_message_text(
            f"⚖️ القاعدة {rule_id}: اختياراتك",
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, completed=completed)
        )
        return

    # شرح القاعدة
    if data.startswith("explain:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        await query.edit_message_text(f"📹 شرح القاعدة {rule_id} هنا (ضع لينك الفيديو)")
        return

    # مثال
    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        await query.edit_message_text(
            f"🎬 مثال {idx}: لينك الفيديو هنا",
            reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx)
        )
        return

    # بعد الإجابة على المثال
    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)

        # حفظ إن المثال اتفهم
        save_progress(query.from_user.id, "completed_examples", idx)

        completed = load_progress(query.from_user.id).get("completed_examples", [])
        await query.edit_message_text(
            f"✅ تم تعليم مثال {idx} كمفهوم",
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, completed=completed)
        )
        return

    if data.startswith("redo:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        await query.edit_message_text(
            f"🔄 إعادة مثال {idx}: نفس لينك الفيديو",
            reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx)
        )
        return
