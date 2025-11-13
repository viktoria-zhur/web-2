from flask import Blueprint, render_template, request, redirect, session

tree_count = 0

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Введите корректные целые числа!')
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, operation='/')

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    try:
        x1 = float(x1) if x1 != '' else 0
        x2 = float(x2) if x2 != '' else 0
    except ValueError:
        return render_template('lab4/result.html', error='Введите корректные числа!', operation='+')
    
    result = x1 + x2
    return render_template('lab4/result.html', x1=x1, x2=x2, result=result, operation='+')

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    try:
        x1 = float(x1) if x1 != '' else 1
        x2 = float(x2) if x2 != '' else 1
    except ValueError:
        return render_template('lab4/result.html', error='Введите корректные числа!', operation='*')
    
    result = x1 * x2
    return render_template('lab4/result.html', x1=x1, x2=x2, result=result, operation='*')

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/result.html', error='Оба поля должны быть заполнены!', operation='-')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return render_template('lab4/result.html', error='Введите корректные числа!', operation='-')
    
    result = x1 - x2
    return render_template('lab4/result.html', x1=x1, x2=x2, result=result, operation='-')

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/result.html', error='Оба поля должны быть заполнены!', operation='**')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return render_template('lab4/result.html', error='Введите корректные числа!', operation='**')
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/result.html', error='Ноль в нулевой степени не определен!', operation='**')
    
    result = x1 ** x2
    return render_template('lab4/result.html', x1=x1, x2=x2, result=result, operation='**')

# Обработчик для страницы с деревьями
@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    # Обработка GET запроса - просто показываем страницу
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    # Обработка POST запроса - обрабатываем действие и делаем редирект
    operation = request.form.get('operation')
    
    if operation == 'plant':
        tree_count += 1
    elif operation == 'cut':
        if tree_count > 0:  # Проверяем, чтобы счетчик не ушел в минус
            tree_count -= 1
    
    # Редирект на эту же страницу методом GET
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт', 'gender': 'male'},
    {'login': 'vika', 'password': '458', 'name': 'Виктория', 'gender': 'female'},
    {'login': 'sergo', 'password': '153', 'name': 'Сергей', 'gender': 'male'},
    {'login': 'lis', 'password': '777', 'name': 'Лиса', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            # Находим имя пользователя для приветствия
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
        else:
            authorized = False
            login = ''
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)

    login_input = request.form.get('login', '')
    password = request.form.get('password', '')

    # Валидация пустых полей
    errors = []
    if not login_input:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')

    # Если есть ошибки валидации
    if errors:
        return render_template('lab4/login.html', errors=errors, login=login_input, authorized=False)

    # Проверка логина и пароля
    user_found = None
    for user in users:
        if login_input == user['login'] and password == user['password']:
            user_found = user
            break

    if user_found:
        session['login'] = user_found['login']
        return redirect('/lab4/login')
    else:
        errors = ['Неверные логин и/или пароль']
        return render_template('lab4/login.html', errors=errors, login=login_input, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = None
    message = None
    snowflakes = 0
    error = None
    
    if request.method == 'POST':
        temp_input = request.form.get('temperature', '').strip()
        
        # Проверка на пустое значение
        if not temp_input:
            error = "Ошибка: не задана температура"
        else:
            try:
                temperature = int(temp_input)
                
                # Проверка диапазонов температуры
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
    
    return render_template('lab4/fridge.html', 
                         temperature=temperature,
                         message=message,
                         snowflakes=snowflakes,
                         error=error)