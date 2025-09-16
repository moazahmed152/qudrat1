from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import lessons_keyboard, rules_keyboard, rule_content_keyboard, example_feedback_keyboard
from utils.database import save_progress

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("chapter:"):
        _, chapter_id = data.split(":", 1)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        await query.edit_message_text(f"📘 {chapter['chapter_name']}", reply_markup=lessons_keyboard(chapter_id, chapter["lessons"]))
        return

    if data.startswith("lesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        await query.edit_message_text(f"📗 {lesson['lesson_name']}", reply_markup=rules_keyboard(chapter_id, lesson_id, lesson["rules"]))
        return

    if data.startswith("rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)
        txt = f"🔸 {rule['rule_name']}\n\n{rule['summary']}"
        await query.edit_message_text(txt, reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id))
        return

    if data.startswith("explain:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)
        await query.message.reply_text(f"📹 فيديو الشرح:\n{rule['explanation_video']}")
        return

    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson["rules"] if r["rule_id"] == rule_id), None)
        videos = rule.get("examples_videos", [])
        if idx < 1 or idx > len(videos):
            await query.message.reply_text("المثال غير متاح.")
            return
        url = videos[idx-1]
        await query.message.reply_text(f"📺 مثال {idx}:\n{url}")
        await query.message.reply_text("هل فهمت المثال؟", reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx))
        return

    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        key = f"{chapter_id}:{lesson_id}:{rule_id}:ex{idx}"
        save_progress(query.from_user.id, key, "done")
        await query.edit_message_text("✅ تم تسجيل فهمك للمثال.")
        return

    if data.startswith("redo:example:"):
        await query.edit_message_text("🔄 تمام، أعد مشاهدة الفيديو من زر الشرح/المثال.")
        return
