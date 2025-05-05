from sqlalchemy.sql import text
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, ProgrammingError
import mysql.connector
from mysql.connector import errorcode
import os
import time

# Указываем путь к папке шаблонов и статических файлов
template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+mysqlconnector://root:123@db/db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

def create_database():
    max_retries = 10
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host='db',
                user='root',
                password='123'
            )
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            if 'db' not in databases:
                cursor.execute("CREATE DATABASE db")
                print("Database 'db' created successfully.")
            else:
                print("Database 'db' already exists.")
            cursor.close()
            conn.close()
            break
        except mysql.connector.Error as err:
            print(f"Attempt {attempt + 1}/{max_retries}: Error connecting to MySQL: {err}")
            time.sleep(retry_delay)
    else:
        print("Failed to connect to MySQL after several attempts.")
        raise

def create_tables():
    try:
        with app.app_context():
            db.create_all()
            print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
create_tables()
def initialize_database():
         max_retries = 10
         retry_delay = 5
         for attempt in range(max_retries):
             try:
                 with app.app_context():
                     db.session.execute(text("SELECT 1"))
                     print("Database connection successful.")
                     return
             except (OperationalError, ProgrammingError) as e:
                 print(f"Attempt {attempt + 1}/{max_retries}: Database connection failed: {e}")
                 if attempt == max_retries - 1:
                     print("Failed to connect to MySQL after several attempts.")
initialize_database()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        try:
            db.session.add(user)
            db.session.commit()
        except (OperationalError, ProgrammingError) as e:
            print(f"Error adding user: {e}")
            create_database()
            create_tables()
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        print(f"User {user_id} deleted successfully.")
    except (OperationalError, ProgrammingError) as e:
        print(f"Error deleting user: {e}")
        create_database()
        create_tables()
        db.session.delete(user)
        db.session.commit()
    
    return redirect(url_for('home'))
if __name__ == '__main__':
         initialize_database()
         app.run(host='0.0.0.0', port=5000, debug=True)