from flask import Blueprint, redirect, url_for, render_template, request

lab2 = Blueprint('lab2', __name__)

# Списки данных
flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

flowers_with_prices = [
    {'id': 0, 'name': 'роза', 'price': 150},
    {'id': 1, 'name': 'тюльпан', 'price': 80},
    {'id': 2, 'name': 'незабудка', 'price': 50},
    {'id': 3, 'name': 'ромашка', 'price': 40}
]

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

legendary_cars = [
    {'name': 'Ford Mustang 1965', 'image': 'lab2/Ford Mustang 1965.png', 'description': 'Американский мускул-кар, икона 60-х годов'},
    {'name': 'Chevrolet Corvette Stingray', 'image': 'lab2/Chevrolet Corvette Stingray.jpg', 'description': 'Легендарный спорткар с уникальным дизайном'},
    {'name': 'Porsche 911', 'image': 'lab2/Porsche 911.jpg', 'description': 'Немецкий спорткар с заднемоторной компоновкой'},
    {'name': 'Ferrari F40', 'image': 'lab2/Ferrari F40.jpg', 'description': 'Последний Ferrari, одобренный Энцо Феррари'},
    {'name': 'Lamborghini Countach', 'image': 'lab2/Lamborghini Countach.png', 'description': 'Суперкар с клиновидным дизайном 70-х'},
    {'name': 'BMW M3 E30', 'image': 'lab2/BMW M3 E30.jpg', 'description': 'Первое поколение культового спортивного седана'},
    {'name': 'Mercedes-Benz 300SL', 'image': 'lab2/Mercedes-Benz 300SL.png', 'description': 'Знаменит дверями "крыло чайки"'},
    {'name': 'Audi Quattro', 'image': 'lab2/Audi Quattro.jpg', 'description': 'Пионер полного привода в ралли'},
    {'name': 'Toyota Supra MK4', 'image': 'lab2/Toyota Supra MK4.jpg', 'description': 'Японская легенда с двигателем 2JZ'},
    {'name': 'Nissan Skyline GT-R R34', 'image': 'lab2/Nissan Skyline GT-R R34.jpg', 'description': 'Легенда японского автопрома'},
    {'name': 'Mazda RX-7 FD', 'image': 'lab2/Mazda RX-7 FD.jpg', 'description': 'Спорткар с роторным двигателем'},
    {'name': 'Subaru Impreza WRX STI', 'image': 'lab2/Subaru Impreza WRX STI.jpg', 'description': 'Раллийная легенда с симметричным полным приводом'},
    {'name': 'Mitsubishi Lancer Evolution', 'image': 'lab2/Mitsubishi Lancer Evolution.jpg', 'description': 'Соперник Subaru в мировом ралли'},
    {'name': 'Volkswagen Golf GTI', 'image': 'lab2/Volkswagen Golf GTI.jpg', 'description': 'Родоначальник хот-хэтчей'},
    {'name': 'Ford GT40', 'image': 'lab2/Ford GT40.jpg', 'description': 'Победитель Ле-Мана, созданный чтобы победить Ferrari'},
    {'name': 'Jaguar E-Type', 'image': 'lab2/Jaguar E-Type.jpg', 'description': 'Был назван самой красивой машиной Энцо Феррари'},
    {'name': 'Aston Martin DB5', 'image': 'lab2/Aston Martin DB5.jpg', 'description': 'Автомобиль Джеймса Бонда'},
    {'name': 'DeLorean DMC-12', 'image': 'lab2/DeLorean DMC-12.jpg', 'description': 'Знаменит дверями-крыльями и появлением в "Назад в будущее"'},
    {'name': 'Dodge Charger', 'image': 'lab2/Dodge Charger.jpg', 'description': 'Американский мускул-кар из фильмов'},
    {'name': 'Shelby Cobra', 'image': 'lab2/Shelby Cobra.jpg', 'description': 'Американский V8 в британском кузове'},
    {'name': 'Bugatti Veyron', 'image': 'lab2/Bugatti Veyron.jpg', 'description': 'Первый суперкар мощностью 1000 л.с.'},
    {'name': 'McLaren F1', 'image': 'lab2/McLaren F1.jpg', 'description': 'Легендарный гиперкар с центральным расположением водителя'},
    {'name': 'Ferrari Testarossa', 'image': 'lab2/Ferrari Testarossa.png', 'description': 'Икона 80-х с характерными воздухозаборниками'}
]


