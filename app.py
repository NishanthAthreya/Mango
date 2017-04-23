import os
from flask import Flask, render_template, request, url_for, send_from_directory, redirect, json
import pymysql.cursors
from flask_login import LoginManager, login_required, UserMixin, login_user

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
    return redirect(url_for('testing'))

@app.route('/protected')
@login_required
def testing():
    return render_template('testing.html')

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)