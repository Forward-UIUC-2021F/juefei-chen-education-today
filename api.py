from flask import Flask, request
import os
import mysql.connector
import json

app = Flask(__name__)

checked = {}

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="localhost",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

@app.route('/universityNum', methods=['GET', 'POST'])
def get_university_num():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) FROM University;')
    universityNum = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'universityNum': universityNum}

@app.route('/departmentNum', methods=['GET', 'POST'])
def get_department_num():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) FROM Department;')
    departmentNum = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM Department_History where Status = "Success";')
    success = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM Department_History where Status = "Fail";')
    fail = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'departmentNum': departmentNum, 'success': success, 'fail': fail}

@app.route('/facultyNum', methods=['GET', 'POST'])
def get_faculty_num():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) FROM Faculty;')
    facultyNum = mycursor.fetchone()[0]
    mycursor.execute('select count(distinct(University_ID)) from Faculty_History;')
    universityCount = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM Faculty_History where Status = "Success";')
    success = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM Faculty_History where Status = "Fail";')
    fail = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'facultyNum': facultyNum, 'universityCount': universityCount, 'success': success, 'fail': fail}

@app.route('/averageRunningTime', methods=['GET', 'POST'])
def get_average_running_time():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT avg(Execution_Time) FROM Department_History;')
    department = mycursor.fetchone()[0]
    mycursor.execute('SELECT avg(Execution_Time) FROM Faculty_History where Status = "Success";')
    faculty = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'department': department, 'faculty': faculty}

@app.route('/getUniversityList', methods=['GET', 'POST'])
def get_university_list():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT * FROM University;')
    r = mycursor.fetchall()
    university = ['All']
    for i in r:
        university.append(str(i[0]) + '. ' + i[1])
    mycursor.close()
    mydb.close()
    return {'university': university}

@app.route('/getDepartmentList', methods=['GET', 'POST'])
def get_department_list():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    if len(data) == 0 or data == 'All':
        return {'department': []}
    q = data.split('. ')
    mycursor.execute('SELECT Task_ID FROM Department_History where University_ID = ' + q[0] + ';')
    id = mycursor.fetchone()[0]
    mycursor.execute('SELECT Department_Name from Department where Task_ID = "' + id + '";')
    r = mycursor.fetchall()
    departments = ['All']
    for i in r:
        departments.append(i[0])
    mycursor.close()
    mydb.close()
    return {'department': departments}

@app.route('/submitQuery', methods=['GET', 'POST'])
def submit_query():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    if len(data) == 0:
        return {'result': []}
    if len(data['department']) > 0 and data['department'] != 'All':
        university_id = int(data['university'].split('. ')[0])
        department = data['department']
        sql = 'SELECT Task_ID, URL, Execution_Time from Faculty_History where University_ID = "{}" and Department_Name = "{}";'.format(university_id, department)
        mycursor.execute(sql)
        t = mycursor.fetchone()
        task_id = t[0]
        url = t[1]
        execution_time = t[2]
        print(task_id)
        mycursor.execute('SELECT Name, Position, Research, Email, Phone from Faculty where Task_ID = "' + task_id + '";')
        r = mycursor.fetchall()
        res = []
        for i in r:
            # res.append({'Name': i[0], 'Position': i[1], 'Research': i[2], 'Email': i[3], 'Phone': i[4]})
            res.append(list(i))
        mycursor.close()
        mydb.close()
        return {'result': res, 'type': 'Faculty', 'url': url, 'execution_time': execution_time, 'task_id': task_id}
    else:
        university_id = int(data['university'].split('. ')[0])
        sql = 'SELECT Task_ID, URL, Execution_Time from Department_History where University_ID = "{}";'.format(university_id)
        mycursor.execute(sql)
        t = mycursor.fetchone()
        task_id = t[0]
        url = t[1]
        execution_time = t[2]
        mycursor.execute('SELECT Department_Name from Department where Task_ID = "' + task_id + '";')
        r = mycursor.fetchall()
        res = []
        for i in r:
            # res.append({'Department': i[0]})
            res.append([i[0]])
        mycursor.close()
        mydb.close()
        return {'result': res, 'type': 'Department', 'url': url, 'execution_time': execution_time, 'task_id': task_id}

