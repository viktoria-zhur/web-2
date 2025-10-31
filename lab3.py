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