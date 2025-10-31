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