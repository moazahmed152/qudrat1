from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import (
    lessons_keyboard,
    rules_keyboard,
    rule_content_keyboard,
    example_feedback_keyboard,
)
from utils.database import save_progress, get_progress


def _completed_examples_for(user_id: int, chapter_id: str, lesson_id: str, rule_id: str):
    progress = get_progress(user_id) or {}
    prefix = f"{chapter_id}:{lesson_id}:{rule_id}:example"
    done = set()
    for k, v in progress.items():
        if k.startswith(prefix) and v:
            try:
                idx = int(k.replace(prefix, ""))
                done.add(idx)
            except Exception:
                continue
    return done


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

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

        summary = rule.get("summary", "")
        examples = rule.get("examples_videos", [])
        num_examples = len(examples) if examples else 10

        done = _completed_examples_for(user_id, chapter_id, lesson_id, rule_id)

        text = f"🔸 {rule.get('rule_name', '')}\n\n{summary}\n\nاختر: شرح أو أمثلة أو واجب."
        await query.edit_message_text(
            text,
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=num_examples, completed=done),
        )
        return

    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx = int(idx)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
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

    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        idx_int = int(idx)

        key = f"{chapter_id}:{lesson_id}:{rule_id}:example{idx_int}"
        save_progress(user_id, key, "done")

        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)
        examples = rule.get("examples_videos", [])
        num_examples = len(examples) if examples else 10

        done = _completed_examples_for(user_id, chapter_id, lesson_id, rule_id)

        await query.message.reply_text(
            "✅ تمام، تم تسجيل فهمك. اختَر المثال اللى بعده:",
            reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=num_examples, completed=done),
        )
        return

    if data.startswith("redo:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l["lesson_id"] == lesson_id), None)
        rule = next((r for r in lesson.get("rules", []) if r["rule_id"] == rule_id), None)

        url = rule.get("explanation_video")
        if not url:
            await query.message.reply_text("⚠️ لا يوجد فيديو شرح متاح.")
            return

        await query.message.reply_text(f"🔁 إعادة مشاهدة الشرح:\n{url}")
        return
