import os
from flask import Flask, render_template, request, url_for, send_from_directory, redirect, json, jsonify
import pymysql.cursors
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)

hackru_pass = os.environ['HACKRU_PASS']
hackru_host = os.environ['HACKRU_HOST']
app.secret_key = os.environ['app_secret_key']


connection = pymysql.connect(host=hackru_host,
                             user='mango',
                             password=hackru_pass,
                             db='mangodb')


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    with connection.cursor() as cursor:
        rows = cursor.execute("SELECT * FROM users WHERE email='{}'".format(email))
    if rows == 0:
        return None
    user = User()
    user.id = email
    return user

@app.route('/explore')
@login_required
def explore():
    return render_template('explore.html');

@app.route("/create", methods=['POST'])
def create():
    email = request.form['email']
    print(email)
    firstname = request.form['first-name']
    lastname = request.form['last-name']
    major = request.form['major']
    educ_level = request.form['educ_level']
    phone = request.form['phone-number']
    password = request.form['password']
    line = "'" + email+ "','"+firstname + "','" + lastname + "','" + major + "','" + educ_level + "','" + phone + "','" + password + "'"
    print(educ_level)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users(email, firstname, lastname, major, educ_level, phone, password)values("
                       + "{})".format(line))
    connection.commit()
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email='{}'".format(email))
        row = cursor.fetchone()
    if (row is None) or (request.form['password'] != row[6]):
        return json.dumps({'status':'fail','username':email,'password':request.form['password']}); # testing
    user = User()
    user.id = email
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/signup')
def signup():
    return render_template('signup.html');    

@app.route('/dashboard')
@login_required
def dashboard():
    with connection.cursor() as cursor:
        cursor.execute("SELECT dept_id,tutor,cid FROM tutoruser WHERE student='{}'".format(current_user.id))
        rows = cursor.fetchall()
        is_student = []
        for i in range(len(rows)):
            is_student.append([rows[i][0],rows[i][1],rows[i][2]])
            cursor.execute("SELECT name FROM courses WHERE cid='{}'".format(rows[i][2]) + " AND dept_id='{}'".format(rows[i][0]))
            is_student[i][2] = cursor.fetchone()[0]
            cursor.execute("SELECT firstname,lastname FROM users WHERE email='{}'".format(current_user.id))
            full_student = cursor.fetchone()
            is_student[i][0] = full_student[0] + " " + full_student[1]

        cursor.execute("SELECT dept_id,student,cid FROM tutoruser WHERE tutor='{}'".format(current_user.id))
        rows = cursor.fetchall()
        is_tutor = []
        for i in range(len(rows)):
            is_tutor.append([rows[i][0], rows[i][1], rows[i][2]])
            cursor.execute("SELECT name FROM courses WHERE cid='{}'".format(rows[i][2]) + " AND dept_id='{}'".format(rows[i][0]))
            is_tutor[i][2] = cursor.fetchone()[0]
            cursor.execute("SELECT firstname,lastname FROM users WHERE email='{}'".format(current_user.id))
            full_tutor = cursor.fetchone()
            is_tutor[i][0] = full_tutor[0] + " " + full_tutor[1]
    return render_template('dashboard.html', learning_list=is_student, teaching_list=is_tutor)


@app.route('/willtutor', methods=['GET', 'POST'])
def willtutor():
    if request.method == 'GET':
        return '''
                <form action = 'available' method='POST'>
                <table>
                    <tr><td><input type='text' name='dept_id' id='dept_id' placeholder='department id'></input></td></tr>
                    <tr><td><input type='text' name='cid' id='cid' placeholder='course id'></input></td></tr>
                </table>
                <input type='submit' name='submit'></input>
                </form>
                '''
    email = current_user.id
    cid = request.form['cid']
    dept_id = request.form['dept_id']
    line = "'" + email + "','" + cid + "','" + dept_id + "'"
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO available(tutor, cid, dept_id)values({})".format(line))
    connection.commit()
    return render_template("index.html");

@app.route('/availabletutors', methods=['GET'])
def available():
    cid = request.args.get('cid')
    dept_id = request.args.get('dept_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available WHERE cid={}".format(cid) + " and dept_id={}".format(dept_id))
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'GET':
        return '''
                <form action = 'connect' method='POST'>
                <table>
                    <tr><td><input type='text' name='dept_id' id='dept_id' placeholder='department id'></td></tr>
                    <tr><td><input type='text' name='cid' id='cid' placeholder='course id'></td></tr>
                    <tr><td><input type='text' name='tutor' id='tutor' placeholder='tutor email'>
                </table>
                <input type='submit' name='submit'></input>
                </form>
                '''
    student = current_user.id
    dept_id = request.form['dept_id']
    cid = request.form['cid']
    tutor = request.form['tutor']
    line = "'" + tutor + "','" + student + "','" + cid + "','" + dept_id + "'"
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO tutoruser(tutor, student, cid, dept_id)values({})".format(line))
    connection.commit()
    return render_template('index.html')

@app.route('/departments', methods=['GET'])
def get_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT dept_id,dept_name FROM courses")
    rows = cursor.fetchall()
    return jsonify(rows);

@app.route('/courses', methods=['GET'])
def get_courses():
    dept_id = request.args.get('deptid')
    with connection.cursor() as cursor:
        cursor.execute("SELECT cid,name FROM courses WHERE dept_id={}".format(dept_id))
    rows = cursor.fetchall()
    return jsonify(rows);


@app.route('/protected')
@login_required
def testing():
    return render_template('testing.html')

@app.route('/')
def home():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)