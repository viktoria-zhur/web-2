from flask import Blueprint, request, session, make_response, redirect
import random

lab4 = Blueprint('lab4', __name__)

tree_count = 0

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт', 'gender': 'male'},
    {'login': 'vika', 'password': '458', 'name': 'Виктория', 'gender': 'female'},
    {'login': 'sergo', 'password': '153', 'name': 'Сергей', 'gender': 'male'},
    {'login': 'lis', 'password': '777', 'name': 'Лиса', 'gender': 'female'}
]


@lab4.route('/')
def index():
    css_path = "/static/lab1/lab1.css"
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Лабораторная 4</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="corner-heart">💗</div>
        <div class="corner-heart">💖</div>
        <div class="corner-heart">💝</div>
        <div class="corner-heart">💞</div>
        <div class="container">
            <header>
                <h1>Лабораторная работа 4</h1>
            </header>
            <p>
                Эта лабораторная работа посвящена работе с формами, валидации данных,
                работе с сессиями и cookies, а также созданию интерактивных веб-приложений.
            </p>
            <h2>Список роутов</h2>
            <div class="info-box">
                <h3>Калькулятор:</h3>
                <ul>
                    <li><a href="/lab4/sum-form">Сложение</a></li>
                    <li><a href="/lab4/sub-form">Вычитание</a></li>
                    <li><a href="/lab4/mult-form">Умножение</a></li>
                    <li><a href="/lab4/div-form">Деление</a></li>
                    <li><a href="/lab4/pow-form">Возведение в степень</a></li>
                </ul>
                <h3>Игры и симуляторы:</h3>
                <ul>
                    <li><a href="/lab4/tree">Посадка деревьев</a></li>
                    <li><a href="/lab4/fridge">Холодильник</a></li>
                    <li><a href="/lab4/grain">Заказ зерна</a></li>
                </ul>
                <h3>Авторизация и пользователи:</h3>
                <ul>
                    <li><a href="/lab4/login">Вход</a></li>
                    <li><a href="/lab4/register">Регистрация</a></li>
                    <li><a href="/lab4/users">Список пользователей</a></li>
                    <li><a href="/lab4/edit_profile">Редактирование профиля</a></li>
                </ul>
            </div>
            <div class="text-center">
                <a href="/" class="btn">🏠 Вернуться на главную</a>
            </div>
            <footer>
                <hr>
                <p>Журавлева Виктория Александровна, ФБИ-34, 3 курс, 2024</p>
            </footer>
        </div>
    </body>
    </html>
    '''


# ================= КАЛЬКУЛЯТОР =================
def calculator_template(operation, x1='', x2='', result='', error=''):
    css_path = "/static/lab1/lab1.css"
    operations = {
        '+': ('Сложение', '/lab4/sum'),
        '-': ('Вычитание', '/lab4/sub'),
        '*': ('Умножение', '/lab4/mult'),
        '/': ('Деление', '/lab4/div'),
        '**': ('Возведение в степень', '/lab4/pow')
    }
    
    op_name, action = operations.get(operation, ('Операция', '#'))
    
    result_html = ''
    if result and not error:
        result_html = f'''
        <div class="success-box" style="margin: 20px 0; padding: 15px; background: #d4edda; border-radius: 5px;">
            <h3>Результат:</h3>
            <p style="font-size: 1.2em; font-weight: bold;">
                {x1} {operation} {x2} = {result}
            </p>
        </div>
        '''
    
    error_html = f'<p style="color: red;">{error}</p>' if error else ''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>{op_name}</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>🧮 {op_name}</h1>
            <p>Введите два числа для выполнения операции</p>
            
            {error_html}
            
            <form method="POST" action="{action}">
                <div class="form-group">
                    <label for="x1">Первое число:</label>
                    <input type="text" id="x1" name="x1" value="{x1 if x1 else ''}" required>
                </div>
                
                <div class="form-group">
                    <label for="x2">Второе число:</label>
                    <input type="text" id="x2" name="x2" value="{x2 if x2 else ''}" required>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn">➗ Вычислить</button>
                    <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                </div>
            </form>
            
            {result_html}
        </div>
    </body>
    </html>
    '''


@lab4.route('/div-form')
def div_form():
    return calculator_template('/')


