from config import MIN_ONE_SUSPICION, total_lines, total_suspicion_lines, total_of_suspicions
from analyzer import list_line_checks, dict_of_checks_suspicion


def update_global_statistics(generator):
    """פונקציה המעדכנת את כל המשתנים הגלובלים בזמן ריצה"""
    global total_lines, total_suspicion_lines, total_of_suspicions
    for line in generator:
        total_lines += 1
        suspicion = dict_of_checks_suspicion()
        line_suspicion = (list_line_checks(line, suspicion))

        # בדיקה האם השרורה הנוכחית קיימת איזו חשודה
        if len(line_suspicion) >= MIN_ONE_SUSPICION:
            total_suspicion_lines += 1
        # לולאה שעוברת על כל החשדות שיש בשורה הנוכחית
        for key in line_suspicion:
            # אם החשוד לא קיים, נוסיף אותו למילון עם ערך אחד
            if key not in total_of_suspicions:
                total_of_suspicions[key] = 1
            # אחרת נוסיף אחד לחשוד הקיים
            else:
                total_of_suspicions[key] += 1
