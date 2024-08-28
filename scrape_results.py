import requests
from bs4 import BeautifulSoup

def get_results(reg_no, exam):
    url = "https://results.sadakath.ac.in/ResultPage00.aspx"
    payload = {
        '__VIEWSTATE': '/wEPDwUJNzE3NDI4OTM5D2QWAgIBD2QWAgIDDxBkDxYBZhYBEAUIQXByIDIwMjQFCEFwciAyMDI0Z2RkZNfhH8TAPGj+jNfJu9VS+f/Gc6Kc',
        '__VIEWSTATEGENERATOR': 'C3B21792',
        '__EVENTVALIDATION': '/wEdAARWB15LHIeDcKWh0+c980mhZS6BASrBkr5QeAzZHQV1+vfYVcBQlI6FF9YVpRBGMujN+DvxnwFeFeJ9MIBWR693rGBNTopC3b6hMkVb8EyTwjjh0tc=',
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