@lab4.route('/div', methods=['POST'])
def div():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    
    if not x1 or not x2:
        return calculator_template('/', x1, x2, error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return calculator_template('/', x1, x2, error='Введите корректные числа!')
    
    if x2 == 0:
        return calculator_template('/', x1, x2, error='На ноль делить нельзя!')
    
    result = x1 / x2
    return calculator_template('/', x1, x2, result)


@lab4.route('/sum-form')
def sum_form():
    return calculator_template('+')


@lab4.route('/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    try:
        x1 = float(x1) if x1 != '' else 0
        x2 = float(x2) if x2 != '' else 0
    except ValueError:
        return calculator_template('+', x1, x2, error='Введите корректные числа!')
    
    result = x1 + x2
    return calculator_template('+', x1, x2, result)


@lab4.route('/mult-form')
def mult_form():
    return calculator_template('*')


@lab4.route('/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    try:
        x1 = float(x1) if x1 != '' else 1
        x2 = float(x2) if x2 != '' else 1
    except ValueError:
        return calculator_template('*', x1, x2, error='Введите корректные числа!')
    
    result = x1 * x2
    return calculator_template('*', x1, x2, result)


@lab4.route('/sub-form')
def sub_form():
    return calculator_template('-')


@lab4.route('/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    
    if not x1 or not x2:
        return calculator_template('-', x1, x2, error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return calculator_template('-', x1, x2, error='Введите корректные числа!')
    
    result = x1 - x2
    return calculator_template('-', x1, x2, result)


@lab4.route('/pow-form')
def pow_form():
    return calculator_template('**')


@lab4.route('/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    
    if not x1 or not x2:
        return calculator_template('**', x1, x2, error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return calculator_template('**', x1, x2, error='Введите корректные числа!')
    
    if x1 == 0 and x2 == 0:
        return calculator_template('**', x1, x2, error='Ноль в нулевой степени не определен!')
    
    result = x1 ** x2
    return calculator_template('**', x1, x2, result)


# ================= ДЕРЕВЬЯ =================
@lab4.route('/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    css_path = "/static/lab1/lab1.css"
    
    if request.method == 'POST':
        operation = request.form.get('operation')
        
        if operation == 'plant':
            tree_count += 1
        elif operation == 'cut':
            if tree_count > 0:
                tree_count -= 1
        
        return redirect('/lab4/tree')
    
    # Генерируем деревья
    trees_html = ''
    for i in range(tree_count):
        tree_color = random.choice(['#2ecc71', '#27ae60', '#229954'])
        tree_html = f'''
        <div class="tree" style="display: inline-block; margin: 10px; text-align: center;">
            <div style="color: {tree_color}; font-size: 40px;">🌲</div>
            <div style="background: #8B4513; width: 20px; height: 30px; margin: 0 auto;"></div>
        </div>
        '''
        trees_html += tree_html
    
    if tree_count == 0:
        trees_html = '''
        <div style="text-align: center; padding: 40px; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 60px;">🌵</div>
            <p style="color: #666;">Здесь пока нет деревьев</p>
        </div>
        '''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Посадка деревьев</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .tree-counter {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                font-size: 1.5em;
            }}
            .tree-controls {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }}
            .tree-controls button {{
                padding: 15px 30px;
                font-size: 18px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                transition: transform 0.3s;
            }}
            .tree-controls button:hover {{
                transform: translateY(-3px);
            }}
            .plant-btn {{
                background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
                color: white;
            }}
            .cut-btn {{
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌳 Посадка деревьев</h1>
            <p>Посадите или срубите дерево. Всего деревьев: {tree_count}</p>
            
            <div class="tree-counter">
                <h2>🌲 {tree_count} деревьев</h2>
            </div>
            
            <div class="tree-controls">
                <form method="POST" action="/lab4/tree" style="display: inline;">
                    <input type="hidden" name="operation" value="plant">
                    <button type="submit" class="plant-btn">🌱 Посадить дерево</button>
                </form>
                
                <form method="POST" action="/lab4/tree" style="display: inline;">
                    <input type="hidden" name="operation" value="cut">
                    <button type="submit" class="cut-btn" {'disabled' if tree_count == 0 else ''}>🪓 Срубить дерево</button>
                </form>
            </div>
            
            <div style="margin: 30px 0;">
                {trees_html}
            </div>
            
            <div class="text-center">
                <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
            </div>
        </div>
    </body>
    </html>
    '''


# ================= ХОЛОДИЛЬНИК =================
@lab4.route('/fridge', methods=['GET', 'POST'])
def fridge():
    css_path = "/static/lab1/lab1.css"
    
    temperature = None
    message = None
    snowflakes = 0
    error = None
    
    if request.method == 'POST':
        temp_input = request.form.get('temperature', '').strip()
        
        if not temp_input:
            error = "Ошибка: не задана температура"
        else:
            try:
                temperature = int(temp_input)
                
                if temperature < -12:
                    error = "Не удалось установить температуру — слишком низкое значение"
                elif temperature > -1:
                    error = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temperature <= -9:
                    message = f"Установлена температура: {temperature}°C"
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    message = f"Установлена температура: {temperature}°C"
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    message = f"Установлена температура: {temperature}°C"
                    snowflakes = 1
                    
            except ValueError:
                error = "Ошибка: введите целое число"
    
    # Генерируем снежинки
    snowflakes_html = '❄️' * snowflakes
    if snowflakes == 0:
        snowflakes_html = '🌡️'
    
    result_html = ''
    if message:
        result_html = f'''
        <div class="success-box" style="margin: 20px 0; padding: 20px; background: #d4edda; border-radius: 10px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">
                {snowflakes_html}
            </div>
            <h3>{message}</h3>
            <p>Количество снежинок: {snowflakes}</p>
        </div>
        '''
    
    error_html = f'''
    <div class="error-box" style="margin: 20px 0; padding: 15px; background: #f8d7da; color: #721c24; border-radius: 5px;">
        {error}
    </div>
    ''' if error else ''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Холодильник</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .fridge-display {{
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
            }}
            .temp-display {{
                font-size: 3em;
                font-weight: bold;
                margin: 10px 0;
            }}
            .range-info {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>❄️ Холодильник</h1>
            <p>Установите температуру холодильника (от -12°C до -1°C)</p>
            
            {error_html}
            
            <div class="range-info">
                <p><strong>Диапазон температур:</strong></p>
                <ul>
                    <li>от -12°C до -9°C: ❄️❄️❄️ (очень холодно)</li>
                    <li>от -8°C до -5°C: ❄️❄️ (холодно)</li>
                    <li>от -4°C до -1°C: ❄️ (прохладно)</li>
                </ul>
            </div>
            
            <form method="POST" action="/lab4/fridge">
                <div class="form-group">
                    <label for="temperature">Температура (°C):</label>
                    <input type="number" id="temperature" name="temperature" 
                           min="-12" max="-1" step="1" 
                           value="{temperature if temperature else ''}" 
                           placeholder="Введите температуру от -12 до -1" required>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn">🌡️ Установить температуру</button>
                    <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                </div>
            </form>
            
            {result_html}
        </div>
    </body>
    </html>
    '''


# ================= ЗЕРНО =================
@lab4.route('/grain', methods=['GET', 'POST'])
def grain():
    css_path = "/static/lab1/lab1.css"
    
    grain_type = ''
    weight = ''
    total_price = 0
    discount = 0
    message = ''
    error = ''
    success = False
    
    prices = {
        'barley': 12000,
        'oats': 8500,
        'wheat': 9000,
        'rye': 15000
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if request.method == 'POST':
        grain_type = request.form.get('grain_type', '')
        weight_input = request.form.get('weight', '').strip()
        
        if not grain_type:
            error = "Ошибка: выберите тип зерна"
        elif not weight_input:
            error = "Ошибка: не указан вес"
        else:
            try:
                weight = float(weight_input)
                
                if weight <= 0:
                    error = "Ошибка: вес должен быть больше 0"
                elif weight > 100:
                    error = "Извините, такого объёма сейчас нет в наличии"
                else:
                    price_per_ton = prices[grain_type]
                    total_price = weight * price_per_ton
                    
                    if weight > 10:
                        discount = total_price * 0.10
                        total_price -= discount
                        message = f"Заказ успешно сформирован. Вы заказали {grain_names[grain_type]}. Вес: {weight} т. Сумма к оплате: {total_price:,.0f} руб. (применена скидка 10% за большой объём - {discount:,.0f} руб.)"
                    else:
                        message = f"Заказ успешно сформирован. Вы заказали {grain_names[grain_type]}. Вес: {weight} т. Сумма к оплате: {total_price:,.0f} руб."
                    
                    success = True
                    
            except ValueError:
                error = "Ошибка: введите корректное число для веса"
    
    error_html = f'<div class="error-box">{error}</div>' if error else ''
    
    result_html = ''
    if success:
        result_html = f'''
        <div class="success-box" style="margin: 20px 0; padding: 20px; background: #d4edda; border-radius: 10px;">
            <h3>✅ Заказ оформлен!</h3>
            <p>{message}</p>
            <div style="background: #155724; color: white; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <strong>Итоговая сумма:</strong> {total_price:,.0f} руб.
            </div>
        </div>
        '''
    
    price_list = ''.join([f'<li>{name}: {price:,} руб./т</li>' for grain, price in prices.items() 
                         for name in [grain_names[grain]]])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Заказ зерна</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .price-table {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .discount-info {{
                background: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 4px solid #ffc107;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 Заказ зерна</h1>
            <p>Выберите тип зерна и укажите вес для расчета стоимости</p>
            
            {error_html}
            
            <div class="price-table">
                <h3>Цены на зерно:</h3>
                <ul>{price_list}</ul>
            </div>
            
            <div class="discount-info">
                <strong>🎁 Скидка 10%</strong> при заказе более 10 тонн!
            </div>
            
            <form method="POST" action="/lab4/grain">
                <div class="form-group">
                    <label for="grain_type">Тип зерна:</label>
                    <select id="grain_type" name="grain_type" required>
                        <option value="">-- Выберите зерно --</option>
                        <option value="barley" {'selected' if grain_type == 'barley' else ''}>Ячмень</option>
                        <option value="oats" {'selected' if grain_type == 'oats' else ''}>Овёс</option>
                        <option value="wheat" {'selected' if grain_type == 'wheat' else ''}>Пшеница</option>
                        <option value="rye" {'selected' if grain_type == 'rye' else ''}>Рожь</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="weight">Вес (тонны):</label>
                    <input type="number" id="weight" name="weight" 
                           min="0.1" max="100" step="0.1" 
                           value="{weight if weight else ''}" 
                           placeholder="Введите вес в тоннах" required>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn">💰 Рассчитать стоимость</button>
                    <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                </div>
            </form>
            
            {result_html}
        </div>
    </body>
    </html>
    '''


# ================= АВТОРИЗАЦИЯ =================
@lab4.route('/login', methods=['GET', 'POST'])
def login():
    css_path = "/static/lab1/lab1.css"
    
    if request.method == 'GET':
        authorized = 'login' in session
        login = session.get('login', '')
        user_name = ''
        
        if authorized:
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
        
        if authorized:
            return f'''
            <!doctype html>
            <html>
            <head>
                <title>Вход</title>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>👋 Добро пожаловать, {user_name}!</h1>
                    <p>Вы уже авторизованы как <strong>{login}</strong></p>
                    
                    <div class="btn-group">
                        <form method="POST" action="/lab4/logout" style="display: inline;">
                            <button type="submit" class="btn btn-danger">🚪 Выйти</button>
                        </form>
                        <a href="/lab4/users" class="btn">👥 Список пользователей</a>
                        <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                    </div>
                </div>
            </body>
            </html>
            '''
        else:
            return f'''
            <!doctype html>
            <html>
            <head>
                <title>Вход</title>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>🔐 Вход в систему</h1>
                    <p>Введите логин и пароль для входа</p>
                    
                    <form method="POST" action="/lab4/login">
                        <div class="form-group">
                            <label for="login">Логин:</label>
                            <input type="text" id="login" name="login" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="password">Пароль:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        
                        <div class="btn-group">
                            <button type="submit" class="btn">🔓 Войти</button>
                            <a href="/lab4/register" class="btn">📝 Регистрация</a>
                            <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                        </div>
                    </form>
                </div>
            </body>
            </html>
            '''
    
    # POST запрос
    login_input = request.form.get('login', '')
    password = request.form.get('password', '')
    
    errors = []
    if not login_input:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    
    if errors:
        errors_html = ''.join([f'<li style="color: red;">{error}</li>' for error in errors])
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Вход</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>🔐 Вход в систему</h1>
                <p>Ошибки:</p>
                <ul>{errors_html}</ul>
                <a href="/lab4/login" class="btn">← Попробовать снова</a>
            </div>
        </body>
        </html>
        '''
    
    user_found = None
    for user in users:
        if login_input == user['login'] and password == user['password']:
            user_found = user
            break
    
    if user_found:
        session['login'] = user_found['login']
        return redirect('/lab4/login')
    else:
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Вход</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>🔐 Вход в систему</h1>
                <p style="color: red;">Неверные логин и/или пароль</p>
                <a href="/lab4/login" class="btn">← Попробовать снова</a>
            </div>
        </body>
        </html>
        '''


@lab4.route('/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/register', methods=['GET', 'POST'])
def register():
    css_path = "/static/lab1/lab1.css"
    
    if request.method == 'GET':
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Регистрация</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>📝 Регистрация</h1>
                <p>Создайте новый аккаунт</p>
                
                <form method="POST" action="/lab4/register">
                    <div class="form-group">
                        <label for="login">Логин:</label>
                        <input type="text" id="login" name="login" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Пароль:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="confirm_password">Подтверждение пароля:</label>
                        <input type="password" id="confirm_password" name="confirm_password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="name">Имя:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="btn-group">
                        <button type="submit" class="btn">📝 Зарегистрироваться</button>
                        <a href="/lab4/login" class="btn">🔐 Уже есть аккаунт?</a>
                        <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        '''
    
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    name = request.form.get('name', '').strip()
    
    errors = []
    
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    if not confirm_password:
        errors.append('Не введено подтверждение пароля')
    if not name:
        errors.append('Не введено имя')
    
    if password != confirm_password:
        errors.append('Пароли не совпадают')
    
    for user in users:
        if user['login'] == login:
            errors.append('Логин уже занят')
            break
    
    if errors:
        errors_html = ''.join([f'<li style="color: red;">{error}</li>' for error in errors])
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Регистрация</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>📝 Регистрация</h1>
                <p>Ошибки:</p>
                <ul>{errors_html}</ul>
                <a href="/lab4/register" class="btn">← Попробовать снова</a>
            </div>
        </body>
        </html>
        '''
    
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': 'male'
    }
    users.append(new_user)
    
    session['login'] = login
    return redirect('/lab4/login')


@lab4.route('/users')
def users_list():
    css_path = "/static/lab1/lab1.css"
    
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    
    users_html = ''
    for user in users:
        user_html = f'''
        <div class="user-card" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background: {'#f0f8ff' if user['login'] == current_user_login else 'white'};">
            <h3 style="margin: 0;">{user['name']}</h3>
            <p><strong>Логин:</strong> {user['login']}</p>
            <p><strong>Пол:</strong> {user['gender']}</p>
            {f'<p style="color: #2ecc71;"><strong>👑 Это вы!</strong></p>' if user['login'] == current_user_login else ''}
        </div>
        '''
        users_html += user_html
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Пользователи</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>👥 Список пользователей</h1>
            <p>Всего пользователей: {len(users)}</p>
            
            {users_html}
            
            <div class="btn-group">
                <form method="POST" action="/lab4/delete_user" style="display: inline;">
                    <button type="submit" class="btn btn-danger">🗑️ Удалить мой аккаунт</button>
                </form>
                <a href="/lab4/edit_profile" class="btn">✏️ Редактировать профиль</a>
                <a href="/lab4/" class="btn btn-small">← Назад к лабе 4</a>
            </div>
        </div>
    </body>
    </html>
    '''


@lab4.route('/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    global users
    users = [user for user in users if user['login'] != current_user_login]
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    css_path = "/static/lab1/lab1.css"
    
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    current_user = None
    
    for user in users:
        if user['login'] == current_user_login:
            current_user = user
            break
    
    if request.method == 'GET':
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Редактирование профиля</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>✏️ Редактирование профиля</h1>
                <p>Измените данные вашего аккаунта</p>
                
                <form method="POST" action="/lab4/edit_profile">
                    <div class="form-group">
                        <label for="login">Логин:</label>
                        <input type="text" id="login" name="login" value="{current_user['login']}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="name">Имя:</label>
                        <input type="text" id="name" name="name" value="{current_user['name']}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Новый пароль (оставьте пустым, если не хотите менять):</label>
                        <input type="password" id="password" name="password">
                    </div>
                    
                    <div class="form-group">
                        <label for="confirm_password">Подтверждение нового пароля:</label>
                        <input type="password" id="confirm_password" name="confirm_password">
                    </div>
                    
                    <div class="btn-group">
                        <button type="submit" class="btn">💾 Сохранить изменения</button>
                        <a href="/lab4/users" class="btn btn-small">← Назад к пользователям</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        '''
    
    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    errors = []
    
    if not new_login:
        errors.append('Не введён логин')
    if not new_name:
        errors.append('Не введено имя')
    
    for user in users:
        if user['login'] == new_login and user['login'] != current_user_login:
            errors.append('Логин уже занят')
            break
    
    if new_password and new_password != confirm_password:
        errors.append('Пароли не совпадают')
    
    if errors:
        errors_html = ''.join([f'<li style="color: red;">{error}</li>' for error in errors])
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Редактирование профиля</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>✏️ Редактирование профиля</h1>
                <p>Ошибки:</p>
                <ul>{errors_html}</ul>
                <a href="/lab4/edit_profile" class="btn">← Попробовать снова</a>
            </div>
        </body>
        </html>
        '''
    
    current_user['login'] = new_login
    current_user['name'] = new_name
    
    if new_password:
        current_user['password'] = new_password
    
    session['login'] = new_login
    return redirect('/lab4/users')