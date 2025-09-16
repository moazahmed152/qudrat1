# handlers/training_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from exercises.training_exercises import get_training_questions
from utils.database import save_progress
from utils.keyboards import example_feedback_keyboard
import random

async def handle_training_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # pattern: train:chapter1:lesson1:rule1:start  (we may call this initially)
    if data.startswith("train:"):
        # structure train:chapter1:lesson1:rule1
        _, chapter_id, lesson_id, rule_id = data.split(":")
        questions = get_training_questions(chapter_id, lesson_id, rule_id)
        if not questions:
            await query.edit_message_text("لا توجد أسئلة تدريب لهذه القاعدة.")
            return
        # send first question
        q = random.choice(questions)
        # show question text and options as inline buttons
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        opts = [[InlineKeyboardButton(opt, callback_data=f"tans:{q['qid']}:{i}")] for i,opt in enumerate(q["options"])]
        await query.edit_message_text(f"❓ {q['text']}", reply_markup=InlineKeyboardMarkup(opts))
        # store current question in context.user_data
        context.user_data["current_training_q"] = q
        return

    # answer to training question: tans:qid:opt_index
    if data.startswith("tans:"):
        _, qid, opt_idx = data.split(":")
        opt_idx = int(opt_idx)
        # find question in context or search all (simple approach: use context)
        q = context.user_data.get("current_training_q")
        if not q or q.get("qid") != qid:
            await query.message.reply_text("لم يتم العثور على السؤال الحالي.")
            return
        correct = q["answer_index"]
        user_id = query.from_user.id
        if opt_idx == correct:
            save_progress(user_id, f"training:{qid}")
            await query.edit_message_text("✅ إجابة صحيحة! شاهد شرح إذا رغبت.", reply_markup=example_feedback_keyboard("training", qid, ""))
        else:
            # send explanation video (if exists)
            await query.edit_message_text(f"❌ إجابة خاطئة. شاهد الشرح:\n{q.get('explain_video')}")
        return
