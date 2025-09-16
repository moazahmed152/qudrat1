# foundation/chapter1.py
CHAPTER = {
    "chapter_id": "chapter1",
    "chapter_name": "الباب الأول",
    "lessons": [
        {
            "lesson_id": "lesson1",
            "lesson_name": "الدرس 1",
            "rules": [
                {
                    "rule_id": "rule1",
                    "rule_name": "قاعدة الجمع",
                    "summary": "ملخص: طريقة جمع الأعداد بسرعة باستخدام خطوات بسيطة.",
                    "explanation_video": "https://bunny.example.net/videos/ch1_l1_r1_explain.mp4",
                    "examples_videos": [
                        f"https://bunny.example.net/videos/ch1_l1_r1_ex_{i}.mp4" for i in range(1,11)
                    ],
                    "homework": [
                        {
                            "question_id": "hw_ch1_l1_r1_q1",
                            "question_text": "كم حاصل 2 + 3 ؟",
                            "options": ["4","5","6","7"],
                            "answer_index": 1,
                            "explanation_video": "https://bunny.example.net/videos/hw_ch1_l1_r1_q1_explain.mp4"
                        }
                    ]
                },
                {
                    "rule_id": "rule2",
                    "rule_name": "قاعدة الطرح",
                    "summary": "ملخص الطرح مع أمثلة.",
                    "explanation_video": "https://bunny.example.net/videos/ch1_l1_r2_explain.mp4",
                    "examples_videos": [
                        f"https://bunny.example.net/videos/ch1_l1_r2_ex_{i}.mp4" for i in range(1,11)
                    ],
                    "homework": []
                }
            ]
        },
        {
            "lesson_id": "lesson2",
            "lesson_name": "الدرس 2",
            "rules": [
                {
                    "rule_id": "rule1_l2",
                    "rule_name": "قاعدة الضرب",
                    "summary": "ملخص الضرب.",
                    "explanation_video": "https://bunny.example.net/videos/ch1_l2_r1_explain.mp4",
                    "examples_videos": [f"https://bunny.example.net/videos/ch1_l2_r1_ex_{i}.mp4" for i in range(1,11)],
                    "homework": []
                }
            ]
        }
    ]
}
