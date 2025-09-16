# training/chapter1.py

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
                            "text": "ما ناتج 1 + 4؟",
                            "options": ["3", "4", "5", "6"],
                            "answer_index": 2,
                            "explain_video": "https://bunny.example.net/videos/tr_ch1_l1_r1_q1_explain.mp4"
                        },
                        {
                            "qid": "t_ch1_l1_r1_q2",
                            "text": "ما ناتج 2 + 3؟",
                            "options": ["4", "5", "6", "3"],
                            "answer_index": 1,
                            "explain_video": "https://bunny.example.net/videos/tr_ch1_l1_r1_q2_explain.mp4"
                        },
                        {
                            "qid": "t_ch1_l1_r1_q3",
                            "text": "ما ناتج 5 + 0؟",
                            "options": ["5", "0", "1", "6"],
                            "answer_index": 0,
                            "explain_video": "https://bunny.example.net/videos/tr_ch1_l1_r1_q3_explain.mp4"
                        }
                        # ممكن تضيف باقي الأسئلة بنفس الشكل
                    ]
                }
            ]
        }
    ]
}
