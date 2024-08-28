from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate grade points
def calculate_grade_point(mark):
    if 90 <= mark <= 100:
        return 10
    elif 80 <= mark <= 89:
        return 9
    elif 70 <= mark <= 79:
        return 8
    elif 60 <= mark <= 69:
        return 7
    elif 50 <= mark <= 59:
        return 6
    elif 40 <= mark <= 49:
        return 5
    elif 0 <= mark <= 39:
        return 0
    return None

# Function to calculate CGPA
def calculate_cgpa(subjects):
    total_weighted_marks = 0
    total_credits = 0
    for subject in subjects:
        grade_point = calculate_grade_point(subject['mark'])
        if grade_point == 0:
            return None  # Fail, CGPA can't be calculated
        total_weighted_marks += grade_point * subject['credit']
        total_credits += subject['credit']
    return round(total_weighted_marks / total_credits, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        semester = int(request.form['semester'])  # Get the specific semester
        subjects = []
        
        for i in range(int(request.form[f'total_subjects_sem{semester}'])):
            subject_name = request.form[f'subject_name_sem{semester}_{i}']
            credit = int(request.form[f'credit_sem{semester}_{i}'])
            mark = int(request.form[f'mark_sem{semester}_{i}'])
            subjects.append({'subject_name': subject_name, 'credit': credit, 'mark': mark})

        # Add practicals
        for practical in ['practical1', 'practical2']:
            mark = int(request.form[f'mark_sem{semester}_{practical}'])
            subjects.append({'subject_name': practical, 'credit': 1, 'mark': mark})

        cgpa = calculate_cgpa(subjects)
        if cgpa is None:
            return render_template('index.html', error=f"Failed in Semester {semester}")
        
        total_marks = sum(subject['mark'] for subject in subjects)
        percentage = round((total_marks / (len(subjects) * 100)) * 100, 2)

        return render_template('index.html', semester=semester, cgpa=cgpa, total_marks=total_marks, percentage=percentage)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
