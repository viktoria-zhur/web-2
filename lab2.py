from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab2', __name__)

@app.route('/lab2/')
def lab2_index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Лабораторная работа 2</title>
    <link rel="stylesheet" href="/static/lab1.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Лабораторная работа 2</h1>
        </header>
        
        <nav>
            <ul>
                <li><a href="/">Главная</a></li>
                <li><a href="/lab1">Лабораторная работа 1</a></li>
            </ul>
        </nav>

        <main>
            <div class="routes-section">
                <h2>Список всех роутов лабораторной работы 2</h2>
                
                <div class="routes-category">
                    <h3>Основные роуты:</h3>
                    <ul>
                        <li><a href="/lab2/example">Пример страницы</a></li>
                        <li><a href="/lab2/filters">Фильтры Jinja2</a></li>
                        <li><a href="/lab2/calc/">Калькулятор</a></li>
                        <li><a href="/lab2/books">Библиотека книг</a></li>
                        <li><a href="/lab2/cars">Легендарные автомобили</a></li>
                        <li><a href="/lab2/flowers">Управление цветами</a></li>
                        <li><a href="/lab2/add_flower/">Добавить цветок</a></li>
                        <li><a href="/lab2/flowers_advanced">Расширенное управление цветами</a></li>
                    </ul>
                </div>

                <div class="routes-category">
                    <h3>Быстрый доступ:</h3>
                    <ul>
                        <li><a href="/lab2/calc/10/5">Калькулятор: 10 и 5</a></li>
                        <li><a href="/lab2/calc/25">Калькулятор: 25 и 1</a></li>
                        <li><a href="/lab2/flowers/clear">Очистить список цветов</a></li>
                        <li><a href="/lab2/flowers_advanced/clear">Очистить расширенный список</a></li>
                    </ul>
                </div>
            </div>
        </main>

        <footer>
            <hr>
            <p>© 2025 Журавлева Виктория Александровна, ФБИ-34, 3 курс</p>
        </footer>
    </div>
</body>
</html>
'''
@app.route('/lab2/a/')
def a_with_slash():
    return 'со слешем'

@app.route('/lab2/b')
def a_without_slash():
    return 'без слеша'

@app.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers_management.html', flower_list=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def show_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок с таким ID не найден", 404
    
    return render_template('flower_detail.html', 
                         flower=flower_list[flower_id], 
                         flower_id=flower_id,
                         total_count=len(flower_list))

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return render_template('flowers_management.html', flower_list=flower_list)

@app.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower_form():
    if request.method == 'POST':
        name = request.form.get('flower_name')
        if name:
            flower_list.append(name)
            return redirect('/lab2/flowers')
        else:
            return "вы не задали имя цветка", 400
    
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Добавить цветок</title>
            <link rel="stylesheet" href="/static/lab1.css">
        </head>
        <body>
            <h1>Добавить новый цветок</h1>
            <form method="POST">
                <label for="flower_name">Название цветка:</label>
                <input type="text" id="flower_name" name="flower_name" required>
                <button type="submit">Добавить</button>
            </form>
            <p><a href="/lab2/flowers">← Вернуться к списку цветов</a></p>
        </body>
    </html>
    '''

@app.route('/lab2/example')                    
def example_lab2():
    name, lab_num, group, course = 'Журавлева Виктория', 3, 'ФБИ-34', 3
    fruits = [
        {'name':'яблоки', 'price': 100},
        {'name':'груши', 'price': 120},
        {'name':'апельсины', 'price': 80},
        {'name':'мандарины', 'price': 95},
        {'name':'манго', 'price': 321}
    ]    
    return render_template('example.html',
                            name=name, lab_num=lab_num, group=group,
                            course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = [
        {'symbol': '+', 'result': a + b, 'name': 'Сумма'},
        {'symbol': '-', 'result': a - b, 'name': 'Разность'},
        {'symbol': '×', 'result': a * b, 'name': 'Произведение'},
        {'symbol': '/', 'result': a / b if b != 0 else 'Ошибка: деление на ноль', 'name': 'Частное'},
        {'symbol': '^', 'result': a ** b, 'name': 'Степень'}
    ]
    
    return render_template('calc.html', a=a, b=b, operations=operations)

# Пересылка с /lab2/calc/ на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

# Пересылка с /lab2/calc/<int:a> на /lab2/calc/<int:a>/1
@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1') 

# Список книг на стороне сервера
books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 320},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

