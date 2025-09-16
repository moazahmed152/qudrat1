from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import lessons_keyboard, rules_keyboard, rule_content_keyboard, example_feedback_keyboard
from utils.database import save_progress, load_students

def _completed_examples_for(user_id, chapter_id, lesson_id, rule_id):
    students = load_students()
    student = students.get(str(user_id), {})
    progress = student.get("progress", {})
    return [
        int(k.split("example")[-1])
        for k, v in progress.items()
        if k.startswith(f"{chapter_id}:{lesson_id}:{rule_id}:example") and v == "done"
    ]

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "foundation":
        module = __import__("foundation.chapter1", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        await query.edit_message_text("📘 اختر الدرس:", reply_markup=lessons_keyboard("chapter1", chapter["lessons"]))
        return

    if data.startswith("lesson:"):
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = module.CHAPTER
        lesson = next((l for l in chapter["lessons"] if l["lesson_id"] == lesson_id), None)
        await query.edit_message_text("📘 اختر القاعدة:", reply_markup=rules_keyboard(chapter_id, lesson_id, lesson["rules"]))
        return

    if data.startswith("rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        done = _completed_examples_for(user_id, chapter_id, lesson_id, rule_id)
        await query.edit_message_text("📘 محتوى القاعدة:", reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, completed=done))
        return

    if data.startswith("example:"):
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        await query.edit_message_text(f"🎬 مثال {idx}\n📺 لينك الفيديو: https://example.com/{idx}",
                                      reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx))
        return

    if data.startswith("got:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        save_progress(user_id, f"{chapter_id}:{lesson_id}:{rule_id}:example{idx}", "done")
        done = _completed_examples_for(user_id, chapter_id, lesson_id, rule_id)
        await query.edit_message_text("✅ تمام، تم تسجيل فهمك.", reply_markup=rule_content_keyboard(chapter_id, lesson_id, rule_id, completed=done))
        return

    if data.startswith("redo:example:"):
        _, _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        await query.edit_message_text(f"🔄 إعادة مثال {idx}\n📺 لينك الفيديو: https://example.com/{idx}",
                                      reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx))
        return
