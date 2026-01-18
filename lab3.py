from flask import Blueprint, request, make_response, redirect
from datetime import datetime

lab3 = Blueprint('lab3', __name__)

# Список игрушек
toys = [
    {'id': 1, 'name': 'Конструктор LEGO City', 'brand': 'LEGO', 'price': 2990, 'category': 'Конструктор', 'age': '6+'},
    {'id': 2, 'name': 'Кукла Barbie', 'brand': 'Mattel', 'price': 1890, 'category': 'Кукла', 'age': '3+'},
    {'id': 3, 'name': 'Машинка Hot Wheels', 'brand': 'Mattel', 'price': 390, 'category': 'Машинка', 'age': '3+'},
    {'id': 4, 'name': 'Плюшевый мишка', 'brand': 'Aurora', 'price': 1290, 'category': 'Мягкая игрушка', 'age': '0+'},
    {'id': 5, 'name': 'Набор доктора', 'brand': 'PlayGo', 'price': 1590, 'category': 'Ролевые игры', 'age': '3+'},
    {'id': 6, 'name': 'Железная дорога', 'brand': 'Brio', 'price': 4590, 'category': 'Железная дорога', 'age': '3+'},
    {'id': 7, 'name': 'Пазл 1000 элементов', 'brand': 'Ravensburger', 'price': 890, 'category': 'Пазл', 'age': '8+'},
    {'id': 8, 'name': 'Набор для рисования', 'brand': 'Crayola', 'price': 1290, 'category': 'Творчество', 'age': '4+'},
    {'id': 9, 'name': 'Интерактивный робот', 'brand': 'WowWee', 'price': 7990, 'category': 'Электронная игрушка', 'age': '6+'},
    {'id': 10, 'name': 'Настольная игра "Монополия"', 'brand': 'Hasbro', 'price': 2490, 'category': 'Настольная игра', 'age': '8+'},
    {'id': 11, 'name': 'Кукольный домик', 'brand': 'Sylvanian Families', 'price': 5990, 'category': 'Кукольный домик', 'age': '4+'},
    {'id': 12, 'name': 'Воздушный змей', 'brand': 'Prism', 'price': 1490, 'category': 'Уличные игрушки', 'age': '5+'},
    {'id': 13, 'name': 'Набор "Юный химик"', 'brand': 'Bondibon', 'price': 1890, 'category': 'Обучающие', 'age': '8+'},
    {'id': 14, 'name': 'Радиоуправляемая машинка', 'brand': 'WLtoys', 'price': 3290, 'category': 'Радиоуправление', 'age': '6+'},
    {'id': 15, 'name': 'Музыкальный инструмент', 'brand': 'Melissa & Doug', 'price': 2190, 'category': 'Музыкальные', 'age': '3+'},
    {'id': 16, 'name': '3D-ручка', 'brand': 'MyRiwell', 'price': 2990, 'category': 'Творчество', 'age': '8+'},
    {'id': 17, 'name': 'Набор "Фокусы"', 'brand': 'Bondibon', 'price': 990, 'category': 'Обучающие', 'age': '6+'},
    {'id': 18, 'name': 'Спортивный набор', 'brand': 'Little Tikes', 'price': 3590, 'category': 'Спортивные', 'age': '3+'},
    {'id': 19, 'name': 'Интерактивный питомец', 'brand': 'FurReal', 'price': 4590, 'category': 'Электронная игрушка', 'age': '4+'},
    {'id': 20, 'name': 'Набор "Сделай слайм"', 'brand': 'Crayola', 'price': 790, 'category': 'Творчество', 'age': '6+'},
    {'id': 21, 'name': 'Детский планшет', 'brand': 'VTech', 'price': 3990, 'category': 'Электронная игрушка', 'age': '3+'},
    {'id': 22, 'name': 'Набор солдатиков', 'brand': 'Playmobil', 'price': 1590, 'category': 'Фигурки', 'age': '4+'},
    {'id': 23, 'name': 'Мягкий конструктор', 'brand': 'Battat', 'price': 1190, 'category': 'Конструктор', 'age': '1+'},
    {'id': 24, 'name': 'Набор для вышивания', 'brand': 'Rico', 'price': 690, 'category': 'Творчество', 'age': '7+'},
    {'id': 25, 'name': 'Детский микроскоп', 'brand': 'National Geographic', 'price': 2890, 'category': 'Обучающие', 'age': '6+'}
]


