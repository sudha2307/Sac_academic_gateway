import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scrape_results import get_results  # Ensure this is correctly implemented or adjust as needed
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://SAC-DATA_owner:uiLaEU68gpOz@ep-royal-mouse-a1x46r4p.ap-southeast-1.aws.neon.tech/SAC-DATA?sslmode=require'

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
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    avatar = db.Column(db.String(150), nullable=True,default ='static/avatars/avatar5.jpg')  # Field to store avatar filename

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to create tables
def create_tables():
    with app.app_context():
        db.create_all()

# Function to fetch hidden fields
def fetch_hidden_fields(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
    
    return viewstate, viewstate_generator, event_validation

# Function to scrape attendance from the website
def scrape_attendance(reg_no):
    url = "https://sadakath.ac.in/attend/attendance3.aspx"
    
    # Simulating a request to get the page
    session = requests.Session()
    response = session.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to access the attendance page"}
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the attendance form
    viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
    event_validation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

    # Data for POST request (form submission)
    payload = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": event_validation,
        "txtRegno": reg_no,
        "btnView": "View Attendance"
    }

    # Submit the form with the registration number
    response = session.post(url, data=payload)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch attendance data"}

    # Parse the response
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"id": "attendanceTable"})  # Adjust the ID based on actual table structure

    if not table:
        return {"error": "No attendance data found"}

    # Extract data from table rows
    rows = table.find_all("tr")[1:]  # Skipping header row
    attendance_records = []

    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 7:
            continue  # Skip invalid rows
        
        record = {
            "RegNo": reg_no,
            "SubCode": columns[0].text.strip(),
            "Total": columns[1].text.strip(),
            "Present": columns[2].text.strip(),
            "Absent": columns[3].text.strip(),
            "OD": columns[4].text.strip(),
            "Total_Present": columns[5].text.strip(),
            "Present_Percentage": columns[6].text.strip(),
        }
        attendance_records.append(record)

    return {
        "AdminNo": reg_no,
        "Name": f"Student {reg_no}",
        "Records": attendance_records
    }



# Function to get attendance details
def get_attendance_details(url, reg_no, viewstate, viewstate_generator, event_validation):
    payload = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstate_generator,
        '__EVENTVALIDATION': event_validation,
        'TxtRegno': reg_no,
        'Button1': 'Submit'
    }
    
    response = requests.post(url, data=payload)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    result = {}
    result['AdminNo'] = soup.find('span', {'id': 'Label1'}).text.strip()
    result['Name'] = soup.find('span', {'id': 'Label2'}).text.strip()
    
    table = soup.find('table', {'id': 'GridView1'})
    if table:
        rows = table.find_all('tr')[1:]
        result['Records'] = []
        for row in rows:
            columns = row.find_all('td')
            record = {
                'CCode': columns[0].text.strip(),
                'Semno': columns[1].text.strip(),
                'RegNo': columns[2].text.strip(),
                'AdmnNo': columns[3].text.strip(),
                'SName': columns[4].text.strip(),
                'Total': columns[5].text.strip(),
                'Present': columns[6].text.strip(),
                'Absent': columns[7].text.strip(),
                'OD': columns[8].text.strip(),
                'Percentage': columns[9].text.strip()
            }
            result['Records'].append(record)
    
    return result
# Route to fetch student name based on registration number
@app.route('/get_student_name', methods=['POST'])
def get_student_name():
    reg_number = request.json.get('reg_number').upper()

    # Fetch attendance details to get the student name
    attendance_details = get_attendance_details(
        'https://sadakath.ac.in/attend/attendance2.aspx',
        reg_number,
        *fetch_hidden_fields('https://sadakath.ac.in/attend/attendance2.aspx')
    )
    student_name = attendance_details.get('Name', 'Unknown')  # Extract student name

    return jsonify({'student_name': student_name})

