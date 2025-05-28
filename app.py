# app.py
from flask import Flask, render_template
from flask_mysqldb import MySQL
from db_config import db_config

app = Flask(__name__)

# Configure DB
app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']

mysql = MySQL(app)

@app.route('/')
def home():
    return '<h1>Welcome to the Fitness Tracker!</h1><p>Visit /users to see users</p>'

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, current_weight, goal_weight FROM User")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
