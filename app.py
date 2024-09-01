import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scrape_results import get_results
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sac_data_user:a7Xx7eWHJXGsxzpRhoFvpMi0bmwe0lwW@dpg-cr8vse5svqrc739hat90-a.singapore-postgres.render.com/sac_data'
app.config['SECRET_KEY'] = '452c455e9533ee85071833a704fa2c97'
app.config['UPLOAD_FOLDER'] = 'static/avatars'

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model to store user information
class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    avatar = db.Column(db.String(150), nullable=True)  # Field to store avatar filename

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            login_user(user)
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
@login_required
def dashboard():
    current_time = datetime.datetime.now()
    avatar_url = url_for('static', filename='avatars/' + current_user.avatar) if current_user.avatar else url_for('static', filename='avatars/download (1).jpeg')
    return render_template('dashboard.html', name=current_user.name, username=current_user.username, department=current_user.department, current_time=current_time, avatar_url=avatar_url)

# Update avatar route
@app.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    user = current_user
    response = {'success': False}

    # Handle file upload
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            user.avatar = filename
            response['success'] = True

    # Handle sample avatar URL
    if 'selected_avatar' in request.form:
        user.avatar = request.form['selected_avatar']
        response['success'] = True

    db.session.commit()
    return jsonify(response)


# Profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, username=current_user.username, department=current_user.department)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
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

# Main entry point
if __name__ == '__main__':
    create_tables()  # Create tables if they don't exist
    app.run(debug=True)
