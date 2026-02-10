"""
קובץ להגדרת: משתנים קבועים,
"""


PORT_SENSITIVE = {"SSH": "22", "TELNET": "23", "RDP": "3389"} # מילון של פורטים רגישים
SIZE_BYTES_FILE = 5000 # גודל הקובץ
MAP_ROWS = {"DATE": 0, "IP_SOURCE": 1, "IP_DEST": 2, "PORT": 3, "PROTOCOL": 4, "SIZE": 5, "SIZE_STATUS": 6} # מפה לעמודות