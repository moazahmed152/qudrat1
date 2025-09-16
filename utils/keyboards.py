# utils/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def main_menu_reply():
    kb = [["📘 تأسيس", "📗 تدريب"], ["🔀 سؤال عشوائي", "/stats"]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def chapters_keyboard(chapters):
    # chapters: list of dicts with chapter_name & chapter_id
    kb = [[InlineKeyboardButton(ch["chapter_name"], callback_data=f"chapter:{ch['chapter_id']}")] for ch in chapters]
    return InlineKeyboardMarkup(kb)

def lessons_keyboard(chapter_id, lessons):
    kb = [[InlineKeyboardButton(ls["lesson_name"], callback_data=f"lesson:{chapter_id}:{ls['lesson_id']}")] for ls in lessons]
    return InlineKeyboardMarkup(kb)

def rules_keyboard(chapter_id, lesson_id, rules):
    kb = [[InlineKeyboardButton(r["rule_name"], callback_data=f"rule:{chapter_id}:{lesson_id}:{r['rule_id']}")] for r in rules]
    return InlineKeyboardMarkup(kb)

def rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=10):
    kb = []
    kb.append([InlineKeyboardButton("📹 شرح القاعدة", callback_data=f"explain:{chapter_id}:{lesson_id}:{rule_id}")])
    for i in range(1, num_examples+1):
        kb.append([InlineKeyboardButton(f"مثال {i}", callback_data=f"example:{chapter_id}:{lesson_id}:{rule_id}:{i}")])
    kb.append([InlineKeyboardButton("📝 واجب", callback_data=f"homework:{chapter_id}:{lesson_id}:{rule_id}")])
    return InlineKeyboardMarkup(kb)

def example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx):
    kb = [
        [
            InlineKeyboardButton("✅ فهمت", callback_data=f"got:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}"),
            InlineKeyboardButton("🔄 إعادة", callback_data=f"redo:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}")
        ]
    ]
    return InlineKeyboardMarkup(kb)
