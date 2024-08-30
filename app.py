from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from scrape_results import get_results

from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use your actual database
db = SQLAlchemy(app)

# User model to store user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)

# Function to create tables
def create_tables():
    with app.app_context():
        db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login Successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
            return redirect(url_for('register'))

        # Hash the password and save the new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, username=username, password=hashed_password, department=department)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    current_time = datetime.datetime.now()
    return render_template('dashboard.html', name=user.name, username=user.username, department=user.department, current_time=current_time)

# Profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You need to log in first', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', name=user.name, username=user.username, department=user.department)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Attendance route
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

# Results route
@app.route('/result')
def index():
    return render_template('result_ui.html')

@app.route('/get_result', methods=['POST'])
def get_result():
    reg_no = request.form.get('reg_no')
    exam = request.form.get('exam')
    results = get_results(reg_no, exam)
    return render_template('result.html', results=results)


# CGPA Calculator route
@app.route('/cgpa_calculator')
def cgpa_calculator():
    return render_template('cgpa_cal.html')

# Time Table route
@app.route('/time_table')
def time_table():
    return render_template('time_table.html')

# Academic Calendar route
@app.route('/academic_calender')
def academic_calender():
    return render_template('academic_calender.html')


if __name__ == '__main__':
    create_tables()  # Create tables if not exist
    app.run(debug=True)
