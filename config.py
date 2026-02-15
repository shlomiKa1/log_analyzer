"""
קובץ להגדרת: משתנים קבועים,
"""


PORT_SENSITIVE = {"SSH": "22", "TELNET": "23", "RDP": "3389"} # מילון של פורטים רגישים
SIZE_BYTES_FILE = 5000 # גודל הקובץ
MAP_ROWS = {"DATE": 0, "IP_SOURCE": 1, "IP_DEST": 2, "PORT": 3, "PROTOCOL": 4, "SIZE": 5, "SIZE_STATUS": 6} # מפה לעמודות
NIGHT_ACTIVITY = ("00:00", "06:00") # שעות לילה
MIN_THREE_SUSPICION = 3 # מינימום חשודות
NOT_EXTERNAL_IP = ("10.", "192.168") # כתובות חוקיים
KB_FORMAT = 1024 # המרת של בייטים לקילובייט
MIN_ONE_SUSPICION = 1

# globals
total_lines = 0
total_suspicion_lines = 0
total_of_suspicions = {}
