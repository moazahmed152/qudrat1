from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import (
    lessons_keyboard,
    rules_keyboard,
    rule_content_keyboard,
    example_feedback_keyboard,
)
from utils.database import save_progress


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # اختيار باب (Chapter)
    if data.startswith("chapter:"):
        _, chapter_id = data.split(":", 1)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lessons = chapter.get("lessons", [])
        await query.edit_message_text(
            f"📘 {chapter.get('chapter_name', '')}\nاختر الدرس:",
            reply_markup=lessons_keyboard(chapter_id, lessons),
        )
        return

    # اختيار درس (Lesson)
    if data.startswith("lesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        if not lesson:
            await query.edit_message_text("❌ الدرس غير موجود.")
            return
        await query.edit_message_text(
            f"📗 {lesson.get('lesson_name', '')}\nاختر القاعدة:",
            reply_markup=rules_keyboard(chapter_id, lesson_id, lesson.get("rules", [])),
        )
        return

    # اختيار قاعدة (Rule)
    if data.startswith("rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        if not lesson:
            await query.edit_message_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
        if not rule:
            await query.edit_message_text("❌ القاعدة غير موجودة.")
            return

        text = f"🔸 {rule.get('rule_name', '')}\n\n{rule.get('summary', '')}\n\nاختر: شرح أو أمثلة أو واجب."
        await query.edit_message_text(
            text,
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id),
        )
        return

    # فيديو شرح القاعدة
    if data.startswith("explain:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        url = rule.get("explanation_video")
        if not url:
            await query.message.reply_text("⚠️ لا يوجد فيديو شرح للقاعدة حالياً.")
            return

        await query.message.reply_text(f"📹 رابط شرح القاعدة:\n{url}")
        return

    # فتح مثال معيّن
    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        videos = rule.get("examples_videos", [])
        if not (1 <= idx <= len(videos)):
            await query.message.reply_text("⚠️ المثال غير متوفر.")
            return

        url = videos[idx - 1]
        await query.message.reply_text(f"📺 مثال {idx}:\n{url}")
        await query.message.reply_text(
            "هل فهمت المثال؟",
            reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx),
        )
        return

    # الطالب اختار "✅ فهمت" → نسجل التقدم ونرجّعه لقائمة الأمثلة/القاعدة
    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        key = f"{chapter_id}:{lesson_id}:{rule_id}:example{idx}"
        save_progress(query.from_user.id, key, "done")

        # ارجاع نفس قائمة القاعدة (شرح + أمثلة + واجب)
        await query.message.reply_text(
            "✅ تمام، خلصت المثال ده. اختار اللي بعده:",
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=10),
        )
        return

    # الطالب اختار "🔄 إعادة" → نعيد إرسال فيديو الشرح
    if data.startswith("redo:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        url = rule.get("explanation_video")
        if not url:
            await query.message.reply_text("⚠️ لا يوجد فيديو شرح متاح.")
            return

        await query.message.reply_text(f"🔁 إعادة مشاهدة الشرح:\n{url}")
        return
