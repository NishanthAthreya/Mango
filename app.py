import os
from flask import Flask, render_template, request, url_for, send_from_directory, redirect
import pymysql.cursors
from flask_login import LoginManager, login_required, UserMixin, login_user

login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = 'super secret string'
login_manager.init_app(app)
hackru_pass = os.environ['HACKRU_PASS']


connection = pymysql.connect(host='mangodb.c3all2cpsbip.us-east-1.rds.amazonaws.com',
                             user='mango',
                             password=hackru_pass,
                             db='mangodb')


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    try:
        with connection.cursor() as cursor:
            rows = cursor.execute("SELECT * FROM users WHERE email={}".format(email))
        if rows == 0:
            return None

        user = User()
        user.id = email
        return user
    except:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    email = request.form['email']
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email='{}'".format(email))
        row = cursor.fetchone()
    if (row is None) or (request.form['pw'] != row[6]):
        return 'bad login'
    user = User()
    user.id = email
    login_user(user, remember=True)
    return render_template('index.html')


@app.route('/')
@login_required
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)