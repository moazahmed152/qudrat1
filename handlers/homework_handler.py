# handlers/homework_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from exercises.foundation_exercises import get_homework_for_rule
from utils.database import save_progress
import json

async def start_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # callback data will be like: homework:chapter1:lesson1:rule1
    query = update.callback_query
    await query.answer()
    _, chapter_id, lesson_id, rule_id = query.data.split(":")
    hw = get_homework_for_rule(chapter_id, lesson_id, rule_id)
    if not hw:
        await query.edit_message_text("لا توجد أسئلة واجب لهذه القاعدة.")
        return
    # send first question
    q = hw[0]
    opts = [[InlineKeyboardButton(opt, callback_data=f"hwans:{q['question_id']}:{i}")] for i,opt in enumerate(q["options"])]
    await query.edit_message_text(q["question_text"], reply_markup=InlineKeyboardMarkup(opts))
    # store hw list in context
    context.user_data["homework_list"] = hw
    context.user_data["homework_index"] = 0
    return

async def handle_hw_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data  # hwans:question_id:opt_index
    _, qid, opt_idx = data.split(":")
    opt_idx = int(opt_idx)
    hw_list = context.user_data.get("homework_list", [])
    idx = context.user_data.get("homework_index", 0)
    if idx >= len(hw_list):
        await query.edit_message_text("انتهى الواجب.")
        return
    q = hw_list[idx]
    correct = q.get("answer_index")
    user_id = query.from_user.id
    if opt_idx == correct:
        # mark this question done
        save_progress(user_id, f"hw:{qid}", "correct")
        # go to next question
        context.user_data["homework_index"] = idx + 1
        if context.user_data["homework_index"] < len(hw_list):
            q_next = hw_list[context.user_data["homework_index"]]
            opts = [[InlineKeyboardButton(opt, callback_data=f"hwans:{q_next['question_id']}:{i}")] for i,opt in enumerate(q_next["options"])]
            await query.edit_message_text("✅ إجابة صحيحة! السؤال التالي:", reply_markup=InlineKeyboardMarkup(opts))
            return
        else:
            # finished
            await query.edit_message_text("🎉 انتهى الواجب! سيتم حساب النتيجة.")
            # you can compute summary here
            return
    else:
        # wrong -> show explanation video
        await query.edit_message_text(f"❌ إجابة خاطئة. شاهد الشرح: {q.get('explanation_video')}")
        # optionally allow retry or continue to next
        return
