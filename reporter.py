from config import KB_FORMAT, MAP_ROWS, PORT_SENSITIVE, NIGHT_ACTIVITY
from datetime import datetime, time

def format_time(date_str):
    """פונקציה שמקבלת רשימה של timestamps ומחזירה רשימה של השעות"""
    return list(map(lambda time: int(time[11:13]),  date_str))

def list_bytes_to_kb(size_str):
    """פונקציה שמקבלת רשימה של מחרזות של גדלים בביטיים ומחזירה רשימה של לקילובייט"""
    return list(map(lambda kb: round(int(kb) / KB_FORMAT, 2), size_str))

def list_of_sensitive_port(data_list):
    """פונקציה שמקבלת רשימה של רשימות ומחזירה רשימה של רשימותץ של כל ה PORT הרגישים"""
    return list( filter(lambda port: port[MAP_ROWS["PORT"]] in PORT_SENSITIVE.values(), data_list))

def list_of_night_active(data_list):
    """פונקציה שמחזירה רשימה של רשימות של כל אלה שהיו שבשעות הלילה (ממוין)"""
    return sorted(list(filter(lambda data: is_night_active_format(data[MAP_ROWS["DATE"]]), data_list)))

# פונקצית עזר פורמט זמן
def is_night_active_format(date_str):
    """פונקציה לפירמוט מחרזות של זמן לשעוות, ובדיקה אם זה בטווח של שעות הלילה"""
    format_str_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    current = format_str_date.time()

    start = datetime.strptime(NIGHT_ACTIVITY[0], "%H:%M").time()
    end = datetime.strptime(NIGHT_ACTIVITY[1], "%H:%M").time()

    # אם הטווח הוא מחצות
    if start < end:
        return start <= current <= end
    # אם הטווח מתחיל לפני חצות ונגמר אחרי חצות
    return start <= current or end >= current