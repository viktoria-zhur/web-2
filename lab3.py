from flask import Blueprint, render_template, request, make_response, redirect

# Сначала создаем Blueprint
lab3 = Blueprint('lab3', __name__)

# Затем определяем маршруты
@lab3.route('/lab3/')
def lab():
    return render_template('lab3/lab3.html')

@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    errors = {}
    
    if user is not None and not user.strip():
        errors['user'] = 'Заполните поле!'
    
    if age is not None and not age.strip():
        errors['age'] = 'Заполните поле!'
    
    return render_template('lab3/form1.html', 
                         user=user, 
                         age=age, 
                         sex=sex, 
                         errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/success')
def success():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/cookie')
def cookie():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/cookie.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/set_cookie')
def set_cookie():
    name = request.args.get('name')
    age = request.args.get('age')
    
    resp = make_response(redirect('/lab3/cookie'))
    if name:
        resp.set_cookie('name', name)
        # Автоматически устанавливаем розовый цвет для имени
        resp.set_cookie('name_color', 'magenta')
    else:
        # Если имя пустое, удаляем цвет
        resp.set_cookie('name_color', '', expires=0)
    
    if age:
        resp.set_cookie('age', age)
    else:
        resp.set_cookie('age', '', expires=0)
    
    return resp

@lab3.route('/lab3/delete_cookie')
def delete_cookie():
    resp = make_response(redirect('/lab3/cookie'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('name_color', '', expires=0)
    return resp

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    # Если есть новые настройки - устанавливаем куки и делаем редирект
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
    
    # Если новых настроек нет - показываем страницу с текущими настройками из куки
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    
    return render_template('lab3/settings.html', 
                         color=color, 
                         bg_color=bg_color, 
                         font_size=font_size, 
                         font_family=font_family)

@lab3.route('/lab3/delete_settings')
def delete_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_family', '', expires=0)
    return resp

@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        # Получаем данные из формы
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        linen = request.form.get('linen')
        baggage = request.form.get('baggage')
        age = request.form.get('age')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date = request.form.get('date')
        insurance = request.form.get('insurance')
        
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
        if age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    errors.append("Возраст должен быть от 1 до 120 лет")
            except ValueError:
                errors.append("Возраст должен быть числом")
        
        if errors:
            return render_template('lab2/ticket_form.html', errors=errors)
        
        # Расчет стоимости
        age_int = int(age)
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
        
        # Формируем данные билета
        ticket_data = {
            'fio': fio,
            'shelf': shelf,
            'linen': linen,
            'baggage': baggage,
            'age': age_int,
            'departure': departure,
            'destination': destination,
            'date': date,
            'insurance': insurance,
            'total_price': total_price,
            'is_child': age_int < 18
        }
        
        return render_template('lab3/ticket_result.html', **ticket_data)
    
    return render_template('lab3/ticket_form.html')

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

@lab3.route('/lab3/toys')
def toys_search():
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
    
    # Рассчитываем мин и макс цены для плейсхолдеров
    all_prices = [toy['price'] for toy in toys]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    response = make_response(render_template(
        'lab3/toys.html',
        toys=filtered_toys,
        min_price=min_price,
        max_price=max_price,
        min_all_price=min_all_price,
        max_all_price=max_all_price,
        found_count=len(filtered_toys),
        total_count=len(toys)
    ))
    
    # Сохраняем в куки (если не сброс)
    if not request.args.get('reset'):
        if min_price:
            response.set_cookie('min_price', min_price, max_age=30*24*60*60)
        if max_price:
            response.set_cookie('max_price', max_price, max_age=30*24*60*60)
    else:
        # Очищаем куки при сбросе
        response.set_cookie('min_price', '', expires=0)
        response.set_cookie('max_price', '', expires=0)
    
    return response