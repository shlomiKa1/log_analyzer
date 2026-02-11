from config import KB_FORMAT, MAP_ROWS, PORT_SENSITIVE


def format_time(date_str):
    """פונקציה שמקבלת רשימה של timestamps ומחזירה רשימה של השעות"""
    return list(map(lambda time: int(time[11:13]),  date_str))

def list_bytes_to_kb(size_str):
    """פונקציה שמקבלת רשימה של מחרזות של גדלים בביטיים ומחזירה רשימה של לקילובייט"""
    return list(map(lambda kb: round(int(kb) / KB_FORMAT, 2), size_str))

def list_of_sensitive_port(data_list):
    """פונקציה שמקבלת רשימה של רשימות ומחזירה רשימה של רשימותץ של כל ה PORT הרגישים"""
    return list( filter(lambda port: port[MAP_ROWS["PORT"]] in PORT_SENSITIVE.values(), data_list))