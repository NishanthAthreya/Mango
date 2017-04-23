import os
from flask import Flask, render_template, request, url_for, send_from_directory
import pymysql.cursors
from flask_login import LoginManager, login_required, UserMixin

login_manager = LoginManager()
app = Flask(__name__)
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
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/')
def home():
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute("INSERT INTO user (email, pwd) VALUES (%s, %s)", ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM user"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        return render_template('index.html')


app.run(host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)))