@app.route('/getUniversityWithFacultyFailure', methods=['GET', 'POST'])
def get_university_with_faculty_failure():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT DISTINCT University_ID, University_Name FROM University;')
    r = mycursor.fetchall()
    university = ['ALL']
    for i in r:
        university.append(str(i[0]) + '. ' + i[1])
    mycursor.close()
    mydb.close()
    return {'university': university}

@app.route('/getFailures', methods=['GET', 'POST'])
def get_failures():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    university_id = int(data['university'].split('. ')[0])
    mycursor.execute('SELECT DISTINCT Department_Name FROM Faculty_History where Status like "Fail%" and University_ID = "{}";'.format(university_id))
    r = mycursor.fetchall()
    department = []
    for i in r:
        department.append({'Department': i[0]})
    mycursor.close()
    mydb.close()
    return {'result': department, 'type': 'Department'}

@app.route('/getTask', methods=['GET', 'POST'])
def get_task():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    if data['university'] == 'ALL':
        mycursor.execute('SELECT University_Name, Department_Name, Execution_Time, Algo_Version, Status, Time_Stamp, URL from Faculty_History natural join University order by University_ID asc, Department_Name asc;')
    else:
        university_id = int(data['university'].split('. ')[0])
        mycursor.execute('SELECT University_Name, Department_Name, Execution_Time, Algo_Version, Status, Time_Stamp, URL from Faculty_History natural join University where University_ID = "{}" order by Department_Name asc;'.format(university_id))
    r = mycursor.fetchall()
    res = []
    for i in range(len(r)):
        res.append(list(r[i]))
    mycursor.close()
    mydb.close()
    return {'result': res, 'type': 'Department'}

@app.route('/changeData', methods=['GET', 'POST'])
def change_data():
    mydb, mycursor = connect_to_mysql()
    d = json.loads(request.data)
    task_id = d['id']
    data = d['data']
    print(task_id)
    print(data[0])
    if not task_id:
        return {}
    mycursor.execute('DELETE from Faculty where Task_ID = "{}"'.format(task_id))
    sql = 'insert into Faculty (Task_ID, Name, Position, Research, Email, Phone) values (%s, %s, %s, %s, %s, %s)'
    for i in data:
        if not i[0]:
            continue
        try:
            vals = (task_id, i[0], i[1], i[2], i[3], i[4])
            mycursor.execute(sql, vals)
        except:
            print('Error in inserting new faculty data!!!')
            continue
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {}

@app.route('/correction', methods=['GET', 'POST'])
def correction():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    try:
        l = data[0]
    except:
        mycursor.close()
        mydb.close()
        return {}
    print(l)
    if l[2] == l[3]:
        mycursor.close()
        mydb.close()
        return {}
    m = {0: 'Name', 1: 'Position', 2: 'Research', 3: 'Email', 4: 'Phone'}
    type = m[l[1]]
    mycursor.execute('select * from Correction where Type = "{}" and Old = "{}" and New = "{}"'.format(type, l[3], l[2]))
    r = mycursor.fetchall()
    if len(r) == 0:
        sql = 'insert into Correction (Type, Old, New) values (%s, %s, %s)'
        mycursor.execute(sql, (type, l[2], l[3]))
    else:
        mycursor.execute('delete from Correction where Type = "{}" and Old = "{}" and New = "{}"'.format(type, l[3], l[2]))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {}

@app.route('/departmentOverview', methods=['GET', 'POST'])
def department_overview():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) FROM Department_History where Status = "Success";')
    success = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM Department_History where Status = "Fail";')
    fail = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'res': [['Status', 'Num'], ['Success', success], ['Fail', fail]]}