@lab3.route('/')
def index():
    css_path = "/static/lab1/lab1.css"
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Лабораторная 3</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="corner-heart">💗</div>
        <div class="corner-heart">💖</div>
        <div class="corner-heart">💝</div>
        <div class="corner-heart">💞</div>
        <div class="container">
            <header>
                <h1>Лабораторная работа 3</h1>
            </header>
            <p>
                Эта лабораторная работа посвящена работе с формами, обработке данных
                от пользователя, работе с cookies и сессиями в Flask.
            </p>
            <h2>Список роутов</h2>
            <div class="info-box">
                <h3>Работа с формами:</h3>
                <ul>
                    <li><a href="/lab3/form1?user=Пример&age=20&sex=мужской">Форма 1 (с параметрами)</a></li>
                    <li><a href="/lab3/form1">Форма 1 (пустая)</a></li>
                    <li><a href="/lab3/order">Заказ напитка</a></li>
                    <li><a href="/lab3/ticket">Билет на поезд</a></li>
                    <li><a href="/lab3/toys">Поиск игрушек</a></li>
                </ul>
                <h3>Работа с cookies:</h3>
                <ul>
                    <li><a href="/lab3/cookie">Просмотр cookies</a></li>
                    <li><a href="/lab3/set_cookie?name=Виктория&age=20">Установить cookie</a></li>
                    <li><a href="/lab3/delete_cookie">Удалить cookies</a></li>
                    <li><a href="/lab3/settings">Настройки стилей</a></li>
                    <li><a href="/lab3/delete_settings">Сбросить настройки</a></li>
                </ul>
                <h3>Результаты:</h3>
                <ul>
                    <li><a href="/lab3/success?drink=cofee&milk=on&sugar=on">Пример успешного заказа</a></li>
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


