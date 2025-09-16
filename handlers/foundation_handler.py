# handlers/foundation_handler.py
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
    """
    ترجع set بالأرقام (ints) بتاعت الأمثلة اللي الطالب خلاها 'done'
    بنفترض إننا خزناهم بمفتاح: "{chapter}:{lesson}:{rule}:example{idx}"
    """
    done = set()
    # هنحاول نقرأ كل الأمثلة من 1..N عن طريق get_progress
    # لكن get_progress بتاخد مفتاح، فمشاعلنا هنا نبحث عن كل مفاتيح موجودة
    # أسلوب بسيط: نتحقق من أرقام من 1 إلى 50 (لو عندك عدد أقل عدّله)
    # أفضل لو عندك قائمة الأمثلة فعلًا، يبقى تستخدم طولها، لكن هنا نحافظ على مرونة.
    prefix = f"{chapter_id}:{lesson_id}:{rule_id}:example"
    # نفحص أرقام من 1 لـ 50 (لو عندك أمثلة أقل، مش هتأثر)
    for i in range(1, 51):
        k = f"{prefix}{i}"
        try:
            val = get_progress(user_id, k)
        except Exception:
            val = None
        if val == "done":
            done.add(i)
    return done


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    # اختيار باب (chapter)
    if data.startswith("chapter:"):
        # callback_data example: "chapter:chapter1"
        _, chapter_id = data.split(":", 1)
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lessons = chapter.get("lessons", [])
        await query.edit_message_text(
            f"📘 {chapter.get('chapter_name', '')}\nاختر الدرس:",
            reply_markup=lessons_keyboard(chapter_id, lessons),
        )
        return

    # اختيار درس (lesson)
    if data.startswith("lesson:"):
        # callback_data example: "lesson:chapter1:lesson1"
        _, chapter_id, lesson_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        if not lesson:
            await query.edit_message_text("❌ الدرس غير موجود.")
            return
        await query.edit_message_text(
            f"📗 {lesson.get('lesson_name', '')}\nاختر القاعدة:",
            reply_markup=rules_keyboard(chapter_id, lesson_id, lesson.get("rules", [])),
        )
        return

    # اختيار قاعدة (rule)
    if data.startswith("rule:"):
        # callback_data example: "rule:chapter1:lesson1:rule1"
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        if not lesson:
            await query.edit_message_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r.get("rule_id") == rule_id), None)
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
            reply_markup=rule_content_keyboard(
                chapter_id, lesson_id, rule_id, num_examples=num_examples, completed=done
            ),
        )
        return

    # عرض فيديو شرح القاعدة
    if data.startswith("explain:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r.get("rule_id") == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        url = rule.get("explanation_video")
        if not url:
            await query.message.reply_text("⚠️ لا يوجد فيديو شرح للقاعدة حالياً.")
            return

        await query.message.reply_text(f"📹 رابط شرح القاعدة:\n{url}")
        return

    # فتح مثال معين
    if data.startswith("example:"):
        # callback_data: example:chapter1:lesson1:rule1:3
        _, chapter_id, lesson_id, rule_id, idx = data.split(":")
        try:
            idx_int = int(idx)
        except ValueError:
            await query.message.reply_text("⚠️ خطأ في رقم المثال.")
            return

        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r.get("rule_id") == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        videos = rule.get("examples_videos", [])
        if not videos or idx_int < 1 or idx_int > len(videos):
            await query.message.reply_text("⚠️ المثال غير متوفر.")
            return

        url = videos[idx_int - 1]
        await query.message.reply_text(f"📺 مثال {idx_int}:\n{url}")
        await query.message.reply_text(
            "هل فهمت المثال؟",
            reply_markup=example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx_int),
        )
        return

    # الطالب ضغط "✅ فهمت" على المثال → نسجّل ونعيد القايمة مع ✅
    if data.startswith("got:example:"):
        # callback_data: got:example:chapter1:lesson1:rule1:3
        parts = data.split(":")
        if len(parts) != 6:
            await query.message.reply_text("⚠️ بيانات غير صحيحة.")
            return
        _, _, chapter_id, lesson_id, rule_id, idx = parts
        try:
            idx_int = int(idx)
        except ValueError:
            await query.message.reply_text("⚠️ رقم المثال غير صحيح.")
            return

        # حفظ التقدّم
        key = f"{chapter_id}:{lesson_id}:{rule_id}:example{idx_int}"
        try:
            save_progress(user_id, key, "done")
        except Exception:
            # لا توقف التنفيذ لو حصل خطأ بالحفظ
            pass

        # نعيد تحميل حالة القاعدة ونحسب عدد الأمثلة وعدد المكتمل
        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        rule = next((r for r in lesson.get("rules", []) if r.get("rule_id") == rule_id), None)
        examples = rule.get("examples_videos", [])
        num_examples = len(examples) if examples else 10

        done = _completed_examples_for(user_id, chapter_id, lesson_id, rule_id)

        await query.message.reply_text(
            "✅ تمام، تم تسجيل فهمك. اختَر المثال اللى بعده:",
            reply_markup=rule_content_keyboard(
                chapter_id, lesson_id, rule_id, num_examples=num_examples, completed=done
            ),
        )
        return

    # إعادة مشاهدة الشرح (🔄)
    if data.startswith("redo:example:"):
        # callback_data: redo:example:chapter1:lesson1:rule1:3
        parts = data.split(":")
        if len(parts) != 6:
            await query.message.reply_text("⚠️ بيانات غير صحيحة.")
            return
        _, _, chapter_id, lesson_id, rule_id, idx = parts
        try:
            idx_int = int(idx)
        except ValueError:
            await query.message.reply_text("⚠️ رقم المثال غير صحيح.")
            return

        module = __import__(f"foundation.{chapter_id}", fromlist=["CHAPTER"])
        chapter = getattr(module, "CHAPTER", {})
        lesson = next((l for l in chapter.get("lessons", []) if l.get("lesson_id") == lesson_id), None)
        if not lesson:
            await query.message.reply_text("❌ الدرس غير موجود.")
            return
        rule = next((r for r in lesson.get("rules", []) if r.get("rule_id") == rule_id), None)
        if not rule:
            await query.message.reply_text("❌ القاعدة غير موجودة.")
            return

        url = rule.get("explanation_video")
        if not url:
            await query.message.reply_text("⚠️ لا يوجد فيديو شرح متاح.")
            return

        await query.message.reply_text(f"🔁 إعادة مشاهدة الشرح:\n{url}")
        return

    # لو مفيش أي pattern اتطابق، نرجّع رسالة بسيطة
    await query.message.reply_text("⚠️ حدث خطأ، حاول تاني أو ارجع للقائمة الرئيسية.")
    return
