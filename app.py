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

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return '''
            <form action = 'create' method = 'POST'>
                <table>
                    <tr><td><input type='text' name='email' id='email' placeholder='email'></input></td></tr>
                    <tr><td><input type='text' name='firstname' id='firstname' placeholder='first name'></input></td></td>
                    <tr><td><input type='text' name='lastname' id='lastname' placeholder='last-name'></input></td></tr>
                    <tr><td><input type='text' name='major' id='major' placeholder='major(i.e-332)'></input></td></tr>
                    <tr><td><input type='text' name='educ_level' id='educ_level' placeholder='education level'></input></td></tr>
                    <tr><td><input type='text' name='phone' id='phone' placeholder='phone number'></input></td></tr>
                    <tr><td><input type='text' name='password' id='password' placeholder='password'></input></td></tr>
                </table>
                <input type='submit' name='submit'></input>
            </form>
            '''
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    major = request.form['major']
    educ_level = request.form['educ_level']
    phone = request.form['phone']
    password = request.form['password']
    line = "'" + email+ "','"+firstname + "','" + lastname + "','" + major + "','" + educ_level + "','" + phone + "','" + password + "'"
    print(line)
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
    return redirect(url_for('willtutor'))

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

@app.route('/availabletutors', methods=['GET', 'POST'])
def available():
    if request.method == 'GET':
        return '''
                <form action = 'availabletutors' method='POST'>
                <table>
                    <tr><td><input type='text' name='dept_id' id='dept_id' placeholder='department id'></input></td></tr>
                    <tr><td><input type='text' name='cid' id='cid' placeholder='course id'></input></td></tr>
                </table>
                <input type='submit' name='submit'></input>
                </form>
                '''
    cid = request.form['cid']
    dept_id = request.form['dept_id']
    with connection.cursor() as cursor:
        cursor.execute("SELECT available.tutor FROM available WHERE cid='{}'".format(cid) + " and dept_id='{}'".format(dept_id))
        row = cursor.fetchone()
    print(row[0])
    return render_template('index.html')

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

@app.route('/courses', methods=['GET'])
def get_courses():
    dept_id = request.args.get('deptid')
    print(dept_id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM courses WHERE dept_id='{}'".format(dept_id))
    rows = cursor.fetchall()
    print(rows)
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