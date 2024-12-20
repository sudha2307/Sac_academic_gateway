import requests
from bs4 import BeautifulSoup

def get_results(reg_no, exam):
    url = "https://results.sadakath.ac.in/ResultPage.aspx"
    payload = {
        '__VIEWSTATE': '/wEPDwUJNzE3NDI4OTM5D2QWAgIBD2QWAgIDDxBkDxYBZhYBEAUITm92IDIwMjQFCE5vdiAyMDI0Z2RkZIR/zXQeTg+jyVZbtMreusymyMQ4',
        '__VIEWSTATEGENERATOR': '7C3C6012',
        '__EVENTVALIDATION': '/wEdAARzN7bZtmqtQXfSWIF0CIprZS6BASrBkr5QeAzZHQV1+txSYZLFsAialTI1fBLjIvnN+DvxnwFeFeJ9MIBWR693ivjs57FeIsSCjQoYF9sSNQrUVAY=',
        'TxtRegno': reg_no,
        'CMbExam': exam,
        'Button1': 'Submit'
    }

    response = requests.post(url, data=payload, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Parsing the result page
    results_table = soup.find('table', id='GridView1')
    if results_table:
        results = []
        rows = results_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            columns = row.find_all('td')
            result = {
                'sub_code': columns[0].text.strip(),
                'sub_name': columns[1].text.strip(),
                'int_mark': columns[2].text.strip(),
                'ext_mark': columns[3].text.strip(),
                'total': columns[4].text.strip(),
                'result': columns[5].text.strip()
            }
            results.append(result)
        return results
    else:
        return None
