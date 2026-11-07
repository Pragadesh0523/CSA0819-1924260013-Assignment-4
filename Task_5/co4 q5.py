import csv
from datetime import datetime, timedelta

def read_file():
    with open("attendance.csv") as f:
        return list(csv.DictReader(f))

def percentage(data):
    total = len(data)
    present = sum(r["Status"] == "Present" for r in data)
    return present / total * 100 if total else 0

def attendance_report(data):
    print("Attendance:", percentage(data), "%")

def absent_report(data):
    records = {}
    for r in data:
        if r["Status"] == "Absent":
            records.setdefault(r["Student"], set()).add(
                datetime.strptime(r["Date"], "%Y-%m-%d").date())

    for student, dates in records.items():
        dates = sorted(dates)
        for i in range(len(dates) - 2):
            if dates[i+1] == dates[i] + timedelta(days=1) and \
               dates[i+2] == dates[i] + timedelta(days=2):
                print(student, "Absent for 3 consecutive days")
                break

if __name__ == "__main__":
    data = read_file()
    attendance_report(data)
    absent_report(data)