@app.route('/facultyOverview', methods=['GET', 'POST'])
def faculty_overview():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute("select count(*) from (select University_ID, Department_Name from Faculty_History where Status = 'Success' group by University_ID, Department_Name) a;")
    success = mycursor.fetchone()[0]
    mycursor.execute("select count(*) from (select University_ID, Department_Name from Faculty_History where Status = 'Fail' group by University_ID, Department_Name) a;")
    fail = mycursor.fetchone()[0]
    mycursor.execute("select count(*) from Department")
    n = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'res': [['Status', 'Num'], ['Success', success], ['Fail', fail], ['None', n]]}

@app.route('/departmentExecutionTime', methods=['GET', 'POST'])
def department_execution_time():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) from Department_History where Execution_Time <= 10;')
    t1 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Department_History where 10 < Execution_Time <= 30;')
    t2 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Department_History where 30 < Execution_Time <= 90;')
    t3 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Department_History where 90 < Execution_Time;')
    t4 = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'res': [['Status', 'Num'], ['[0, 10]', t1], ['(10, 30]', t2], ['(30, 90]', t3], ['(90, inf)', t4]]}

@app.route('/facultyExecutionTime', methods=['GET', 'POST'])
def faculty_execution_time():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('SELECT count(*) from Faculty_History where Execution_Time <= 10;')
    t1 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 10 < Execution_Time <= 30;')
    t2 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 30 < Execution_Time <= 90;')
    t3 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 90 < Execution_Time;')
    t4 = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()
    return {'res': [['Status', 'Num'], ['[0, 10]', t1], ['(10, 30]', t2], ['(30, 90]', t3], ['(90, inf)', t4]]}

@app.route('/getDetailedStatisticsOfUniversity', methods=['GET', 'POST'])
def get_detailed_statistics_of_university():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    if len(data) == 0:
        return {'department': []}
    q = data['university'].split('. ')

    mycursor.execute('SELECT count(*) from Faculty_History where Execution_Time <= 10 and University_ID = "{}";'.format(q[0]))
    t1 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 10 < Execution_Time <= 30 and University_ID = "{}";'.format(q[0]))
    t2 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 30 < Execution_Time <= 90 and University_ID = "{}";'.format(q[0]))
    t3 = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) from Faculty_History where 90 < Execution_Time and University_ID = "{}";'.format(q[0]))
    t4 = mycursor.fetchone()[0]
    table1 = [['Status', 'Num'], ['[0, 10]', t1], ['(10, 30]', t2], ['(30, 90]', t3], ['(90, inf)', t4]]

    mycursor.execute('select a.Department_Name, count(*) from ((select * from Faculty_History where University_ID = "{}") a natural join Faculty) group by a.Department_Name;'.format(q[0]))
    r = mycursor.fetchall()
    l = []
    # 0-20, 20-50, 50-100, 100-inf
    n1, n2, n3, n4 = 0, 0, 0, 0
    for i in r:
        l.append([i[1], i[0]])
        if 0 <= i[1] <= 20:
            n1 += 1
        elif 20 < i[1] <= 50:
            n2 += 1
        elif 50 < i[1] <= 100:
            n3 += 1
        else:
            n4 += 1
    mycursor.execute('select count(*) from Faculty_History where University_ID = "{}" and Status = "Fail";'.format(q[0]))
    fail = mycursor.fetchone()[0]
    table2 = [['Status', 'Num'], ['[0, 20]', n1], ['(20, 50]', n2], ['(50, 100]', n3], ['(100, inf)', n4], ['Fail', fail]]

    l.sort(reverse=True)
    table3 = [['Department', '# Faculty']]
    for i in range(10):
        table3.append(l[i][::-1])
    print(table3)

    mycursor.close()
    mydb.close()
    return {'table1': table1, 'table2': table2, 'table3': table3}

