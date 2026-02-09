from config import *


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