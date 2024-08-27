document.getElementById('resultForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const regno = document.getElementById('regno').value;
    const exam = document.getElementById('exam').value;
    
    fetch('/get_result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ regno: regno, exam: exam }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error: ' + error.message;
    });
});
