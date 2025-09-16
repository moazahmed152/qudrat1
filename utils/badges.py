def assign_badge(score_pct):
    if score_pct >= 90:
        return "🏅 ميدالية ذهبية"
    elif score_pct >= 70:
        return "🥈 ميدالية فضية"
    elif score_pct >= 50:
        return "🥉 ميدالية برونزية"
    else:
        return "📘 محتاج مراجعة"
