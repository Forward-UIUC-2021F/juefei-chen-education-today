# celery -A tasks worker --pool=solo --loglevel=info
# celery -A tasks worker --pool=prefork --concurrency=1 --loglevel=info
# src/redis-server --protected-mode no

# redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import time
from algorithm import find
import json
import mysql.connector
import datetime

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="owl2.cs.illinois.edu",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

# Redis broker URL
# BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://juefeic2@172.22.224.119:6379/0'

celery_app = Celery('Restaurant', broker=BROKER_URL)

@celery_app.task(soft_time_limit=300)
def get_faculty(university, department):
    mydb, mycursor = connect_to_mysql()
    try:
        mycursor.execute('select University_ID from University where University_Name = "{}"'.format(university))
        university_id = int(mycursor.fetchone()[0])
        start = time.time()
        data, url = find(university, department)
        
        execution_time = int(time.time() - start)
        timestamp = datetime.datetime.now().strftime("%m/%d/%y-%X")
        status = 'Success' if len(data) > 0 else 'Fail'
        task_id = str(university_id) + department + '_' + timestamp
        print(task_id)
        print(university_id)
        print(department)
        print(timestamp)
        print(execution_time)
        print(url)
        sql = 'insert into Faculty_History (Task_ID, University_ID, Department_Name, Time_Stamp, Execution_Time, URL, Algo_Version, Status) values (%s, %s, %s, %s, %s, %s, %s, %s)'
        vals = (task_id, university_id, department, timestamp, execution_time, url, 1, status)
        mycursor.execute(sql, vals)
        sql = 'insert into Faculty (Task_ID, Name, Position, Research, Email, Phone) values (%s, %s, %s, %s, %s, %s)'
        for i in data:
            if not i['Name']:
                continue
            for j in ['Posistion', 'Research Interest', 'Email', 'Phone number']:
                if j not in i:
                    i[j] = 'Missing'
            vals = (task_id, i['Name'], i['Position'], i['Research Interest'], i['Email'], i['Phone number'])
            mycursor.execute(sql, vals)

        print('# faculty: ' + str(len(data)))
        print(url)
        # mycursor.execute('update Faculty_Tasks set Priority = 2147483647 where University_ID = {} and Department_Name = "{}"'.format(university_id, department))
        # mydb.commit()
    except SoftTimeLimitExceeded:
        print('time limit...')
    finally:
        mycursor.execute('update Faculty_Tasks set Priority = 2147483647 where University_ID = {} and Department_Name = "{}"'.format(university_id, department))
        mydb.commit()
        mycursor.close()
        mydb.close()
    