@app.route('/getNextTasks', methods=['GET', 'POST'])
def get_next_tasks():
    mydb, mycursor = connect_to_mysql()
    mycursor.execute('select University_ID, Department_Name, Priority from Faculty_Tasks order by Priority asc, University_ID asc, Department_Name asc;')
    r = mycursor.fetchall()
    res = []
    n = 2 ** 31 - 1
    data = json.loads(request.data)
    num = data['page']
    university = data['university']
    department = data['department']

    if not (len(university) == 0 or university == 'All'):
        id = int(university[:university.find('.')])
        r1 = []
        for i in r:
            if i[0] == id:
                r1.append(i)
        r = r1.copy()
    
    if not (len(department) == 0 or department == 'All'):
        r1 = []
        for i in r:
            if department in i[1]:
                r1.append(i)
        r = r1.copy()

    if len(r) <= 50 * (num - 1):
        return {'res': []}

    for i in range(50 * (num - 1), min(50 * num, len(r))):
        mycursor.execute('select University_Name from University where University_ID = {};'.format(r[i][0]))
        university = mycursor.fetchone()[0]
        department = r[i][1]
        if r[i][2] == -2147483648:
            department += ' (Pending)'
        res.append([str(r[i][0]) + '. ' + university, department])
    mycursor.close()
    mydb.close()
    return {'res': res}

@app.route('/prioritizeTasks', methods=['GET', 'POST'])
def prioritize_tasks():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    table = data['table']
    mycursor.execute('select min(Priority) from Faculty_Tasks where Priority > -2147483648;')
    n = mycursor.fetchone()[0]
    for i in table[::-1]:
        if len(i) == 3 and i[-1]:
            n -= 1
            id = i[0][:i[0].find('.')]
            department = i[1]
            if ' (Pending)' in department:
                department = department[:-10]
            mycursor.execute('update Faculty_Tasks set Priority = {} where University_ID = "{}" and Department_Name = "{}"'.format(n - 1, id, department))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {}

@app.route('/prioritizeAll', methods=['GET', 'POST'])
def prioritize_all():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    university = data['university']
    department = data['department']
    if university in ['', 'All'] and department in ['', 'All']:
        mycursor.close()
        mydb.close()
        return {}
    
    mycursor.execute('select University_ID, Department_Name, Priority from Faculty_Tasks order by Priority asc, University_ID asc, Department_Name asc;')
    r = mycursor.fetchall()
    if not (len(university) == 0 or university == 'All'):
        id = int(university[:university.find('.')])
        r1 = []
        for i in r:
            if i[0] == id:
                r1.append(i)
        r = r1.copy()
    if not (len(department) == 0 or department == 'All'):
        r1 = []
        for i in r:
            if department in i[1]:
                r1.append(i)
        r = r1.copy()

    mycursor.execute('select min(Priority) from Faculty_Tasks where Priority > -2147483648;')
    n = mycursor.fetchone()[0]
    for i in r[::-1]:
        n -= 1
        mycursor.execute('update Faculty_Tasks set Priority = {} where University_ID = {} and Department_Name = "{}"'.format(n - 1, i[0], i[1]))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {}

@app.route('/deleteTasks', methods=['GET', 'POST'])
def delete_tasks():
    mydb, mycursor = connect_to_mysql()
    data = json.loads(request.data)
    university_id = int(data['university'].split('. ')[0])
    department = data['department']
    n = 2 ** 31 - 1
    if len(department) > 1:
        mycursor.execute('update Faculty_Tasks set Priority = {} where University_ID = "{}" and Department_Name = "{}"'.format(n, university_id, department))
    else:
        mycursor.execute('update Faculty_Tasks set Priority = {} where University_ID = "{}"'.format(n, university_id))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {}


if __name__ == "__main__":
    # flask run --host=0.0.0.0 --port=3113
    app.run(host = '172.22.224.119', port=3113)
