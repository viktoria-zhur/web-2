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

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    grain_type = ''
    weight = ''
    total_price = 0
    discount = 0
    message = ''
    error = ''
    success = False
    
    # Цены на зерно
    prices = {
        'barley': 12000,   # ячмень
        'oats': 8500,      # овёс
        'wheat': 9000,     # пшеница
        'rye': 15000       # рожь
    }
    
    # Названия зерна для отображения
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if request.method == 'POST':
        grain_type = request.form.get('grain_type', '')
        weight_input = request.form.get('weight', '').strip()
        
        # Проверка на пустые значения
        if not grain_type:
            error = "Ошибка: выберите тип зерна"
        elif not weight_input:
            error = "Ошибка: не указан вес"
        else:
            try:
                weight = float(weight_input)
                
                # Проверка веса
                if weight <= 0:
                    error = "Ошибка: вес должен быть больше 0"
                elif weight > 100:
                    error = "Извините, такого объёма сейчас нет в наличии"
                else:
                    # Расчет стоимости
                    price_per_ton = prices[grain_type]
                    total_price = weight * price_per_ton
                    
                    # Применение скидки
                    if weight > 10:
                        discount = total_price * 0.10
                        total_price -= discount
                        message = f"Заказ успешно сформирован. Вы заказали {grain_names[grain_type]}. Вес: {weight} т. Сумма к оплате: {total_price:,.0f} руб. (применена скидка 10% за большой объём - {discount:,.0f} руб.)"
                    else:
                        message = f"Заказ успешно сформирован. Вы заказали {grain_names[grain_type]}. Вес: {weight} т. Сумма к оплате: {total_price:,.0f} руб."
                    
                    success = True
                    
            except ValueError:
                error = "Ошибка: введите корректное число для веса"
    
    return render_template('lab4/grain.html',
                         grain_type=grain_type,
                         weight=weight,
                         message=message,
                         error=error,
                         success=success,
                         prices=prices,
                         grain_names=grain_names)
@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    name = request.form.get('name', '').strip()
    
    errors = []
    
    # Валидация
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
    
    # Проверка уникальности логина
    for user in users:
        if user['login'] == login:
            errors.append('Логин уже занят')
            break
    
    if errors:
        return render_template('lab4/register.html', errors=errors, 
                             login=login, name=name)
    
    # Добавление нового пользователя
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': 'male'  # по умолчанию
    }
    users.append(new_user)
    
    # Автоматическая авторизация после регистрации
    session['login'] = login
    return redirect('/lab4/login') 

@lab4.route('/lab4/users')
def users_list():
    # Проверка авторизации
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    return render_template('lab4/users.html', 
                         users=users, 
                         current_user_login=current_user_login) 

@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    
    # Удаляем пользователя из списка
    global users
    users = [user for user in users if user['login'] != current_user_login]
    
    # Выход из системы
    session.pop('login', None)
    return redirect('/lab4/login')      

@lab4.route('/lab4/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    current_user = None
    
    # Находим текущего пользователя
    for user in users:
        if user['login'] == current_user_login:
            current_user = user
            break
    
    if request.method == 'GET':
        return render_template('lab4/edit_profile.html', 
                             user=current_user)
    
    # Обработка POST запроса
    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    errors = []
    
    # Валидация
    if not new_login:
        errors.append('Не введён логин')
    if not new_name:
        errors.append('Не введено имя')
    
    # Проверка уникальности логина (кроме текущего пользователя)
    for user in users:
        if user['login'] == new_login and user['login'] != current_user_login:
            errors.append('Логин уже занят')
            break
    
    if new_password and new_password != confirm_password:
        errors.append('Пароли не совпадают')
    
    if errors:
        return render_template('lab4/edit_profile.html', 
                             user=current_user, 
                             errors=errors)
    
    # Обновление данных пользователя
    current_user['login'] = new_login
    current_user['name'] = new_name
    
    # Обновление пароля только если введен новый
    if new_password:
        current_user['password'] = new_password
    
    # Обновление логина в сессии
    session['login'] = new_login
    
    return redirect('/lab4/users')