@lab2.route('/')
def index():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Лабораторная 2</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="corner-heart">💗</div>
        <div class="corner-heart">💖</div>
        <div class="corner-heart">💝</div>
        <div class="corner-heart">💞</div>
        <div class="container">
            <header>
                <h1>Лабораторная работа 2</h1>
            </header>
            <p>
                Эта лабораторная работа посвящена работе с Jinja2, шаблонизатором Flask.
                Вы научитесь создавать динамические HTML-страницы, использовать переменные,
                циклы, условия и фильтры в шаблонах.
            </p>
            <h2>Список роутов</h2>
            <div class="info-box">
                <h3>Основные роуты:</h3>
                <ul>
                    <li><a href="/">Главная страница</a></li>
                    <li><a href="/lab2/">Лабораторная работа 2</a></li>
                    <li><a href="/lab2/example">Пример работы с Jinja2</a></li>
                    <li><a href="/lab2/filters">Фильтры Jinja2</a></li>
                    <li><a href="/lab2/calc/5/3">Калькулятор (5/3)</a></li>
                    <li><a href="/lab2/books">Книги</a></li>
                    <li><a href="/lab2/cars">Автомобили</a></li>
                </ul>
                <h3>Работа с цветами:</h3>
                <ul>
                    <li><a href="/lab2/flowers">Управление цветами</a></li>
                    <li><a href="/lab2/flowers_advanced">Цветы с ценами</a></li>
                    <li><a href="/lab2/add_flower/">Добавить цветок</a></li>
                </ul>
                <h3>Тестовые роуты:</h3>
                <ul>
                    <li><a href="/lab2/a/">Со слешем</a></li>
                    <li><a href="/lab2/b">Без слеша</a></li>
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


@lab2.route('/a/')
def a_with_slash():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''<!doctype html>
    <html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Со слешем</h1>
            <p>Этот путь заканчивается слешем: /lab2/a/</p>
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>'''


@lab2.route('/b')
def a_without_slash():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''<!doctype html>
    <html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Без слеша</h1>
            <p>Этот путь НЕ заканчивается слешем: /lab2/b</p>
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>'''


