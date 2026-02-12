from config import KB_FORMAT, PORT_SENSITIVE, MIN_ONE_SUSPICION
from datetime import datetime
from analyzer import *

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


def dict_of_checks_suspicion():
    """פונקציה המחזירה מילון שבודק איזה שורות יש להם דברים חשודים"""
    return {"EXTERNAL_IP": lambda ip: is_external(ip[MAP_ROWS["IP_SOURCE"]]),
            "PORT_SENSITIVE": lambda port: is_sensitive(port[MAP_ROWS["PORT"]]),
            "LARGE_PACKET": lambda size: is_largest_size(size[MAP_ROWS["SIZE"]]),
            "NIGHT_ACTIVITY": lambda night: is_night_active_format(night[MAP_ROWS["DATE"]])
            }

def list_line_checks(line, dict_check):
    """פונקציה שמקבלת שורה ומילון של הבדיקות שעשינו, ומחזירה רשימהשל כל החשודות שיש לשורה הזאת"""
    return list(filter(lambda checks_name: dict_check[checks_name](line), dict_check))


def checks_of_all_lines(data_list):
    """פונקציה המקבלת רשימה של שורות ומחזירה רשימהשל כל החשודות שיש לכל שורה"""
    dict_checks = dict_of_checks_suspicion()
    map_suspicion = map(lambda data: list_line_checks(data, dict_checks), data_list)
    return list(filter(lambda min_suspicion: len(min_suspicion) >= MIN_ONE_SUSPICION, map_suspicion))

# stage 4
def checks_suspicion_yield(line_file_yield):
    """פונקציה המקבלת שורה ועוברת ע"י yield על כולם ומחזירה את כל השורות שיש להם לפחות חשודה אחת"""
    dict_check = dict_of_checks_suspicion()
    return list(line for line in line_file_yield if list_line_checks(line, dict_check))
