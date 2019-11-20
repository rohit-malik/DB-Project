import psycopg2

try:
    connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
    sql = """INSERT INTO department(department_id,dept_name)
             VALUES(%s,%s)"""
    records = (1,"Farji")
    
    conn = psycopg2.connect(connect_str)
    
    cursor = conn.cursor()
    
    cursor.execute(sql,records)
    
    #result = cursor.fetchone()[0]
    conn.commit() # <--- makes sure the change is shown in the database
    #rows = cursor.fetchall()
    #print(result)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)