# Все остальные роуты возвращают простой HTML без шаблонов
@lab2.route('/example')
def example_lab2():
    css_path = url_for("static", filename="lab1/lab1.css")
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    
    fruits_html = ''.join([f'<li>{fruit["name"]} - {fruit["price"]} руб.</li>' for fruit in fruits])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Пример Jinja2</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Пример работы с Jinja2</h1>
            <p>Имя: Журавлева Виктория</p>
            <p>Лабораторная: 3</p>
            <p>Группа: ФБИ-34</p>
            <p>Курс: 3</p>
            
            <h2>Фрукты:</h2>
            <ul>{fruits_html}</ul>
            
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/filters')
def filters():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Фильтры Jinja2</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Фильтры Jinja2</h1>
            <p>Оригинальная фраза: 0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...</p>
            <p>Без safe: 0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...</p>
            <p>С safe: 0 сколько нам открытий чудных...</p>
            
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/calc/<int:a>/<int:b>')
def calc(a, b):
    css_path = url_for("static", filename="lab1/lab1.css")
    
    operations = [
        {'symbol': '+', 'result': a + b, 'name': 'Сумма'},
        {'symbol': '-', 'result': a - b, 'name': 'Разность'},
        {'symbol': '×', 'result': a * b, 'name': 'Произведение'},
        {'symbol': '/', 'result': a / b if b != 0 else 'Ошибка: деление на ноль', 'name': 'Частное'},
        {'symbol': '^', 'result': a ** b, 'name': 'Степень'}
    ]
    
    operations_html = ''.join([f'<li>{op["name"]}: {a} {op["symbol"]} {b} = {op["result"]}</li>' for op in operations])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Калькулятор</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Калькулятор</h1>
            <p>a = {a}, b = {b}</p>
            
            <h2>Операции:</h2>
            <ul>{operations_html}</ul>
            
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/books')
def show_books():
    css_path = url_for("static", filename="lab1/lab1.css")
    
    books_html = ''.join([f'<li><strong>{book["title"]}</strong> - {book["author"]} ({book["pages"]} стр.)</li>' for book in books])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Книги</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Книги</h1>
            <ul>{books_html}</ul>
            
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/cars')
def show_cars():
    css_path = url_for("static", filename="lab1/lab1.css")
    
    cars_html = ''.join([f'''
    <div class="car-item">
        <h3>{car['name']}</h3>
        <p>{car['description']}</p>
    </div>
    ''' for car in legendary_cars])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Автомобили</title>
        <link rel="stylesheet" href="{css_path}">
        <style>
            .car-item {{
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }}
            .car-item h3 {{
                margin-top: 0;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Легендарные автомобили</h1>
            {cars_html}
            
            <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/flowers')
def show_flowers():
    css_path = url_for("static", filename="lab1/lab1.css")
    
    flowers_html = ''.join([f'<li>{flower}</li>' for flower in flower_list])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Цветы</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Управление цветами</h1>
            <ul>{flowers_html}</ul>
            
            <div class="btn-group">
                <a href="/lab2/add_flower/" class="btn">Добавить цветок</a>
                <a href="/lab2/flowers/clear" class="btn btn-danger">Очистить список</a>
                <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
            </div>
        </div>
    </body>
    </html>
    '''


@lab2.route('/flowers/<int:flower_id>')
def show_flower(flower_id):
    css_path = url_for("static", filename="lab1/lab1.css")
    
    if flower_id < 0 or flower_id >= len(flower_list):
        return f'''
        <!doctype html>
        <html>
        <head>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h1>Ошибка 404</h1>
                <p>Цветок с ID {flower_id} не найден</p>
                <a href="/lab2/flowers" class="btn btn-small">← Вернуться к цветам</a>
            </div>
        </body>
        </html>
        ''', 404
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Цветок</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Цветок #{flower_id}</h1>
            <p>Название: <strong>{flower_list[flower_id]}</strong></p>
            <p>Всего цветов: {len(flower_list)}</p>
            
            <a href="/lab2/flowers" class="btn btn-small">← Вернуться к цветам</a>
        </div>
    </body>
    </html>
    '''


@lab2.route('/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')


@lab2.route('/add_flower/', methods=['GET', 'POST'])
def add_flower_form():
    css_path = url_for("static", filename="lab1/lab1.css")
    
    if request.method == 'POST':
        name = request.form.get('flower_name')
        if name:
            flower_list.append(name)
            return redirect('/lab2/flowers')
        else:
            return '''
            <!doctype html>
            <html>
            <head>
                <link rel="stylesheet" href="''' + css_path + '''">
            </head>
            <body>
                <div class="container">
                    <h1>Ошибка</h1>
                    <p>Вы не задали имя цветка</p>
                    <a href="/lab2/add_flower/" class="btn btn-small">← Попробовать снова</a>
                </div>
            </body>
            </html>
            ''', 400
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Добавить цветок</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Добавить новый цветок</h1>
            <form method="POST">
                <label for="flower_name">Название цветка:</label>
                <input type="text" id="flower_name" name="flower_name" required>
                <button type="submit" class="btn">Добавить</button>
            </form>
            <p><a href="/lab2/flowers" class="btn btn-small">← Вернуться к списку цветов</a></p>
        </div>
    </body>
    </html>
    '''


@lab2.route('/flowers_advanced')
def show_flowers_advanced():
    css_path = url_for("static", filename="lab1/lab1.css")
    
    total_price = sum(flower['price'] for flower in flowers_with_prices)
    flowers_html = ''.join([f'<li>{flower["name"]} - {flower["price"]} руб. <a href="/lab2/flowers_advanced/delete/{flower["id"]}">❌</a></li>' for flower in flowers_with_prices])
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Цветы с ценами</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Цветы с ценами</h1>
            <ul>{flowers_html}</ul>
            <p><strong>Общая стоимость:</strong> {total_price} руб.</p>
            
            <div class="btn-group">
                <form action="/lab2/flowers_advanced/add" method="POST" style="display: inline;">
                    <input type="text" name="name" placeholder="Название" required>
                    <input type="number" name="price" placeholder="Цена" required>
                    <button type="submit" class="btn">Добавить</button>
                </form>
                <a href="/lab2/flowers_advanced/clear" class="btn btn-danger">Очистить все</a>
                <a href="/lab2/" class="btn btn-small">← Назад к лабе 2</a>
            </div>
        </div>
    </body>
    </html>
    '''


@lab2.route('/flowers_advanced/add', methods=['POST'])
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
        return redirect('/lab2/flowers_advanced')
    
    return "Не указано имя или цена", 400


@lab2.route('/flowers_advanced/delete/<int:flower_id>')
def delete_flower_advanced(flower_id):
    global flowers_with_prices
    flowers_with_prices = [flower for flower in flowers_with_prices if flower['id'] != flower_id]
    return redirect('/lab2/flowers_advanced')


@lab2.route('/flowers_advanced/clear')
def clear_flowers_advanced():
    global flowers_with_prices
    flowers_with_prices.clear()
    return redirect('/lab2/flowers_advanced')


@lab2.route('/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')