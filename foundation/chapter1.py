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
                    "summary": "شرح مبسط لقاعدة الجمع.",
                    "explanation_video": "https://bunny.example.net/explain_rule1.mp4",
                    "examples_videos": [f"https://bunny.example.net/example_{i}.mp4" for i in range(1, 11)],
                    "homework": [
                        {"id": "h1", "q": "2 + 3 = ?", "options": ["4","5","6","7"], "answer": 1, "explanation": "https://bunny.example.net/h1_explain.mp4"},
                        {"id": "h2", "q": "4 + 5 = ?", "options": ["8","9","10","11"], "answer": 1, "explanation": "https://bunny.example.net/h2_explain.mp4"}
                    ]
                }
            ]
        }
    ]
}
