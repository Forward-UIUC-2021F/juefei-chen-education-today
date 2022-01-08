import mysql.connector
import string
import pathlib
from collections import defaultdict

key_words = ['professor', 'associate', 'assistant', 'lecturer', 'assoc', 'adjunct', 'faculty', 'instructor', 'director', 'asst',
             'emeritus', 'prof ']

def check_position(s):
    s = s.lower()
    for i in key_words:
        if i in s:
            return True
    return False
