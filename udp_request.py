import socket
import sqlite3

# Create a function to connect to a database with SQLite
def sqlite_connect(db_name):
    """Connect to a database if exists. Create an instance if otherwise.
    Args:
        db_name: The name of the database to connect
    Returns:
        an sqlite3.connection object
    """
    try:
        # Create a connection
        conn = sqlite3.connect(db_name)
    except sqlite3.Error:
        print(f"Error connecting to the database '{db_name}'")
    finally:
        return conn

UDP_IP = '149.171.37.142'
UDP_PORT = 5000
MESSAGE = b'studentmarklist\0'

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

allInfo_origin, addr = sock.recvfrom(2048)

allInfo = allInfo_origin.decode()
print(allInfo)

num_students = int(allInfo[0:4])

connection = sqlite_connect('studentmarklist.db')
cursor = connection.cursor()
sql_create_table_query = """
CREATE TABLE IF NOT EXISTS studentinfo (student_name TEXT NOT NULL, student_mark BLOB);
"""
cursor.execute(sql_create_table_query)
sql_create_table_query = """
CREATE TABLE IF NOT EXISTS num_students (lable TEXT NOT NULL, num_of_students BLOB);
"""
cursor.execute(sql_create_table_query)
connection.commit()
connection.close()

student_dictionary = {}
student_dictionary["number of students"] = num_students

connection = sqlite_connect('studentmarklist.db')
connection.execute("insert into num_students(lable, num_of_students) values(?, ?)", ("num_of_students", num_students))

for i in range(0,num_students):
    current_value = 4+i*20
    student_name = allInfo[current_value:current_value+16]
    student_name = student_name.replace('\x00','')
    student_mark = int(allInfo[current_value+16:current_value+20])
    student_dictionary[student_name] = student_mark
    connection.execute("insert into studentinfo(student_name, student_mark) values(?, ?)", (student_name, student_mark))

connection.commit()
connection.close()

print(student_dictionary)

