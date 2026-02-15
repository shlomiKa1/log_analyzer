from config import MIN_ONE_SUSPICION, total_lines, total_suspicion_lines, total_of_suspicions, MIN_THREE_SUSPICION
from analyzer import list_line_checks, dict_of_checks_suspicion, checks_of_all_lines, dict_ip_suspicion, more_of_tow_suspicion
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
    dict_ips = dict_ip_suspicion(generator_file)
    update_global_statistics(generator_file)
    return dict_ips

def generate_report(suspicious):
    """פונקציה המקבלת מילון של IPs עם רשימת החשודות שלה, כך שבונה מחרוזת ל 'דוח תעבורה חשודות'"""
    report = ""
    report += "======================================="
    report += "            דוח תעבורה חשודות          "
    report += "======================================="
    report += "\nסטטיסטקות כלליות:\n"
    report += f" - שורות שנקראו: {total_lines}\n"
    report += f" - שורות חשודות: {total_suspicion_lines}\n"
    for key, val in total_of_suspicions.items():
        report += f" - {key}: {val}\n"

    report += "\nIPs עם רמה סיכון גבוה (3+ חשודות):\n"

    high_risk_level = {}
    low_risk_level = {}
    for ips, sus in suspicious.items():
        if len(sus) >= MIN_THREE_SUSPICION:
            high_risk_level[ips] = sus
        else:
            low_risk_level[ips] = sus

    for ips, sus in high_risk_level.items():
        report += f" - {ips}: {sus}\n"

    report += "\nIPs חשודים נוספים:"
    for ips, sus in low_risk_level.items():
        report += f"\n - {ips}: {sus}"
    return report
