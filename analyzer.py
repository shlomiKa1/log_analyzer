from config import MAP_ROWS, NIGHT_ACTIVITY, MIN_SUSPICION
from checks import is_external, is_sensitive, is_largest_size


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
    return {item: val for item, val in dict_ip_suspicion(data_dict).items() if len(val) >= MIN_SUSPICION}