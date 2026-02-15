from config import MIN_ONE_SUSPICION, total_lines, total_suspicion_lines, total_of_suspicions
from analyzer import list_line_checks, dict_of_checks_suspicion, checks_of_all_lines, dict_ip_suspicion
from reader import load_csv_on_yield


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

def analyze_log(file):
    """פונקציה המקבלת ניתוב לקובץ ומעבדת  קריאה לקובץ, בדיקת חשודות, מילון עם IP והחשודות ןעדכון סטטיסטיקות"""
    generator_file = list(load_csv_on_yield(file))
    checks_suspicions_line = [list_line_checks(line, dict_of_checks_suspicion()) for line in generator_file]
    dict_ups = dict_ip_suspicion(generator_file)
    update_global_statistics(generator_file)

