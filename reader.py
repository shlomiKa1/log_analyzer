import csv


def load_csv_to_list(filename):
    """טעינה קובץ csv ומחזירה רשימה של רשימות"""
    try:
        with open(filename, 'r', encoding='utf-8') as rFile:
            reader = csv.reader(rFile)
            data = list(reader)
            return data
    except FileNotFoundError:
        print("Error not found file")
        return None