from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# القائمة الرئيسية
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📘 تأسيس", callback_data="foundation")],
        [InlineKeyboardButton("📗 تدريب", callback_data="training")],
        [InlineKeyboardButton("📊 إحصائياتي", callback_data="stats")],
        [InlineKeyboardButton("🔀 سؤال عشوائي", callback_data="random_q")]
    ]
    return InlineKeyboardMarkup(keyboard)


# قائمة الأبواب
def chapters_keyboard(chapters, mode="foundation"):
    keyboard = []
    for ch in chapters:
        keyboard.append([
            InlineKeyboardButton(f"📂 {ch['title']}", callback_data=f"{mode}:chapter:{ch['id']}")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


# قائمة الدروس
def lessons_keyboard(lessons, chapter_id, mode="foundation"):
    keyboard = []
    for l in lessons:
        keyboard.append([
            InlineKeyboardButton(f"📖 {l['title']}", callback_data=f"{mode}:lesson:{chapter_id}:{l['id']}")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data=f"{mode}:back")])
    return InlineKeyboardMarkup(keyboard)


# قائمة القواعد
def rules_keyboard(rules, chapter_id, lesson_id, mode="foundation"):
    keyboard = []
    for r in rules:
        keyboard.append([
            InlineKeyboardButton(f"📑 {r['title']}", callback_data=f"{mode}:rule:{chapter_id}:{lesson_id}:{r['id']}")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data=f"{mode}:lesson_back:{chapter_id}")])
    return InlineKeyboardMarkup(keyboard)


# قائمة محتوى القاعدة (شرح + أمثلة + واجب)
def rule_content_keyboard(chapter_id, lesson_id, rule_id):
    keyboard = [
        [InlineKeyboardButton("🎥 شرح القاعدة", callback_data=f"rule_video:{chapter_id}:{lesson_id}:{rule_id}")],
    ]
    for i in range(1, 11):  # 10 أمثلة
        keyboard.append([
            InlineKeyboardButton(f"📝 مثال {i}", callback_data=f"example:{chapter_id}:{lesson_id}:{rule_id}:{i}")
        ])
    keyboard.append([
        InlineKeyboardButton("📒 واجب", callback_data=f"homework:{chapter_id}:{lesson_id}:{rule_id}")
    ])
    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data=f"foundation:lesson_back:{chapter_id}")])
    return InlineKeyboardMarkup(keyboard)


# أزرار سؤال التدريب أو الواجب
def t_question_keyboard(qid, options):
    keyboard = []
    for idx, opt in enumerate(options):
        keyboard.append([
            InlineKeyboardButton(opt, callback_data=f"hans:{qid}:{idx}")
        ])
    return InlineKeyboardMarkup(keyboard)


# أزرار بعد المثال (فهمت / محتاج إعادة)
def example_feedback_keyboard(chapter_id, lesson_id, rule_id, example_idx):
    keyboard = [
        [InlineKeyboardButton("✅ فهمت", callback_data=f"example_done:{chapter_id}:{lesson_id}:{rule_id}:{example_idx}")],
        [InlineKeyboardButton("🔄 محتاج إعادة", callback_data=f"example_retry:{chapter_id}:{lesson_id}:{rule_id}:{example_idx}")]
    ]
    return InlineKeyboardMarkup(keyboard)
