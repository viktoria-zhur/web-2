from flask import Blueprint, request, session, jsonify
import sqlite3
import os
import json

lab6 = Blueprint('lab6', __name__)

def get_db_connection():
    """Подключение к базе данных офисов"""
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect('instance/offices.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed():
    """Инициализировать базу данных если нужно"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER UNIQUE NOT NULL,
            tenant TEXT,
            price INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) as count FROM offices')
    count = cursor.fetchone()['count']
    
    if count == 0:
        for i in range(1, 11):
            cursor.execute(
                'INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)',
                (i, "", 900 + i * 100)
            )
    
    conn.commit()
    conn.close()

@lab6.route('/')
def index():
    css_path = "/static/lab1/lab1.css"
    user = session.get('login')
    
    return f'''<!doctype html>
<html>
<head>
    <title>Лабораторная 6</title>
    <link rel="stylesheet" href="{css_path}">
    <style>
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .user-info {{ background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0; }}
        .btn {{ display: inline-block; padding: 10px 20px; margin: 5px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
        .btn-danger {{ background: #e74c3c; }}
        .btn-success {{ background: #2ecc71; }}
        .offices-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .office-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 10px; }}
        .office-available {{ border-left: 5px solid #2ecc71; }}
        .office-booked {{ border-left: 5px solid #e74c3c; background: #ffe6e6; }}
        .office-number {{ font-size: 1.5em; font-weight: bold; color: #333; }}
        .office-price {{ color: #e74c3c; font-weight: bold; margin: 10px 0; }}
        .office-tenant {{ font-style: italic; color: #666; }}
        .controls {{ margin-top: 10px; }}
    </style>
    <script>
        function sendRPC(method, params) {{
            const data = {{
                jsonrpc: "2.0",
                method: method,
                params: params || {{}},
                id: Date.now()
            }};
            
            fetch('/lab6/api/', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(result => {{
                if (result.error) {{
                    alert('Ошибка: ' + result.error.message);
                }} else {{
                    alert('Успешно!');
                    location.reload();
                }}
            }})
            .catch(error => {{
                alert('Ошибка сети: ' + error);
            }});
        }}
        
        function bookOffice(number) {{
            if (confirm(`Забронировать офис №${{number}}?`)) {{
                sendRPC('booking', {{ number: number }});
            }}
        }}
        
        function cancelOffice(number) {{
            if (confirm(`Отменить бронирование офиса №${{number}}?`)) {{
                sendRPC('cancellation', {{ number: number }});
            }}
        }}
        
        function loadOffices() {{
            const data = {{
                jsonrpc: "2.0",
                method: "info",
                params: {{}},
                id: Date.now()
            }};
            
            fetch('/lab6/api/', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(result => {{
                if (result.result) {{
                    updateOfficesGrid(result.result);
                }}
            }});
        }}
        
        function updateOfficesGrid(offices) {{
            const grid = document.getElementById('officesGrid');
            if (!grid) return;
            
            grid.innerHTML = '';
            offices.forEach(office => {{
                const isBooked = office.tenant && office.tenant.trim() !== '';
                const isMine = office.tenant === '{user}';
                
                let buttons = '';
                if (!isBooked) {{
                    buttons = `<button onclick="bookOffice(${{office.number}})" class="btn btn-success" style="width: 100%;">Забронировать</button>`;
                }} else if (isMine) {{
                    buttons = `<button onclick="cancelOffice(${{office.number}})" class="btn btn-danger" style="width: 100%;">Отменить</button>`;
                }}
                
                grid.innerHTML += `
                <div class="office-card ${{isBooked ? 'office-booked' : 'office-available'}}">
                    <div class="office-number">Офис №${{office.number}}</div>
                    <div class="office-price">${{office.price}} руб./мес.</div>
                    <div class="office-tenant">
                        ${{isBooked ? `Арендатор: ${{office.tenant}}` : 'Свободен'}}
                    </div>
                    <div class="controls">
                        ${{buttons}}
                    </div>
                </div>
                `;
            }});
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            loadOffices();
        }});
    </script>
</head>
<body>
    <div class="container">
        <h1>🏢 Лабораторная работа 6</h1>
        <p>Система бронирования офисов с JSON-RPC API</p>
        
        <div class="user-info">
            <h3>👤 Пользователь</h3>
            {'<p>Вы вошли как: <strong>' + user + '</strong></p>' if user else '<p>Вы не авторизованы</p>'}
            
            <div class="btn-group">
                {'<a href="/lab6/logout" class="btn btn-danger">🚪 Выйти</a>' if user else '<a href="/lab6/login" class="btn">🔐 Войти</a>'}
                <a href="/lab6/init-db" class="btn">🔄 Инициализировать БД</a>
                <a href="/" class="btn">🏠 На главную</a>
            </div>
        </div>
        
        <h2>📋 Доступные офисы</h2>
        <div id="officesGrid" class="offices-grid">
            <!-- Офисы загружаются через JavaScript -->
            <p>Загрузка офисов...</p>
        </div>
        
        <h2>📡 JSON-RPC API</h2>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3>Доступные методы:</h3>
            <ul>
                <li><strong>info</strong> - Получить список офисов (доступен всем)</li>
                <li><strong>booking</strong> - Забронировать офис (требует авторизации)</li>
                <li><strong>cancellation</strong> - Отменить бронирование (требует авторизации)</li>
            </ul>
            
            <h3>Пример запроса:</h3>
            <pre style="background: #333; color: #fff; padding: 10px; border-radius: 5px;">
{{
    "jsonrpc": "2.0",
    "method": "info",
    "params": {{}},
    "id": 1
}}</pre>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button onclick="loadOffices()" class="btn">🔄 Обновить список офисов</button>
        </div>
    </div>
</body>
</html>'''

@lab6.route('/login', methods=['GET', 'POST'])
def login():
    css_path = "/static/lab1/lab1.css"
    
    if request.method == 'POST':
        login_input = request.form.get('login', '').strip()
        if login_input:
            session['login'] = login_input
            return redirect('/lab6/')
    
    return f'''<!doctype html>
<html>
<head>
    <title>Вход</title>
    <link rel="stylesheet" href="{css_path}">
    <style>
        .container {{ max-width: 400px; margin: 50px auto; padding: 30px; }}
        .form-group {{ margin-bottom: 20px; }}
        input[type="text"] {{ width: 100%; padding: 10px; box-sizing: border-box; }}
        button {{ padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Вход в систему</h1>
        <p>Введите любой логин для демонстрации</p>
        
        <form method="POST" action="/lab6/login">
            <div class="form-group">
                <label for="login">Логин:</label>
                <input type="text" id="login" name="login" placeholder="Например: user123" required>
            </div>
            
            <div class="form-group">
                <button type="submit">🔓 Войти</button>
                <a href="/lab6/" style="margin-left: 10px;">← Назад</a>
            </div>
        </form>
        
        <div style="margin-top: 20px; font-size: 0.9em; color: #666;">
            <p>Для тестирования можно использовать:</p>
            <ul>
                <li>user1</li>
                <li>admin</li>
                <li>company</li>
                <li>Любое другое имя</li>
            </ul>
        </div>
    </div>
</body>
</html>'''

@lab6.route('/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab6/')

@lab6.route('/init-db')
def init_db():
    """Инициализация базы данных с офисами"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS offices')
    cursor.execute('''
        CREATE TABLE offices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER UNIQUE NOT NULL,
            tenant TEXT,
            price INTEGER NOT NULL
        )
    ''')
    
    for i in range(1, 11):
        cursor.execute(
            'INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)',
            (i, "", 900 + i * 100)
        )
    
    conn.commit()
    conn.close()
    
    return '''<!doctype html>
<html>
<head>
    <title>Инициализация БД</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container">
        <h1>✅ База данных инициализирована!</h1>
        <p>Создано 10 офисов с номерами от 1 до 10.</p>
        <div style="margin-top: 20px;">
            <a href="/lab6/" class="btn">🏢 Вернуться к офисам</a>
        </div>
    </div>
</body>
</html>'''

@lab6.route('/api/', methods=['POST'])
def api():
    data = request.get_json()
    
    if not data or 'jsonrpc' not in data or data['jsonrpc'] != '2.0':
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": None
        })
    
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')
    
    # Метод info доступен без авторизации
    if method == 'info':
        init_db_if_needed()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM offices ORDER BY number')
        offices = cursor.fetchall()
        conn.close()
        
        offices_list = []
        for office in offices:
            offices_list.append({
                'number': office['number'],
                'tenant': office['tenant'],
                'price': office['price']
            })
        return jsonify({
            'jsonrpc': '2.0',
            'result': offices_list,
            'id': request_id
        })
    
    # Для методов бронирования и отмены нужна авторизация
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': request_id
        })
    
    if method == 'booking':
        office_number = params.get('number')
        
        if not office_number:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params: number required'
                },
                'id': request_id
            })
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cursor.fetchone()
        
        if not office:
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': f'Office {office_number} not found'
                },
                'id': request_id
            })
        
        if office['tenant']:
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': f'Office {office_number} is already booked'
                },
                'id': request_id
            })
        
        cursor.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        conn.commit()
        conn.close()
        
        return jsonify({
            'jsonrpc': '2.0',
            'result': 'success',
            'id': request_id
        })
    
    elif method == 'cancellation':
        office_number = params.get('number')
        
        if not office_number:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params: number required'
                },
                'id': request_id
            })
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cursor.fetchone()
        
        if not office:
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': f'Office {office_number} not found'
                },
                'id': request_id
            })
        
        if not office['tenant']:
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': f'Office {office_number} is not booked'
                },
                'id': request_id
            })
        
        if office['tenant'] != login:
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'You can only cancel your own bookings'
                },
                'id': request_id
            })
        
        cursor.execute('UPDATE offices SET tenant = "" WHERE number = ?', (office_number,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'jsonrpc': '2.0',
            'result': 'success',
            'id': request_id
        })
    
    return jsonify({
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': request_id
    })