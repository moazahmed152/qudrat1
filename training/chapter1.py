# training/chapter1.py
# يحتوي أسئلة تدريب لقاعدة محددة (نفس هيكل القواعد في التأسيس)
TRAINING_CHAPTER = {
    "chapter_id": "chapter1",
    "chapter_name": "تدريب الباب الأول",
    "lessons": [
        {
            "lesson_id": "lesson1",
            "lesson_name": "الدرس 1",
            "rules": [
                {
                    "rule_id": "rule1",
                    "rule_name": "قاعدة الجمع",
                    "questions": [
                        {
                            "qid": "t_ch1_l1_r1_q1",
                            "text": "ما ناتج 1+4؟",
                            "options": ["3","4","5","6"],
                            "answer_index": 2,
                            "explain_video": "https://bunny.example.net/videos/tr_ch1_l1_r1_q1_explain.mp4"
                        },
                        # ... 9 أسئلة إضافية
                    ]
                }
            ]
        }
    ]
}
