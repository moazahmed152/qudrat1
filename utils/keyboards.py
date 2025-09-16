from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# القائمة الرئيسية
def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("📘 تأسيس", callback_data="foundation")],
        [InlineKeyboardButton("📝 تدريب", callback_data="training")],
        [InlineKeyboardButton("📊 إحصائياتي", callback_data="stats")],
        [InlineKeyboardButton("🔀 سؤال عشوائي", callback_data="random_question")],
    ]
    return InlineKeyboardMarkup(buttons)


# قائمة الدروس داخل الباب
def lessons_keyboard(chapter_id, lessons):
    rows = []
    for l in lessons:
        rows.append([
            InlineKeyboardButton(
                l["lesson_name"],
                callback_data=f"lesson:{chapter_id}:{l['lesson_id']}"
            )
        ])
    return InlineKeyboardMarkup(rows)


# قائمة القواعد داخل الدرس
def rules_keyboard(chapter_id, lesson_id, rules):
    rows = []
    for r in rules:
        rows.append([
            InlineKeyboardButton(
                r["rule_name"],
                callback_data=f"rule:{chapter_id}:{lesson_id}:{r['rule_id']}"
            )
        ])
    return InlineKeyboardMarkup(rows)


# قائمة القاعدة مع ✅
def rule_content_keyboard(chapter_id, lesson_id, rule_id, num_examples=10, completed=None):
    done = set(int(x) for x in (completed or []))

    rows = [[InlineKeyboardButton("📹 شرح القاعدة", callback_data=f"explain:{chapter_id}:{lesson_id}:{rule_id}")]]
    for i in range(1, num_examples + 1):
        label = f"✅ مثال {i}" if i in done else f"مثال {i}"
        rows.append([InlineKeyboardButton(label, callback_data=f"example:{chapter_id}:{lesson_id}:{rule_id}:{i}")])

    rows.append([InlineKeyboardButton("📝 واجب", callback_data=f"homework:{chapter_id}:{lesson_id}:{rule_id}")])
    return InlineKeyboardMarkup(rows)


# أزرار بعد المثال
def example_feedback_keyboard(chapter_id, lesson_id, rule_id, idx):
    rows = [
        [
            InlineKeyboardButton("✅ فهمت", callback_data=f"got:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}"),
            InlineKeyboardButton("🔄 إعادة", callback_data=f"redo:example:{chapter_id}:{lesson_id}:{rule_id}:{idx}"),
        ]
    ]
    return InlineKeyboardMarkup(rows)


# أسئلة الواجب/التدريب
def t_question_keyboard(qid, options):
    rows = []
    for i, opt in enumerate(options):
        rows.append([InlineKeyboardButton(opt, callback_data=f"hans:{qid}:{i}")])
    return InlineKeyboardMarkup(rows)


# رجوع للقائمة الرئيسية
def main_menu_reply():
    keyboard = [["🏠 القائمة الرئيسية"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