# Список легендарных машин мира
legendary_cars = [
    {'name': 'Ford Mustang 1965', 'image': 'Ford Mustang 1965.png', 'description': 'Американский мускул-кар, икона 60-х годов'},
    {'name': 'Chevrolet Corvette Stingray', 'image': 'Chevrolet Corvette Stingray.jpg', 'description': 'Легендарный спорткар с уникальным дизайном'},
    {'name': 'Porsche 911', 'image': 'Porsche 911.jpg', 'description': 'Немецкий спорткар с заднемоторной компоновкой'},
    {'name': 'Ferrari F40', 'image': 'Ferrari F40.jpg', 'description': 'Последний Ferrari, одобренный Энцо Феррари'},
    {'name': 'Lamborghini Countach', 'image': 'Lamborghini Countach.png', 'description': 'Суперкар с клиновидным дизайном 70-х'},
    {'name': 'BMW M3 E30', 'image': 'BMW M3 E30.jpg', 'description': 'Первое поколение культового спортивного седана'},
    {'name': 'Mercedes-Benz 300SL', 'image': 'Mercedes-Benz 300SL.png', 'description': 'Знаменит дверями "крыло чайки"'},
    {'name': 'Audi Quattro', 'image': 'Audi Quattro.jpg', 'description': 'Пионер полного привода в ралли'},
    {'name': 'Toyota Supra MK4', 'image': 'Toyota Supra MK4.jpg', 'description': 'Японская легенда с двигателем 2JZ'},
    {'name': 'Nissan Skyline GT-R R34', 'image': 'Nissan Skyline GT-R R34.jpg', 'description': 'Легенда японского автопрома'},
    {'name': 'Mazda RX-7 FD', 'image': 'Mazda RX-7 FD.jpg', 'description': 'Спорткар с роторным двигателем'},
    {'name': 'Subaru Impreza WRX STI', 'image': 'Subaru Impreza WRX STI.jpg', 'description': 'Раллийная легенда с симметричным полным приводом'},
    {'name': 'Mitsubishi Lancer Evolution', 'image': 'Mitsubishi Lancer Evolution.jpg', 'description': 'Соперник Subaru в мировом ралли'},
    {'name': 'Volkswagen Golf GTI', 'image': 'Volkswagen Golf GTI.jpg', 'description': 'Родоначальник хот-хэтчей'},
    {'name': 'Ford GT40', 'image': 'Ford GT40.jpg', 'description': 'Победитель Ле-Мана, созданный чтобы победить Ferrari'},
    {'name': 'Jaguar E-Type', 'image': 'Jaguar E-Type.jpg', 'description': 'Был назван самой красивой машиной Энцо Феррари'},
    {'name': 'Aston Martin DB5', 'image': 'Aston Martin DB5.jpg', 'description': 'Автомобиль Джеймса Бонда'},
    {'name': 'DeLorean DMC-12', 'image': 'DeLorean DMC-12.jpg', 'description': 'Знаменит дверями-крыльями и появлением в "Назад в будущее"'},
    {'name': 'Dodge Charger', 'image': 'Dodge Charger.jpg', 'description': 'Американский мускул-кар из фильмов'},
    {'name': 'Shelby Cobra', 'image': 'Shelby Cobra.jpg', 'description': 'Американский V8 в британском кузове'},
    {'name': 'Bugatti Veyron', 'image': 'Bugatti Veyron.jpg', 'description': 'Первый суперкар мощностью 1000 л.с.'},
    {'name': 'McLaren F1', 'image': 'McLaren F1.jpg', 'description': 'Легендарный гиперкар с центральным расположением водителя'},
    {'name': 'Ferrari Testarossa', 'image': 'Ferrari Testarossa.png', 'description': 'Икона 80-х с характерными воздухозаборниками'}
]

@app.route('/lab2/cars')
def show_cars():
    return render_template('cars.html', cars=legendary_cars)
    
    # Новые улучшенные обработчики с ценами
flowers_with_prices = [
    {'id': 0, 'name': 'роза', 'price': 150},
    {'id': 1, 'name': 'тюльпан', 'price': 80},
    {'id': 2, 'name': 'незабудка', 'price': 50},
    {'id': 3, 'name': 'ромашка', 'price': 40}
]

# Главная страница цветов с ценами
@app.route('/lab2/flowers_advanced')
def show_flowers_advanced():
    total_price = sum(flower['price'] for flower in flowers_with_prices)
    return render_template('flowers_advanced.html', 
                         flowers=flowers_with_prices, 
                         total_price=total_price)

# Добавление цветка с ценой (POST форма)
@app.route('/lab2/flowers_advanced/add', methods=['POST'])
def add_flower_advanced():
    name = request.form.get('name')
    price = request.form.get('price')
    
    if name and price:
        new_id = max([flower['id'] for flower in flowers_with_prices], default=-1) + 1
        flowers_with_prices.append({
            'id': new_id,
            'name': name,
            'price': int(price)
        })
    
    return redirect(url_for('show_flowers_advanced'))

# Удаление цветка по ID
@app.route('/lab2/flowers_advanced/delete/<int:flower_id>')
def delete_flower_advanced(flower_id):
    global flowers_with_prices
    flower_to_delete = None
    
    for flower in flowers_with_prices:
        if flower['id'] == flower_id:
            flower_to_delete = flower
            break
    
    if flower_to_delete:
        flowers_with_prices = [flower for flower in flowers_with_prices if flower['id'] != flower_id]
        return redirect(url_for('show_flowers_advanced'))
    else:
        return "Цветок с таким ID не найден", 404

# Удаление всех цветов
@app.route('/lab2/flowers_advanced/clear')
def clear_flowers_advanced():
    global flowers_with_prices
    flowers_with_prices.clear()
    return redirect(url_for('show_flowers_advanced'))
