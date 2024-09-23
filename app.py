from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="cinema", host="localhost", user="postgres", password="root", port="5432")
    return conn

@app.route('/')
def home():
    return "Welcome to the Home Page! Navigate to /employee to see employee data."

@app.route('/employee')
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employee ORDER BY emp_id;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/create',methods=['POST'])
def create():
    conn=db_conn()
    cur=conn.cursor()
    emp_id=request.form['emp_id']
    salary=request.form['salary']
    birth_date=request.form['birth_date']
    age=request.form['age']
    first_name=request.form['first_name']
    middle_name=request.form['middle_name']
    last_name=request.form['last_name']
    gender=request.form['gender']
    email_id=request.form['email_id']
    phone_no=request.form['phone_no']
    cur.execute('''INSERT INTO employee 
               (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
               (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cur = conn.cursor()

    emp_id = request.form['emp_id']
    salary = request.form['salary']
    birth_date = request.form['birth_date']
    age = request.form['age']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    email_id = request.form['email_id']
    phone_no = request.form['phone_no']

    cur.execute('''UPDATE employee 
                   SET salary = %s, birth_date = %s, age = %s, first_name = %s, middle_name = %s, 
                       last_name = %s, gender = %s, email_id = %s, phone_no = %s 
                   WHERE emp_id = %s''',
                (salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no, emp_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cur = conn.cursor()
    emp_id = request.form['emp_id']
    cur.execute('''DELETE FROM employee WHERE emp_id = %s''', (emp_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)