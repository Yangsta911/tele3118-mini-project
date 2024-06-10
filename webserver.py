from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
import sqlite3

app = Flask(__name__)

def getdata(*args):
    conn = sqlite3.connect('studentmarklist.db')
    cursor = conn.cursor()
    if (len(args) == 0):
        cursor.execute("SELECT * FROM studentinfo;")
    else:
        cursor.execute(f"SELECT * FROM studentinfo WHERE student_name = '{args[0]}';")
    results = cursor.fetchall()
    conn.close
    return results

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/studentlist", methods=['GET','POST'])
def student_list():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    students = getdata()
    print (students)
    return render_template('list.html', usr = students)


@app.route('/api/studentmark/<studentname>', methods=['GET','POST'])
def student(studentname):
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    student = getdata(str(studentname))   
    print (student)      
    return render_template('individual_list.html', usr = student)

