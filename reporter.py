from config import KB_FORMAT


def format_time(date_str):
    """פונקציה שמקבלת רשימה של timestamps ומחזירה רשימה של השעות"""
    return list(map(lambda time: int(time[11:13]),  date_str))

def list_bytes_to_kb(size_str):
    """פונקציה שמקבלת רשימה של מחרזות של גדלים בביטיים ומחזירה רשימה של לקילובייט"""
    return list(map(lambda kb: round(int(kb) / KB_FORMAT, 2), size_str))