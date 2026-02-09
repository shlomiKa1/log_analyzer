def list_ip_source(list_data):
    """מחזירה רשימה של כתובות חיצוניות של השולח"""
    for data in list_data:
        if is_external(data[1]):
            yield data[1]

# פונקצית עזר
def is_external(data) -> bool:
    """בודקת האם זה כתובות חיצוניות"""
    return data[0:2:] != "10" and data[0:7:] != "192.168"