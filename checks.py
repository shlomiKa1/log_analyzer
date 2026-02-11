from config import PORT_SENSITIVE, SIZE_BYTES_FILE, MAP_ROWS, NOT_EXTERNAL_IP


# פונקציה לרשימת IP source
def list_ip_source(data_list):
    """מחזירה רשימה של כתובות חיצוניות של השולח"""
    for data in data_list:
        if is_external(data[MAP_ROWS["IP_SOURCE"]]):
            yield data[MAP_ROWS["IP_SOURCE"]]

# פונקצית עזר
def is_external(data) -> bool:
    """בודקת האם זה כתובות חיצוניות"""
    return data[0:2:] != NOT_EXTERNAL_IP[0] and data[0:7:] != NOT_EXTERNAL_IP[1]

# פונקציה לרישמת פורטים רגישים
def port_sensitive_list(data_list):
    """החזרת רשימה של כל הפורטים הרגישים"""
    return [data[MAP_ROWS["PORT"]] for data in data_list if is_sensitive(data[MAP_ROWS["PORT"]])]

 # פונקצית עזר לפורטים
def is_sensitive(data):
    """בודקת האם אלה פורטים רגישים"""
    return data in PORT_SENSITIVE.values()

# פונקציה לרשימת גדלים
def list_of_size(data_list):
    """החזרת רשימה של הגדלים של הקובץ שיותר מ- 5000"""
    return (is_largest_size(data[MAP_ROWS["SIZE"]]) for data in data_list)

# פונקציה לבדיקת גודל
def is_largest_size(data):
    """פונקצית לבדיקת גודל"""
    return int(data) > SIZE_BYTES_FILE

# פונקציה תג לגודל קובץ
def tags_size(data_list):
    """הוספת תג לרשימה רשימות האם יש חריגה או לא"""
    return [data.append("LARGE") if is_largest_size(data[MAP_ROWS["SIZE"]]) else data.append("NORMAL") for data in data_list]