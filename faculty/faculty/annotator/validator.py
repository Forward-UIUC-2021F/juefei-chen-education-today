from name.check_name import check_name
from position.check_position import check_position
from phone.check_phone import check_phone
from research.check_research import check_research

import csv

def check_email(s):
    s = s.lower()
    if '@' in s and ('.edu' in s or '.com' in s):
        return True
    return False

with open('CS_faculty_200_universities.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            print(row)
            print(check_name(row[1]), check_position(row[2]), check_email(row[3]),  check_phone(row[4]), check_research(row[-2]))
            print()
        line_count += 1
