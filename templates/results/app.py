from flask import Flask, render_template, request
from login.scrape_results import get_results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('result_ui.html')

@app.route('/get_result', methods=['POST'])
def get_result():
    reg_no = request.form.get('reg_no')
    exam = request.form.get('exam')
    results = get_results(reg_no, exam)
    return render_template('result.html', results=results)
                            

if __name__ == '__main__':
    app.run(debug=True)
