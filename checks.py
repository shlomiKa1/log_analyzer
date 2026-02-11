from config import PORT_SENSITIVE, SIZE_BYTES_FILE, MAP_ROWS, NIGHT_ACTIVITY


# פונקציה לרשימת IP source
def list_ip_source(data_list):
    """מחזירה רשימה של כתובות חיצוניות של השולח"""
    for data in data_list:
        if is_external(data[MAP_ROWS["IP_SOURCE"]]):
            yield data[MAP_ROWS["IP_SOURCE"]]

# פונקצית עזר
def is_external(data) -> bool:
    """בודקת האם זה כתובות חיצוניות"""
    return data[0:2:] != "10" and data[0:7:] != "192.168"

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
    return (data[MAP_ROWS["SIZE"]] for data in data_list if int(data[MAP_ROWS["SIZE"]]) > SIZE_BYTES_FILE)


# פונקציה תג לגודל קובץ
def tags_size(data_list):
    """הוספת תג לרשימה רשימות האם יש חריגה או לא"""
    return [data.append("LARGE") if int(data[MAP_ROWS["SIZE"]]) > SIZE_BYTES_FILE else data.append("NORMAL") for data in data_list]

# stage 2
def dict_ip_source(data_list):
    """פונקציה שמחזירה מילון של כתובת IP שולח עם המספר הפניה אליו"""
    val = [data[MAP_ROWS["IP_SOURCE"]] for data in data_list]
    return {key: val.count(key) for key in set(val)}


# פונקציה למיפוי פורט לפרוטוקול
def dict_num_port_name_protocol(data_list):
    """פונקציה שמחזירה מילון של ההמספרי פורט עם השם שלהם"""
    return {int(data[MAP_ROWS["PORT"]]): data[MAP_ROWS["PROTOCOL"]] for data in data_list}


def night_active(data_list):
    """פונקציה שמחזירה מילון של כתובות עם רשימה החששות שיש
    יכול להיות שיהיה תיקונים לפונקציה """
    all_ip = (data[MAP_ROWS["IP_SOURCE"]] for data in data_list)
    return {ip_key:
                (list(set(tags
                    for data in data_list if data[MAP_ROWS["IP_SOURCE"]] == ip_key
                    for condition, tags in [(is_external(data[MAP_ROWS["IP_SOURCE"]]), "EXTERNAL_IP"),
                                      (is_sensitive(data[MAP_ROWS["PORT"]]), "PORT_SENSITIVE"),
                                      (int(data[MAP_ROWS["SIZE"]]) > SIZE_BYTES_FILE, "LARGE_PACKET"),
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
