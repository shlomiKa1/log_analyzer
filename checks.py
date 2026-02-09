from config import PORT_SENSITIVE, SIZE_BYTES_FILE


def list_ip_source(data_list):
    """מחזירה רשימה של כתובות חיצוניות של השולח"""
    for data in data_list:
        if is_external(data[1]):
            yield data[1]

# פונקצית עזר
def is_external(data) -> bool:
    """בודקת האם זה כתובות חיצוניות"""
    return data[0:2:] != "10" and data[0:7:] != "192.168"


def port_sensitive_list(data_list):
    """החזרת רשימה של כל הפורטים הרגישים"""
    return [data[3] for data in data_list if is_sensitive(data[3])]

 # פונקצית עזר לפורטים
def is_sensitive(data):
    """בודקת האם אלה פורטים רגישים"""
    return data in PORT_SENSITIVE.values()


def list_of_size(data_list):
    """החזרת רשימה של הגדלים של הקובץ שיותר מ- 5000"""
    return (data[-1] for data in data_list if int(data[-1]) > SIZE_BYTES_FILE)