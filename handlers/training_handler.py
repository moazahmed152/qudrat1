# handlers/training_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from exercises.training_exercises import get_training_chapter, get_training_lesson, get_training_rule
from utils.database import save_progress
import random
from datetime import datetime

# بيانات المستخدم أثناء التدريب
user_training_data = {}

async def handle_training_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # المرحلة 1: اختيار قاعدة (rule)
    if data.startswith("train_chapter:"):
        _, chapter_id = data.split(":")
        chapter = get_training_chapter(chapter_id)
        if not chapter:
            await query.edit_message_text("❌ هذا الباب غير موجود.")
            return
        # show lessons inside chapter
        keyboard = []
        for lesson in chapter["lessons"]:
            for rule in lesson["rules"]:
                keyboard.append([InlineKeyboardButton(f"{lesson['lesson_name']} - {rule['rule_name']}", callback_data=f"train_rule:{chapter_id}:{lesson['lesson_id']}:{rule['rule_id']}")])
        await query.edit_message_text("اختر القاعدة للتدريب:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # المرحلة 2: اختيار قاعدة محددة → عرض السؤال الأول
    if data.startswith("train_rule:"):
        _, chapter_id, lesson_id, rule_id = data.split(":")
        rule = get_training_rule(chapter_id, lesson_id, rule_id)
        if not rule or not rule.get("questions"):
            await query.edit_message_text("❌ لا توجد أسئلة لهذه القاعدة.")
            return

        # تهيئة بيانات التدريب للمستخدم
        user_id = query.from_user.id
        user_training_data[user_id] = {
            "chapter_id": chapter_id,
            "lesson_id": lesson_id,
            "rule_id": rule_id,
            "questions": rule["questions"],
            "current": 0,
            "score": 0,
            "start_time": datetime.now()
        }
        await send_training_question(query, context, user_id)
        return

    # المرحلة 3: التعامل مع الإجابة على السؤال
    if data.startswith("tans:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)
        user_id = query.from_user.id
        training = user_training_data.get(user_id)
        if not training:
            await query.message.reply_text("❌ لم يتم بدء التدريب.")
            return

        q = training["questions"][training["current"]]
        if q["qid"] != qid:
            await query.message.reply_text("❌ حدث خطأ بالسؤال الحالي.")
            return

        correct = q["answer_index"]
        if opt_idx == correct:
            training["score"] += 1
            save_progress(user_id, f"training:{qid}")
            feedback_text = "✅ إجابة صحيحة!"
        else:
            feedback_text = f"❌ إجابة خاطئة. شاهد الشرح:\n{q.get('explain_video')}"

        # تعديل الأزرار لإظهار الإجابة الصحيحة
        keyboard = [[InlineKeyboardButton(f"✅ {opt}" if i==correct else f"❌ {opt}" if i==opt_idx else opt, callback_data=f"ignore:{i}")] for i,opt in enumerate(q["options"])]
        await query.edit_message_text(f"{feedback_text}\n\n{q['text']}", reply_markup=InlineKeyboardMarkup(keyboard))

        # الانتقال للسؤال التالي
        training["current"] += 1
        if training["current"] < len(training["questions"]):
            await send_training_question(query, context, user_id)
        else:
            await finish_training(query, context, user_id)

async def send_training_question(query, context, user_id):
    training = user_training_data[user_id]
    q = training["questions"][training["current"]]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"tans:{q['qid']}:{i}")] for i,opt in enumerate(q["options"])]
    await context.bot.send_message(chat_id=user_id, text=f"❓ سؤال {training['current']+1}/{len(training['questions'])}\n{q['text']}", reply_markup=InlineKeyboardMarkup(keyboard))

async def finish_training(query, context, user_id):
    training = user_training_data[user_id]
    total = len(training["questions"])
    score = training["score"]
    time_taken = int((datetime.now()-training["start_time"]).total_seconds())
    text = f"🏁 انتهى التدريب!\n⏱️ الوقت: {time_taken} ثانية\n🏆 نتيجتك: {score}/{total}"
    keyboard = [["📗 تدريب من جديد"]]
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    user_training_data.pop(user_id)
