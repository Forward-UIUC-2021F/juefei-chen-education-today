import mysql.connector
import string
import pathlib
from collections import defaultdict

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="owl2.cs.illinois.edu",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

def view_keywords():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT Position FROM Faculty;')
    r = mycursor.fetchall()
    d = defaultdict(int)
    for i in r:
        t = i[0].split()
        for j in t:
            d[j.lower()] += 1
    l = []
    for i in d:
        l.append([d[i], i])
    l.sort()
    for i in l:
        print(i)
    print(len(r))


key_words = ['professor', 'associate', 'assistant', 'lecturer', 'assoc', 'adjunct', 'faculty', 'instructor', 'director', 'asst',
             'emeritus', 'prof ']

def check_position(s):
    s = s.lower()
    for i in key_words:
        if i in s:
            return True
    return False
