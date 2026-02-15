from checks import is_external, is_sensitive, is_largest_size
from config import (
    MAP_ROWS,
    NIGHT_ACTIVITY,
    MIN_THREE_SUSPICION,
    KB_FORMAT,
    PORT_SENSITIVE,
    MIN_ONE_SUSPICION
)
from datetime import datetime
from reader import load_csv_on_yield


# stage 2
def dict_ip_source(data_list):
    """פונקציה שמחזירה מילון של כתובת IP שולח עם המספר הפניה אליו"""
    val = [data[MAP_ROWS["IP_SOURCE"]] for data in data_list]
    return {key: val.count(key) for key in set(val)}


# פונקציה למיפוי פורט לפרוטוקול
def dict_num_port_name_protocol(data_list):
    """פונקציה שמחזירה מילון של ההמספרי פורט עם השם שלהם"""
    return {int(data[MAP_ROWS["PORT"]]): data[MAP_ROWS["PROTOCOL"]] for data in data_list}


def dict_ip_suspicion(data_list):
    """פונקציה שמחזירה מילון של כתובות עם רשימה החשודות שיש
    יכול להיות שיהיה תיקונים לפונקציה """
    all_ip = (data[MAP_ROWS["IP_SOURCE"]] for data in data_list)
    return {ip_key:
                (list(set(tags
                    for data in data_list if data[MAP_ROWS["IP_SOURCE"]] == ip_key
                    for condition, tags in [(is_external(data[MAP_ROWS["IP_SOURCE"]]), "EXTERNAL_IP"),
                                      (is_sensitive(data[MAP_ROWS["PORT"]]), "PORT_SENSITIVE"),
                                      (is_largest_size(data[MAP_ROWS["SIZE"]]), "LARGE_PACKET"),
                                      (is_night_active(data[MAP_ROWS["DATE"]]), "NIGHT_ACTIVITY")]
                          if condition
                          )))
            for ip_key in all_ip}

# פונקצית עזר לטיפול שעות פעילות
def is_night_active(date_str):
    """בדיקה האם היה פעילות בשעת לילה, בהנחה שקיבלנו שעות ב STR"""
    hour_str = date_str[11:16]
    start, end = NIGHT_ACTIVITY
    return start <= hour_str <= end

def more_of_tow_suspicion(data_dict):
    """פונקציה שמחזירה מילון של כל הכתובות שיש להם יותר משתי חשודות"""
    return {item: val for item, val in dict_ip_suspicion(data_dict).items() if len(val) >= MIN_THREE_SUSPICION}

# stage 3
def format_time(date_str):
    """פונקציה שמקבלת רשימה של timestamps ומחזירה רשימה של השעות"""
    return list(map(lambda time: int(time[11:13]), date_str))


def list_bytes_to_kb(size_str):
    """פונקציה שמקבלת רשימה של מחרזות של גדלים בביטיים ומחזירה רשימה של לקילובייט"""
    return list(map(lambda kb: round(int(kb) / KB_FORMAT, 2), size_str))


def list_of_sensitive_port(data_list):
    """פונקציה שמקבלת רשימה של רשימות ומחזירה רשימה של רשימות של כל ה PORT הרגישים"""
    return list(filter(lambda port: port[MAP_ROWS["PORT"]] in PORT_SENSITIVE.values(), data_list))


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


def dict_of_checks_suspicion() -> dict[str, any]:
    """פונקציה המחזירה מילון שבודק איזה שורות יש להם דברים חשודים"""
    return {"EXTERNAL_IP": lambda ip: is_external(ip[MAP_ROWS["IP_SOURCE"]]),
            "PORT_SENSITIVE": lambda port: is_sensitive(port[MAP_ROWS["PORT"]]),
            "LARGE_PACKET": lambda size: is_largest_size(size[MAP_ROWS["SIZE"]]),
            "NIGHT_ACTIVITY": lambda night: is_night_active_format(night[MAP_ROWS["DATE"]])
            }


def list_line_checks(line, dict_check):
    """פונקציה שמקבלת שורה ומילון של הבדיקות שעשינו, ומחזירה רשימה של כל החשודות שיש לשורה הזאת"""
    return list(filter(lambda checks_name: dict_check[checks_name](line), dict_check))


def checks_of_all_lines(data_list):
    """פונקציה המקבלת רשימה של שורות ומחזירה רשימה של כל החשודות שיש לכל שורה"""
    dict_checks = dict_of_checks_suspicion()
    map_suspicion = map(lambda data: list_line_checks(data, dict_checks), data_list)
    return list(filter(lambda min_suspicion: len(min_suspicion) >= MIN_ONE_SUSPICION, map_suspicion))


# stage 4
def checks_suspicion_yield(generator):
    """פונקציה המקבלת שורה ועוברת ע"י yield על כולם ומחזירה את כל השורות שיש להם לפחות חשודה אחת"""
    dict_check = dict_of_checks_suspicion()
    return (line for line in generator if len(list_line_checks(line, dict_check)) >= MIN_ONE_SUSPICION)


def tuple_of_suspicion_details(generator):
    """פונקציה המקבלת generator ומחזירה רשימה של טאפלים שבראשון יש רשימה של הפרטים של השורה ובשני יש את רשימה של החשודות"""
    dict_check = dict_of_checks_suspicion()
    return ((line, list_line_checks(line, dict_check)) for line in checks_suspicion_yield(generator))


def count_of_suspicion_lines(generator):
    """פונקציה שמקבלת generator ומחזירה את הכמות של השורות החשדות"""
    return sum(1 for l in generator)


def union_all_generator():
    """פונקציה לאיחוד כל ה generator והדפסה כמה שורות חשודות יש"""
    lines = load_csv_on_yield("network_traffic.csv")
    suspicious = checks_suspicion_yield(lines)
    detailed = tuple_of_suspicion_details(suspicious)

    count = count_of_suspicion_lines(detailed)
    print(f"Total of sus {count}")
