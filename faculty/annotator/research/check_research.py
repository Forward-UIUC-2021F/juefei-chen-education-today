import mysql.connector
import string
import pathlib
from collections import defaultdict

abs_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

forbiden = {'center', 'policy', 'admissions', 'admission', 'aid', 'course', 'university', 'institute', 'department', 'major', 
            'school', 'personal', 'libarary', 'community', 'communities'}
negative = set()
research_areas = set()
research_keywords = set()

f = open(abs_path + 'negative.txt', 'r')
for i in f.readlines():
    i = i.strip().lower()
    for j in i.split():
        negative.add(j)

d = defaultdict(int)
f = open(abs_path + 'research_areas.txt', 'r')
for i in f.readlines():
    i = i.strip()
    research_areas.add(i)
    for j in i.split():
        research_keywords.add(j)
        d[j] += 1

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="owl2.cs.illinois.edu",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor


def check_research(s):
    s = s.lower().strip().replace(',', '')
    if s in research_areas:
        return True
    s = s.split()
    n = 0
    for i in s:
        if i in forbiden:
            return False
        if i not in negative and i in research_keywords:
            n += 1
    if len(s) > 20:
        return n >= 4
    if len(s) > 50:
        return n >= 8
    return n >= 2 or n == len(s) == 1


# mydb, mycursor = connect_to_mysql()
# mycursor.execute("SELECT Research FROM Faculty where Task_ID like '48%'")
# r = mycursor.fetchall()
# for i in range(9434):
#     if r[i][0]:
#         print(i, check_research(r[i][0]), r[i][0].strip())
#         print()