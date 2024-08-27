
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
            document.getElementById('current-date').textContent = now.toDateString();
        }

        setInterval(updateTime, 1000);
        updateTime();
        const dayOrders = {
            '2024-08-01': 'A6',
            '2024-08-02': 'B',
            '2024-08-05': 'C LSM-I',
            '2024-08-06': 'D',
            '2024-08-07': 'E CIA-I-P Begins',
            '2024-08-08': 'F',
            '2024-08-09': 'A7',
            '2024-08-12': 'B',
            '2024-08-13': 'C CIA-I-P Ends',
            '2024-08-14': 'D LSQ-II',
            '2024-08-19': 'E',
            '2024-08-20': 'F',
            '2024-08-21': 'A8',
            '2024-08-22': 'B',
            '2024-08-23': 'C',
            '2024-08-24': 'D',
            '2024-08-27': 'E CIA-II Begins',
            '2024-08-28': 'F',
            '2024-08-29': 'A9',
            '2024-08-30': 'B',
            '2024-09-02': 'C',
            '2024-09-03': 'D',
            '2024-09-05': 'F CIA- Ends',
            '2024-09-06': 'A10',
            '2024-09-09': 'B Ph.D. C.W-I',
            '2024-09-10': 'C Ph.D. C.W-I',
            '2024-09-11': 'D Ph.D. C.W-I',
            '2024-09-12': 'E',
            '2024-09-13': 'F LSQ-III',
            '2024-09-16': 'A11',
            '2024-09-17': 'B',
            '2024-09-18': 'C',
            '2024-09-19': 'D',
            '2024-09-20': 'E Ph.D. C.W-II',
            '2024-09-21': 'F Ph.D. C.W-II',
            '2024-09-23': 'A12',
            '2024-09-24': 'B',
            '2024-09-25': 'C Ph.D. C.W-II',
            '2024-09-26': 'D',
            '2024-09-27': 'E',
            '2024-09-28': 'F',
            '2024-09-30': 'A13',
            '2024-10-01': 'B',
            '2024-10-03': 'D',
            '2024-10-04': 'E Ph.D. C.W-III',
            '2024-10-07': 'F Ph.D. C.W-III',
            '2024-10-08': 'A14',
            '2024-10-09': 'B Ph.D. C.W-III',
            '2024-10-10': 'C',
            '2024-10-11': 'D',
            '2024-10-14': 'E',
            '2024-10-15': 'F',
            '2024-10-16': 'A15',
            '2024-10-17': 'B',
            '2024-10-18': 'C',
            '2024-10-21': 'D',
            '2024-10-22': 'E',
            '2024-10-23': 'F',
            '2024-10-24': 'A16',
            '2024-10-25': 'B',
            '2024-10-26': 'C',
            '2024-10-28': 'D',
            '2024-10-29': 'E CIA-III-P Begins',
            '2024-10-30': 'F',
            '2024-10-31': 'A17',
            '2024-11-01': 'B',
            '2024-11-02': 'C',
            '2024-11-04': 'D CIA-III-P Ends',
            '2024-11-05': 'E',
            '2024-11-06': 'F',
            '2024-11-07': 'A18',
            '2024-11-08': 'B',
            '2024-11-11': 'C LSQ-IV',
            '2024-11-12': 'D',
            '2024-11-13': 'E',
            '2024-11-14': 'F',
            '2024-11-15': 'A19',
            '2024-11-16': 'B',
            '2024-11-18': 'C',
            '2024-11-19': 'D',
            '2024-11-20': 'E',
            '2024-11-21': 'F',
            '2024-11-22': 'A20',
            '2024-11-23': 'B',
            '2024-11-25': 'C',
            '2024-11-26': 'D',
            '2024-11-27': 'E',
            '2024-11-28': 'F',
            '2024-11-29': 'A21',
            '2024-11-30': 'B',
            '2024-12-02': 'C LSQ-V',
            '2024-12-03': 'D',
            '2024-12-04': 'E',
            '2024-12-05': 'F',
            '2024-12-06': 'A22',
            '2024-12-07': 'B',
            '2024-12-09': 'C',
            '2024-12-10': 'D',
            '2024-12-11': 'E CIA-IV-P Begins',
            '2024-12-12': 'F',
            '2024-12-13': 'A23',
            '2024-12-14': 'B',
            '2024-12-16': 'C CIA-IV-P Ends',
            '2024-12-17': 'D',
            '2024-12-18': 'E',
            '2024-12-19': 'F',
            '2024-12-20': 'A24',
            '2024-12-21': 'B',
            '2024-12-23': 'C',
            '2024-12-24': 'D',
            '2024-12-26': 'E',
            '2024-12-27': 'F',
            '2024-12-28': 'A25',
            '2024-12-30': 'B',
            '2024-12-31': 'C',
            '2025-01-02': 'D',
            '2025-01-03': 'E',
            '2025-01-04': 'F',
            '2025-01-06': 'A26',
            '2025-01-07': 'B',
            '2025-01-08': 'C',
            '2025-01-09': 'D',
            '2025-01-10': 'E',
            '2025-01-11': 'F',
            '2025-01-13': 'A27',
            '2025-01-14': 'B',
            '2025-01-15': 'C',
            '2025-01-16': 'D',
            '2025-01-17': 'E',
            '2025-01-18': 'F',
            '2025-01-20': 'A28',
            '2025-01-21': 'B',
            '2025-01-22': 'C',
            '2025-01-23': 'D',
            '2025-01-24': 'E',
            '2025-01-25': 'F',
            '2025-01-27': 'A29',
            '2025-01-28': 'B',
            '2025-01-29': 'C',
            '2025-01-30': 'D',
            '2025-01-31': 'E',
            '2025-02-01': 'F',
            '2025-02-03': 'A30',
            '2025-02-04': 'B',
            '2025-02-05': 'C',
            '2025-02-06': 'D',
            '2025-02-07': 'E',
            '2025-02-08': 'F',
            '2025-02-10': 'A31',
            '2025-02-11': 'B',
            '2025-02-12': 'C',
            '2025-02-13': 'D',
            '2025-02-14': 'E',
            '2025-02-15': 'F',
            '2025-02-17': 'A32',
            '2025-02-18': 'B',
            '2025-02-19': 'C',
            '2025-02-20': 'D',
            '2025-02-21': 'E',
            '2025-02-22': 'F',
            '2025-02-24': 'A33',
            '2025-02-25': 'B',
            '2025-02-26': 'C',
            '2025-02-27': 'D',
            '2025-02-28': 'E',
            '2025-03-01': 'F',
            '2025-03-03': 'A34',
            '2025-03-04': 'B',
            '2025-03-05': 'C',
            '2025-03-06': 'D',
            '2025-03-07': 'E',
            '2025-03-08': 'F',
            '2025-03-10': 'A35',
            '2025-03-11': 'B',
            '2025-03-12': 'C',
            '2025-03-13': 'D',
            '2025-03-14': 'E',
            '2025-03-15': 'F',
            '2025-03-17': 'A36',
            '2025-03-18': 'B',
            '2025-03-19': 'C',
            '2025-03-20': 'D',
            '2025-03-21': 'E',
            '2025-03-22': 'F',
            '2025-03-24': 'A37',
            '2025-03-25': 'B',
            '2025-03-26': 'C',
            '2025-03-27': 'D',
            '2025-03-28': 'E',
            '2025-03-29': 'F',
            '2025-04-01': 'A38',
            '2025-04-02': 'B',
            '2025-04-03': 'C',
            '2025-04-04': 'D',
            '2025-04-05': 'E',
            '2025-04-07': 'F',
            '2025-04-08': 'A39',
            '2025-04-09': 'B',
            '2025-04-10': 'C',
            '2025-04-11': 'D',
            '2025-04-12': 'E',
            '2025-04-15': 'F',
            '2025-04-16': 'A40',
            '2025-04-17': 'B',
            '2025-04-18': 'C',
            '2025-04-21': 'D',
            '2025-04-22': 'E',
            '2025-04-23': 'F',
            '2025-04-24': 'A41',
            '2025-04-25': 'B',
            '2025-04-26': 'C',
            '2025-04-28': 'D',
            '2025-04-29': 'E',
            '2025-04-30': 'F',
            '2025-05-01': 'A42',
            '2025-05-02': 'B',
            '2025-05-03': 'C',
            '2025-05-05': 'D',
            '2025-05-06': 'E',
            '2025-05-07': 'F',
            '2025-05-08': 'A43',
            '2025-05-09': 'B',
            '2025-05-10': 'C',
            '2025-05-12': 'D',
            '2025-05-13': 'E',
            '2025-05-14': 'F',
            '2025-05-15': 'A44',
            '2025-05-16': 'B',
            '2025-05-17': 'C',
            '2025-05-19': 'D',
            '2025-05-20': 'E',
            '2025-05-21': 'F',
            '2025-05-22': 'A45',
            '2025-05-23': 'B',
            '2025-05-24': 'C',
            '2025-05-26': 'D',
            '2025-05-27': 'E',
            '2025-05-28': 'F',
            '2025-05-29': 'A46',
            '2025-05-30': 'B',
            '2025-05-31': 'C'
        };

        const today = new Date().toISOString().split('T')[0];
        const dayOrder = dayOrders[today];
        document.getElementById('day-order').textContent = dayOrder || 'No Classes Today';
