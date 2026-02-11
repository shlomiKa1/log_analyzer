
def format_time(date_str):
    """פונקציה שמקבלת רשימה של timestamps ומחזירה רשימה של השעעות"""
    return list(map(lambda time: int(time[11:13]),  date_str))