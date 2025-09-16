# handlers/foundation_handler.py
import json, os
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import chapters_keyboard, lessons_keyboard, rules_keyboard, rule_content_keyboard
from utils.database import load_students, save_students
from pathlib import Path

LESSONS_DIR = "foundation"

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # chapter:{chapter_id}
    if data.startswith("chapter:"):
        _, chapter_id = data.split(":",1)
        # load chapter file
        path = Path(LESSONS_DIR) / f"{chapter_id}.py"
        # our foundation files are Python modules with CHAPTER dict; import dynamically
        try:
            module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
            chapter = getattr(module, "CHAPTER", None)
        except Exception:
            chapter = None
        if not chapter:
            await query.edit_message_text("لم يتم العثور على الباب.")
            return
        lessons = chapter.get("lessons", [])
        await query.edit_message_text(f"📘 {chapter.get('chapter_name')}\nاختر الدرس:", reply_markup=lessons_keyboard(chapter_id, lessons))
        return

    # lesson:chapter1:lesson1
    if data.startswith("lesson:"):
        _, chapter_id, lesson_id = data.split(":")
        try:
            module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
            chapter = getattr(module, "CHAPTER", None)
        except Exception:
            chapter = None
        if not chapter:
            await query.edit_message_text("خطأ في تحميل الدرس.")
            return
        lesson = next((l for l in chapter.get("lessons",[]) if l["lesson_id"]==lesson_id), None)
        if not lesson:
            await query.edit_message_text("الدرس غير موجود.")
            return
        await query.edit_message_text(f"📗 {lesson.get('lesson_name')}\nاختر القاعدة:", reply_markup=rules_keyboard(chapter_id, lesson_id, lesson.get("rules", [])))
        return

    # rule:chapter1:lesson1:rule1
    if data.startswith("rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        try:
            module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
            chapter = getattr(module, "CHAPTER", None)
        except Exception:
            chapter = None
        if not chapter:
            await query.edit_message_text("خطأ في تحميل القاعدة.")
            return
        lesson = next((l for l in chapter.get("lessons",[]) if l["lesson_id"]==lesson_id), None)
        rule = None
        if lesson:
            rule = next((r for r in lesson.get("rules",[]) if r["rule_id"]==rule_id), None)
        if not rule:
            await query.edit_message_text("القاعدة غير موجودة.")
            return

        text = f"🔸 {rule.get('rule_name')}\n\n{rule.get('summary','')}\n\nاختر: شاهد الفيديو أو مثال."
        await query.edit_message_text(text, reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id))
        return

    # explain:chapter1:lesson1:rule1  -> send explanation video link
    if data.startswith("explain:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter.get("lessons",[]) if l["lesson_id"]==lesson_id), None)
        rule = next((r for r in lesson.get("rules",[]) if r["rule_id"]==rule_id), None)
        url = rule.get("explanation_video")
        await query.message.reply_text(f"📹 رابط شرح القاعدة:\n{url}")
        return

    # example:chapter1:lesson1:rule1:3
    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter.get("lessons",[]) if l["lesson_id"]==lesson_id), None)
        rule = next((r for r in lesson.get("rules",[]) if r["rule_id"]==rule_id), None)
        videos = rule.get("examples_videos", [])
        if idx-1 < 0 or idx-1 >= len(videos):
            await query.message.reply_text("المثال غير متوفر.")
            return
        url = videos[idx-1]
        # send video link
        await query.message.reply_text(f"🔗 رابط المثال {idx}:\n{url}")
        # show feedback keyboard
        from utils.keyboards import example_feedback_keyboard
        await query.message.reply_text("هل فهمت المثال؟", reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx))
        return

    # got:example:chapter1:lesson1:rule1:3
    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        user_id = update.callback_query.from_user.id
        key = f"{chapter_id}:{lesson_id}:{rule_id}:example{idx}"
        from utils.database import save_progress
        save_progress(user_id, key)
        await query.edit_message_text("✅ تمام، تم تسجيل فهمك للمثال.")
        return

    # redo:example:...
    if data.startswith("redo:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER")
        lesson = next((l for l in chapter.get("lessons",[]) if l["lesson_id"]==lesson_id), None)
        rule = next((r for r in lesson.get("rules",[]) if r["rule_id"]==rule_id), None)
        await query.message.reply_text(f"🔁 إعادة شرح القاعدة:\n{rule.get('explanation_video')}")
        return

    # homework:chapter1:lesson1:rule1
    if data.startswith("homework:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        # Route to homework handler by callback (handled by homework handler registered)
        # We just edit message to indicate loading
        await query.edit_message_text("🔎 جاري تحميل أسئلة الواجب...")
        # The homework handler (registered separately) will catch callbacks like hwq:...
        return
