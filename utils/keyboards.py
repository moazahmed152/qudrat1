from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# القائمة الرئيسية
def main_menu_reply():
    kb = [["📘 تأسيس", "📗 تدريب"], ["📊 إحصائياتي", "🔀 سؤال عشوائي"]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# ---------------------- تأسيس ----------------------

def chapters_keyboard(chapters):
    rows = [[InlineKeyboardButton(ch["chapter_name"], callback_data=f"chapter:{ch['chapter_id']}")] for ch in chapters]
    return InlineKeyboardMarkup(rows)

def lessons_keyboard(chapter_id, lessons):
    rows = [[InlineKeyboardButton(ls["lesson_name"], callback_data=f"lesson:{chapter_id}:{ls['lesson_id']}")] for ls in lessons]
    return InlineKeyboardMarkup(rows)

def rules_keyboard(chapter_id, lesson_id, rules):
    rows = [[InlineKeyboardButton(r["rule_name"], callback_data=f"rule:{chapter_id}:{lesson_id}:{r['rule_id']}")] for r in rules]
    return InlineKeyboardMarkup(rows)

def rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=10, completed=None):
    done = set(int(x) for x in (completed or []))
    rows = [[InlineKeyboardButton("📹 شرح القاعدة", callback_data=f"explain:{chapter_id}:{lesson_id}:{rule_id}")]]
    for i in range(1, num_examples+1):
        label = f"✅ مثال {i}" if i in done else f"مثال {i}"
        rows.append([InlineKeyboardButton(label, callback_data=f"example:{chapter_id}:{lesson_id}:{rule_id}:{i}")])
    rows.append([InlineKeyboardButton("📝 واجب", callback_data=f"homework:{chapter_id}:{lesson_id}:{rule_id}")])
    return InlineKeyboardMarkup(rows)

def example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx):
    rows = [[
        InlineKeyboardButton("✅ فهمت", callback_data=f"got:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}"),
        InlineKeyboardButton("🔄 إعادة", callback_data=f"redo:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}")
    ]]
    return InlineKeyboardMarkup(rows)

# ---------------------- تدريب ----------------------

def t_chapters_keyboard(chapters):
    rows = [[InlineKeyboardButton(ch["chapter_name"], callback_data=f"tchapter:{ch['chapter_id']}")] for ch in chapters]
    return InlineKeyboardMarkup(rows)

def t_lessons_keyboard(chapter_id, lessons):
    rows = [[InlineKeyboardButton(ls["lesson_name"], callback_data=f"tlesson:{chapter_id}:{ls['lesson_id']}")] for ls in lessons]
    return InlineKeyboardMarkup(rows)

def t_rules_keyboard(chapter_id, lesson_id, rules):
    rows = [[InlineKeyboardButton(r["rule_name"], callback_data=f"trule:{chapter_id}:{lesson_id}:{r['rule_id']}")] for r in rules]
    return InlineKeyboardMarkup(rows)

def t_question_keyboard(qid, options):
    rows = [[InlineKeyboardButton(opt, callback_data=f"tans:{qid}:{i}")] for i, opt in enumerate(options)]
    return InlineKeyboardMarkup(rows)