@lab3.route('/form1')
def form1():
    css_path = "/static/lab1/lab1.css"
    user = request.args.get('user', '')
    age = request.args.get('age', '')
    sex = request.args.get('sex', '')
    
    errors_html = ''
    if not user.strip() and user is not None:
        errors_html += '<li style="color: red;">Имя: Заполните поле!</li>'
    if not age.strip() and age is not None:
        errors_html += '<li style="color: red;">Возраст: Заполните поле!</li>'
    
    errors_list = f'<ul>{errors_html}</ul>' if errors_html else ''
    
    sex_checked_male = 'checked' if sex == 'мужской' else ''
    sex_checked_female = 'checked' if sex == 'женский' else ''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Форма 1</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input[type="text"], select {{ 
                width: 100%; 
                padding: 8px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                box-sizing: border-box;
            }}
            .radio-group {{ display: flex; gap: 20px; }}
            .radio-group label {{ display: flex; align-items: center; }}
            .radio-group input {{ margin-right: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Форма 1</h1>
            <p>Простая форма с валидацией данных</p>
            
            {errors_list}
            
            <form method="GET" action="/lab3/form1">
                <div class="form-group">
                    <label for="user">Имя:</label>
                    <input type="text" id="user" name="user" value="{user}" placeholder="Введите ваше имя">
                </div>
                
                <div class="form-group">
                    <label for="age">Возраст:</label>
                    <input type="text" id="age" name="age" value="{age}" placeholder="Введите ваш возраст">
                </div>
                
                <div class="form-group">
                    <label>Пол:</label>
                    <div class="radio-group">
                        <label>
                            <input type="radio" name="sex" value="мужской" {sex_checked_male}>
                            Мужской
                        </label>
                        <label>
                            <input type="radio" name="sex" value="женский" {sex_checked_female}>
                            Женский
                        </label>
                    </div>
                </div>
                
                <button type="submit" class="btn">Отправить</button>
                <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
            </form>
            
            <div style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px;">
                <h3>Переданные данные:</h3>
                <p><strong>Имя:</strong> {user if user else 'Не указано'}</p>
                <p><strong>Возраст:</strong> {age if age else 'Не указано'}</p>
                <p><strong>Пол:</strong> {sex if sex else 'Не указано'}</p>
            </div>
        </div>
    </body>
    </html>
    '''


@lab3.route('/order')
def order():
    css_path = "/static/lab1/lab1.css"
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Заказ напитка</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .checkbox-group {{ margin: 10px 0; }}
            .checkbox-group label {{ display: flex; align-items: center; }}
            .checkbox-group input {{ margin-right: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☕ Заказ напитка</h1>
            <p>Выберите напиток и дополнительные опции</p>
            
            <form method="GET" action="/lab3/success">
                <div class="form-group">
                    <label for="drink">Выберите напиток:</label>
                    <select id="drink" name="drink" required>
                        <option value="">-- Выберите напиток --</option>
                        <option value="cofee">Кофе - 120 руб.</option>
                        <option value="black-tea">Черный чай - 80 руб.</option>
                        <option value="green-tea">Зеленый чай - 70 руб.</option>
                    </select>
                </div>
                
                <div class="checkbox-group">
                    <label>
                        <input type="checkbox" name="milk">
                        Добавить молоко (+30 руб.)
                    </label>
                </div>
                
                <div class="checkbox-group">
                    <label>
                        <input type="checkbox" name="sugar">
                        Добавить сахар (+10 руб.)
                    </label>
                </div>
                
                <button type="submit" class="btn">Заказать</button>
                <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
            </form>
        </div>
    </body>
    </html>
    '''


@lab3.route('/success')
def success():
    css_path = "/static/lab1/lab1.css"
    drink = request.args.get('drink', '')
    milk = request.args.get('milk') == 'on'
    sugar = request.args.get('sugar') == 'on'
    
    # Расчет цены
    if drink == 'cofee':
        price = 120
        drink_name = 'Кофе'
    elif drink == 'black-tea':
        price = 80
        drink_name = 'Черный чай'
    elif drink == 'green-tea':
        price = 70
        drink_name = 'Зеленый чай'
    else:
        price = 0
        drink_name = 'Не выбран'
    
    extras = []
    if milk:
        price += 30
        extras.append('молоко')
    if sugar:
        price += 10
        extras.append('сахар')
    
    extras_text = ', '.join(extras) if extras else 'без добавок'
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Заказ успешен</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .success-box {{
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .price-box {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Заказ успешно оформлен!</h1>
            
            <div class="success-box">
                <h3>Детали заказа:</h3>
                <p><strong>Напиток:</strong> {drink_name}</p>
                <p><strong>Добавки:</strong> {extras_text}</p>
                <div class="price-box">
                    Итоговая стоимость: {price} руб.
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/lab3/order" class="btn">🔄 Сделать новый заказ</a>
                <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
            </div>
        </div>
    </body>
    </html>
    '''


@lab3.route('/cookie')
def cookie():
    css_path = "/static/lab1/lab1.css"
    name = request.cookies.get('name', 'Не установлено')
    age = request.cookies.get('age', 'Не установлено')
    name_color = request.cookies.get('name_color', 'black')
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Cookies</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .cookie-box {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .cookie-item {{
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍪 Cookies</h1>
            <p>Просмотр и управление cookies</p>
            
            <div class="cookie-box">
                <h3>Текущие cookies:</h3>
                <div class="cookie-item">
                    <strong>Имя:</strong> <span style="color: {name_color};">{name}</span>
                </div>
                <div class="cookie-item">
                    <strong>Возраст:</strong> {age}
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/lab3/set_cookie?name=Виктория&age=20" class="btn">➕ Установить cookie</a>
                <a href="/lab3/delete_cookie" class="btn btn-danger">🗑️ Удалить все cookies</a>
                <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
            </div>
        </div>
    </body>
    </html>
    '''


@lab3.route('/set_cookie')
def set_cookie():
    name = request.args.get('name', '')
    age = request.args.get('age', '')
    
    resp = make_response(redirect('/lab3/cookie'))
    if name:
        resp.set_cookie('name', name)
        resp.set_cookie('name_color', 'magenta')
    else:
        resp.set_cookie('name_color', '', expires=0)
    
    if age:
        resp.set_cookie('age', age)
    else:
        resp.set_cookie('age', '', expires=0)
    
    return resp


@lab3.route('/delete_cookie')
def delete_cookie():
    resp = make_response(redirect('/lab3/cookie'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('name_color', '', expires=0)
    return resp


@lab3.route('/settings')
def settings():
    css_path = "/static/lab1/lab1.css"
    
    # Получаем значения из формы
    color = request.args.get('color', '')
    bg_color = request.args.get('bg_color', '')
    font_size = request.args.get('font_size', '')
    font_family = request.args.get('font_family', '')
    
    # Если есть новые настройки - устанавливаем куки
    if any([color, bg_color, font_size, font_family]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp
    
    # Получаем значения из куки
    color = request.cookies.get('color', '#333333')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16px')
    font_family = request.cookies.get('font_family', 'Arial, sans-serif')
    
    # Применяем стили из cookies
    style = f"""
    body {{
        color: {color};
        background-color: {bg_color};
        font-size: {font_size};
        font-family: {font_family};
    }}
    """
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Настройки</title>
        <link rel="stylesheet" href="{css_path}">
        <style>{style}</style>
        <style>
            .preview-box {{
                padding: 20px;
                margin: 20px 0;
                border: 2px dashed #ccc;
                border-radius: 5px;
                background: rgba(255,255,255,0.9);
            }}
            .current-settings {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 Настройки стилей</h1>
            <p>Настройте внешний вид страницы. Настройки сохранятся в cookies.</p>
            
            <div class="current-settings">
                <h3>Текущие настройки:</h3>
                <p><strong>Цвет текста:</strong> {color}</p>
                <p><strong>Цвет фона:</strong> {bg_color}</p>
                <p><strong>Размер шрифта:</strong> {font_size}</p>
                <p><strong>Шрифт:</strong> {font_family}</p>
            </div>
            
            <div class="preview-box">
                <h3>Предпросмотр:</h3>
                <p>Это текст с текущими настройками стилей.</p>
                <p>Вы можете изменить эти настройки с помощью формы ниже.</p>
            </div>
            
            <form method="GET" action="/lab3/settings">
                <div class="form-group">
                    <label for="color">Цвет текста:</label>
                    <input type="color" id="color" name="color" value="{color}">
                </div>
                
                <div class="form-group">
                    <label for="bg_color">Цвет фона:</label>
                    <input type="color" id="bg_color" name="bg_color" value="{bg_color}">
                </div>
                
                <div class="form-group">
                    <label for="font_size">Размер шрифта:</label>
                    <select id="font_size" name="font_size">
                        <option value="12px" {'selected' if font_size == '12px' else ''}>12px</option>
                        <option value="14px" {'selected' if font_size == '14px' else ''}>14px</option>
                        <option value="16px" {'selected' if font_size == '16px' else ''}>16px</option>
                        <option value="18px" {'selected' if font_size == '18px' else ''}>18px</option>
                        <option value="20px" {'selected' if font_size == '20px' else ''}>20px</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="font_family">Шрифт:</label>
                    <select id="font_family" name="font_family">
                        <option value="Arial, sans-serif" {'selected' if font_family == 'Arial, sans-serif' else ''}>Arial</option>
                        <option value="Georgia, serif" {'selected' if font_family == 'Georgia, serif' else ''}>Georgia</option>
                        <option value="'Courier New', monospace" {'selected' if font_family == "'Courier New', monospace" else ''}>Courier New</option>
                        <option value="Verdana, sans-serif" {'selected' if font_family == 'Verdana, sans-serif' else ''}>Verdana</option>
                        <option value="'Times New Roman', serif" {'selected' if font_family == "'Times New Roman', serif" else ''}>Times New Roman</option>
                    </select>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn">💾 Сохранить настройки</button>
                    <a href="/lab3/delete_settings" class="btn btn-danger">🗑️ Сбросить настройки</a>
                    <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''


@lab3.route('/delete_settings')
def delete_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_family', '', expires=0)
    return resp


@lab3.route('/ticket', methods=['GET', 'POST'])
def ticket():
    css_path = "/static/lab1/lab1.css"
    
    if request.method == 'POST':
        # Получаем данные из формы
        fio = request.form.get('fio', '').strip()
        shelf = request.form.get('shelf', '')
        linen = request.form.get('linen', '')
        baggage = request.form.get('baggage', '')
        age = request.form.get('age', '').strip()
        departure = request.form.get('departure', '').strip()
        destination = request.form.get('destination', '').strip()
        date = request.form.get('date', '')
        insurance = request.form.get('insurance', '')
        
        # Проверка на пустые поля
        errors = []
        if not fio: errors.append("ФИО пассажира обязательно")
        if not shelf: errors.append("Выберите полку")
        if not linen: errors.append("Укажите наличие белья")
        if not baggage: errors.append("Укажите наличие багажа")
        if not age: errors.append("Возраст обязателен")
        if not departure: errors.append("Пункт выезда обязателен")
        if not destination: errors.append("Пункт назначения обязателен")
        if not date: errors.append("Дата поездки обязательна")
        if not insurance: errors.append("Укажите наличие страховки")
        
        # Проверка возраста
        age_int = 0
        if age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    errors.append("Возраст должен быть от 1 до 120 лет")
            except ValueError:
                errors.append("Возраст должен быть числом")
        
        if errors:
            errors_html = ''.join([f'<li style="color: red;">{error}</li>' for error in errors])
            return f'''
            <!doctype html>
            <html>
            <head>
                <title>Билет на поезд</title>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>🚂 Билет на поезд</h1>
                    <p>Ошибки в форме:</p>
                    <ul>{errors_html}</ul>
                    <a href="/lab3/ticket" class="btn">← Вернуться к форме</a>
                </div>
            </body>
            </html>
            '''
        
        # Расчет стоимости
        base_price = 700 if age_int < 18 else 1000
        total_price = base_price
        
        # Доплаты
        if shelf in ['нижняя', 'нижняя боковая']:
            total_price += 100
        if linen == 'да':
            total_price += 75
        if baggage == 'да':
            total_price += 250
        if insurance == 'да':
            total_price += 150
        
        # Формируем результат
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Билет оформлен</title>
            <link rel="stylesheet" href="{css_path}">
            <style>
                .ticket {{
                    border: 2px solid #333;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    position: relative;
                    overflow: hidden;
                }}
                .ticket:before {{
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path fill="rgba(255,255,255,0.1)" d="M0,0 L100,0 L100,100 Z"/></svg>');
                    background-size: cover;
                }}
                .ticket-content {{
                    position: relative;
                    z-index: 1;
                }}
                .ticket-header {{
                    text-align: center;
                    margin-bottom: 20px;
                    border-bottom: 1px dashed rgba(255,255,255,0.3);
                    padding-bottom: 10px;
                }}
                .ticket-info {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                .ticket-price {{
                    text-align: center;
                    font-size: 1.5em;
                    font-weight: bold;
                    background: rgba(255,255,255,0.2);
                    padding: 10px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ Билет успешно оформлен!</h1>
                
                <div class="ticket">
                    <div class="ticket-content">
                        <div class="ticket-header">
                            <h2>Железнодорожный билет</h2>
                            <p>Билет №{datetime.now().strftime("%Y%m%d%H%M%S")}</p>
                        </div>
                        
                        <div class="ticket-info">
                            <div>
                                <p><strong>ФИО:</strong> {fio}</p>
                                <p><strong>Возраст:</strong> {age_int} лет</p>
                                <p><strong>Полка:</strong> {shelf}</p>
                                <p><strong>Белье:</strong> {linen}</p>
                                <p><strong>Багаж:</strong> {baggage}</p>
                            </div>
                            <div>
                                <p><strong>Откуда:</strong> {departure}</p>
                                <p><strong>Куда:</strong> {destination}</p>
                                <p><strong>Дата:</strong> {date}</p>
                                <p><strong>Страховка:</strong> {insurance}</p>
                                <p><strong>Категория:</strong> {"Детский" if age_int < 18 else "Взрослый"}</p>
                            </div>
                        </div>
                        
                        <div class="ticket-price">
                            Итоговая стоимость: {total_price} руб.
                        </div>
                    </div>
                </div>
                
                <div class="btn-group">
                    <a href="/lab3/ticket" class="btn">🔄 Оформить еще один билет</a>
                    <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # GET запрос - показываем форму
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Билет на поезд</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .form-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            @media (max-width: 768px) {{
                .form-grid {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚂 Билет на поезд</h1>
            <p>Заполните форму для оформления железнодорожного билета</p>
            
            <form method="POST" action="/lab3/ticket">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="fio">ФИО пассажира:</label>
                        <input type="text" id="fio" name="fio" required placeholder="Иванов Иван Иванович">
                    </div>
                    
                    <div class="form-group">
                        <label for="age">Возраст:</label>
                        <input type="number" id="age" name="age" required min="1" max="120" placeholder="18">
                    </div>
                    
                    <div class="form-group">
                        <label for="departure">Пункт выезда:</label>
                        <input type="text" id="departure" name="departure" required placeholder="Москва">
                    </div>
                    
                    <div class="form-group">
                        <label for="destination">Пункт назначения:</label>
                        <input type="text" id="destination" name="destination" required placeholder="Санкт-Петербург">
                    </div>
                    
                    <div class="form-group">
                        <label for="date">Дата поездки:</label>
                        <input type="date" id="date" name="date" required value="{datetime.now().strftime('%Y-%m-%d')}">
                    </div>
                    
                    <div class="form-group">
                        <label for="shelf">Полка:</label>
                        <select id="shelf" name="shelf" required>
                            <option value="">-- Выберите полку --</option>
                            <option value="верхняя">Верхняя</option>
                            <option value="нижняя">Нижняя</option>
                            <option value="верхняя боковая">Верхняя боковая</option>
                            <option value="нижняя боковая">Нижняя боковая</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="linen">Комплект белья:</label>
                        <select id="linen" name="linen" required>
                            <option value="">-- Выберите опцию --</option>
                            <option value="да">Да (+75 руб.)</option>
                            <option value="нет">Нет</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="baggage">Багаж:</label>
                        <select id="baggage" name="baggage" required>
                            <option value="">-- Выберите опцию --</option>
                            <option value="да">Да (+250 руб.)</option>
                            <option value="нет">Нет</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="insurance">Страховка:</label>
                        <select id="insurance" name="insurance" required>
                            <option value="">-- Выберите опцию --</option>
                            <option value="да">Да (+150 руб.)</option>
                            <option value="нет">Нет</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group" style="margin-top: 20px;">
                    <button type="submit" class="btn">🎫 Оформить билет</button>
                    <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
                </div>
            </form>
            
            <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                <h3>Тарифы:</h3>
                <ul>
                    <li>Детский билет (до 18 лет): 700 руб.</li>
                    <li>Взрослый билет: 1000 руб.</li>
                    <li>Нижняя/нижняя боковая полка: +100 руб.</li>
                    <li>Комплект белья: +75 руб.</li>
                    <li>Багаж: +250 руб.</li>
                    <li>Страховка: +150 руб.</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''


@lab3.route('/toys')
def toys_search():
    css_path = "/static/lab1/lab1.css"
    
    # Получаем значения из куки
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    # Получаем значения из формы (если есть)
    min_price_form = request.args.get('min_price', '')
    max_price_form = request.args.get('max_price', '')
    
    # Определяем приоритет: форма > куки
    min_price = min_price_form if min_price_form != '' else min_price_cookie
    max_price = max_price_form if max_price_form != '' else max_price_cookie
    
    # Обработка сброса
    if request.args.get('reset'):
        min_price = ''
        max_price = ''
    
    # Фильтрация товаров
    filtered_toys = toys.copy()
    
    if min_price or max_price:
        try:
            min_val = float(min_price) if min_price else 0
            max_val = float(max_price) if max_price else float('inf')
            
            # Если пользователь перепутал min и max
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = str(min_val), str(max_val)
            
            filtered_toys = [toy for toy in toys if min_val <= toy['price'] <= max_val]
            
        except ValueError:
            # Если введены некорректные значения
            filtered_toys = toys
    
    # Рассчитываем мин и макс цены
    all_prices = [toy['price'] for toy in toys]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    # Генерируем HTML для игрушек
    toys_html = ''
    for toy in filtered_toys:
        toys_html += f'''
        <div class="toy-card">
            <div class="toy-header">
                <h3>{toy['name']}</h3>
                <span class="price">{toy['price']} руб.</span>
            </div>
            <div class="toy-details">
                <p><strong>Бренд:</strong> {toy['brand']}</p>
                <p><strong>Категория:</strong> {toy['category']}</p>
                <p><strong>Возраст:</strong> {toy['age']}</p>
            </div>
        </div>
        '''
    
    # Создаем ответ
    response = f'''
    <!doctype html>
    <html>
    <head>
        <title>Поиск игрушек</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .toys-container {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .toy-card {{
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                background: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }}
            .toy-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .toy-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }}
            .toy-header h3 {{
                margin: 0;
                font-size: 16px;
                color: #333;
            }}
            .price {{
                background: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-weight: bold;
            }}
            .toy-details p {{
                margin: 5px 0;
                color: #666;
                font-size: 14px;
            }}
            .search-stats {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧸 Поиск игрушек</h1>
            <p>Фильтруйте игрушки по цене. Настройки сохранятся в cookies.</p>
            
            <form method="GET" action="/lab3/toys">
                <div class="form-group" style="display: flex; gap: 10px; align-items: center;">
                    <div style="flex: 1;">
                        <label for="min_price">Минимальная цена:</label>
                        <input type="number" id="min_price" name="min_price" value="{min_price}" 
                               placeholder="{min_all_price}" min="0" step="10">
                    </div>
                    <div style="flex: 1;">
                        <label for="max_price">Максимальная цена:</label>
                        <input type="number" id="max_price" name="max_price" value="{max_price}" 
                               placeholder="{max_all_price}" min="0" step="10">
                    </div>
                    <div style="align-self: flex-end;">
                        <button type="submit" class="btn">🔍 Поиск</button>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button type="submit" name="reset" value="1" class="btn btn-danger">🗑️ Сбросить фильтры</button>
                    <a href="/lab3/" class="btn btn-small">← Назад к лабе 3</a>
                </div>
            </form>
            
            <div class="search-stats">
                <p>Найдено: <strong>{len(filtered_toys)}</strong> из {len(toys)} игрушек</p>
                <p>Диапазон цен: от {min_all_price} до {max_all_price} руб.</p>
                {f'<p>Текущий фильтр: от {min_price} до {max_price} руб.</p>' if min_price or max_price else ''}
            </div>
            
            <div class="toys-container">
                {toys_html if toys_html else '<p style="grid-column: 1/-1; text-align: center; color: #666;">Игрушки не найдены</p>'}
            </div>
        </div>
    </body>
    </html>
    '''
    
    # Создаем ответ с возможностью установки cookies
    resp = make_response(response)
    
    # Сохраняем в куки (если не сброс)
    if not request.args.get('reset'):
        if min_price:
            resp.set_cookie('min_price', min_price, max_age=30*24*60*60)
        if max_price:
            resp.set_cookie('max_price', max_price, max_age=30*24*60*60)
    else:
        # Очищаем куки при сбросе
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)
    
    return responce