# Home route
@app.route('/')
def home():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Convert username to uppercase to match registration
        username = request.form['username'].upper()
        password = request.form['password']
        
        # Query the user from the database using the uppercase username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password matches
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
    student_name = ''
    
    if request.method == 'POST':
        # Extract form data
        reg_number = request.form['username'].upper()  # Assuming username is the registration number
        password = request.form['password']
        department = request.form['department']
        avatar = request.form.get('avatar', 'default.jpeg')  # Default avatar if none is selected
        
        # Fetch attendance details to get the student name
        attendance_details = get_attendance_details(
            'https://sadakath.ac.in/attend/attendance2.aspx',
            reg_number,
            *fetch_hidden_fields('https://sadakath.ac.in/attend/attendance2.aspx')
        )
        student_name = attendance_details.get('Name', 'Unknown')  # Extract student name

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the user already exists
        existing_user = User.query.filter_by(username=reg_number).first()
        if existing_user:
            flash('Username already exists!', 'error')
            return render_template('register.html', student_name=student_name)

        # Create a new user with the selected avatar
        new_user = User(name=student_name, username=reg_number, password=hashed_password, department=department, avatar=avatar)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', student_name=student_name)
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch current time and avatar
    current_time = datetime.datetime.now()
    
    # If the user has an avatar, use it; otherwise, use the default avatar
    avatar_filename = current_user.avatar or 'default.jpeg'
    avatar_url = url_for('static', filename=f'avatars/{avatar_filename}')

    # Fetch attendance details
    try:
        attendance_details = get_attendance_details(
            'https://sadakath.ac.in/attend/attendance2.aspx', 
            current_user.username, 
            *fetch_hidden_fields('https://sadakath.ac.in/attend/attendance2.aspx')
        )
    except Exception as e:
        attendance_details = None

    # Process attendance records
    if attendance_details and 'Records' in attendance_details:
        total_present = sum(float(record.get('Present', 0)) for record in attendance_details['Records'])
        total_absent = sum(float(record.get('Absent', 0)) for record in attendance_details['Records'])
        total_od = sum(float(record.get('OD', 0)) for record in attendance_details['Records'])
    else:
        total_present = total_absent = total_od = "-"

    # Render the dashboard template with the required data
    return render_template('dashboard.html', 
                           name=current_user.name, 
                           username=current_user.username, 
                           department=current_user.department, 
                           current_time=current_time, 
                           avatar_url=avatar_url, 
                           total_present=total_present, 
                           total_absent=total_absent, 
                           total_od=total_od)

# Update avatar route
@app.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    user = current_user
    response = {'success': False}

    # Handle file upload
    if 'avatarUpload' in request.files:
        file = request.files['avatarUpload']
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


# Results route
@app.route('/result')
def index():
    return render_template('result_ui.html')

@app.route('/get_result', methods=['POST'])
def get_result():
    reg_no = request.form.get('reg_no')
    exam = request.form.get('exam')
    results = get_results(reg_no, exam)
    if results:
        return jsonify(results)  # Convert results to JSON
    else:
        return jsonify([]), 404
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

# Combined attendance results route
@app.route('/attendance', methods=['POST'])
def attendance():
    try:
        data = request.get_json()  # Get JSON request body
        reg_no = data.get('reg_no') if data else None  # Extract 'reg_no' from JSON

        if not reg_no:
            return jsonify({"error": "Missing roll number"}), 400  # Handle missing roll number

        url = 'https://sadakath.ac.in/attend/attendance2.aspx'
        viewstate, viewstate_generator, event_validation = fetch_hidden_fields(url)

        # Debugging logs
        print(f"Fetching attendance for: {reg_no}")
        print(f"Hidden Fields: {viewstate}, {viewstate_generator}, {event_validation}")

        attendance_details = get_attendance_details(url, reg_no, viewstate, viewstate_generator, event_validation)

        print(f"Attendance details fetched: {attendance_details}")  # Log the response

        return jsonify(attendance_details)  # Return JSON response

    except Exception as e:
        print(f"Error fetching attendance: {e}")  # Log error details
        return jsonify({"error": str(e)}), 500  # Return detailed error

# Flask API Route
@app.route('/attendance_1st_year', methods=['POST'])
def attendance_1st_year():
    try:
        data = request.get_json()
        reg_no = data.get("reg_no", "").strip()

        if not reg_no:
            return jsonify({"error": "Registration number is required"}), 400

        attendance_data = scrape_attendance(reg_no)
        if "error" in attendance_data:
            return jsonify(attendance_data), 404
        
        return jsonify(attendance_data)

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

   

# Main entry point
if __name__ == '__main__':
    create_tables()  # Create tables if they don't exist
    app.run(debug=True)
