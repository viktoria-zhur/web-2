from flask import Blueprint, redirect, url_for, render_template
lab1 = Blueprint('lab1', __name__)

@lab1.route('/lab1/error500')
def cause_error():
    my_list = [1, 2, 3]
    return my_list[10]


@lab1.route('/lab1/divide_zero')
def divide_zero():
    result = 10 / 0
    return f"Результат: {result}"


@lab1.route('/lab1/type_mismatch')
def type_mismatch():
    text = "Текст: "
    number = 42
    return text + number


@lab1.route("/lab1")
def lab11():
    css_path = url_for("static", filename="lab1.css")
    web_url = url_for('lab1.web')
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="corner-heart">💗</div>
            <div class="corner-heart">💖</div>
            <div class="corner-heart">💝</div>
            <div class="corner-heart">💞</div>
            <div class="container">
                <header>
                    <h1>Лабораторная работа 1</h1>
                </header>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые ба-
                    зовые возможности.
                </p>
                <h2>Список роутов</h2>
                <div class="info-box">
                    <h3>Основные роуты:</h3>
                    <ul>
                        <li><a href="/">Главная страница</a></li>
                        <li><a href="/index">Главная (альтернативная)</a></li>
                        <li><a href="/lab1">Лабораторная работа 1</a></li>
                        <li><a href="/lab1/web">WEB-сервер на Flask</a></li>
                        <li><a href="/lab1/author">Об авторе</a></li>
                        <li><a href="/lab1/image">Изображение</a></li>
                        <li><a href="/lab1/counter">Счётчик посещений</a></li>
                        <li><a href="/lab1/reset_counter">Сброс счётчика</a></li>
                        <li><a href="/lab1/info">Информация (редирект)</a></li>
                    </ul>
                    <h3>Тестирование ошибок:</h3>
                    <ul>
                        <li><a href="/lab1/error500">Ошибка 500 (IndexError)</a></li>
                        <li><a href="/lab1/divide_zero">Ошибка 500 (ZeroDivision)</a></li>
                        <li><a href="/lab1/type_mismatch">Ошибка 500 (TypeError)</a></li>
                        <li><a href="/400">Ошибка 400</a></li>
                        <li><a href="/401">Ошибка 401</a></li>
                        <li><a href="/402">Ошибка 402</a></li>
                        <li><a href="/403">Ошибка 403</a></li>
                        <li><a href="/405">Ошибка 405</a></li>
                        <li><a href="/418">Ошибка 418</a></li>
                    </ul>
                    <h3>Дополнительные роуты:</h3>
                    <ul>
                        <li><a href="/created">Создано (201)</a></li>
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


@lab1.route("/lab1/web")
def start():
    css_path = url_for("static", filename="lab1.css")
    return f"""<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>WEB-сервер на Flask</h1>
                    <div class="text-center">
                        <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
                    </div>
                </div>
            </body>
        </html>""", 200, {
        'X-Server': 'Flask-Sample',
        'Content-Type': 'text/html; charset=utf-8'
    }


@lab1.route("/lab1/author")
def author():
    css_path = url_for("static", filename="lab1.css")
    name = "Журавлева Виктория Александровна"
    group = "ФБИ-34"
    faculty = "ФБ"
    return f"""<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>💖 Об авторе 💖</h1>
                    <div class="info-box">
                        <p><strong>Студент:</strong> {name}</p>
                        <p><strong>Группа:</strong> {group}</p>
                        <p><strong>Факультет:</strong> {faculty}</p>
                    </div>
                    <div class="text-center">
                        <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
                    </div>
                </div>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    image_path = url_for("static", filename="a.png")
    css_path = url_for("static", filename="lab1.css")
    html_content = f'''
    <!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Самостоятельное задание💕</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="corner-heart">💗</div>
        <div class="corner-heart">💖</div>
        <div class="corner-heart">💝</div>
        <div class="corner-heart">💞</div>
        <div class="container">
            <h1>💖 Toyota Supra 💖</h1>
            <div class="image-wrlab1er">
                <img src="{image_path}"
                     alt="Toyota Supra JZA80"
                     class="styled-image">
                <div class="image-caption">✨ Toyota Supra JZA80 ✨</div>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
    </html>'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Developer': 'Zhuravleva-Victoria',
        'X-Student-Group': 'FBI-34',
        'X-Lab-Number': '1'
    }


@lab1.route('/lab1/counter')
def counter():
    css_path = url_for("static", filename="lab1.css")
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return f'''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <div class="container">
                    <h1>🔢 Счётчик посещений 🔢</h1>
                    <div class="info-box">
                        <p><strong>Сколько раз вы сюда заходили:</strong> {count}</p>
                        <p><strong>Дата и время:</strong> {time}</p>
                        <p><strong>Запрошенный адрес:</strong> {url}</p>
                        <p><strong>Ваш IP адрес:</strong> {client_ip}</p>
                    </div>
                    <div class="btn-group">
                        <a href="/lab1/reset_counter" class="btn btn-small">🗑️ Очистить счётчик</a>
                        <a href="/" class="btn btn-small btn-secondary">🏠 На главную</a>
                    </div>
                </div>
            </body>
        </html>
        '''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    css_path = url_for("static", filename="lab1.css")
    global count
    count = 0
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="container">
                <h2>✅ Счётчик очищен!</h2>
                <div class="info-box">
                    <p>Текущее значение счетчика: {count}</p>
                </div>
                <div class="btn-group">
                    <a href="/lab1/counter" class="btn btn-small">🔄 Вернуться к счётчику</a>
                    <a href="/" class="btn btn-small btn-secondary">🏠 На главную</a>
                </div>
            </div>
        </body>
    </html>
    '''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/created")
def created():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>🎉 Создано успешно</h1>
            <div class="info-box">
                <div><i>что-то создано...</i></div>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 201


@lab1.route('/400')
def bad_request():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>400 Bad Request</h1>
            <div class="info-box">
                <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 400


@lab1.route('/401')
def unauthorized():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>401 Unauthorized</h1>
            <div class="info-box">
                <p>Требуется аутентификация для доступа к ресурсу.</p>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 401


@lab1.route('/402')
def payment_required():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>402 Payment Required</h1>
            <div class="info-box">
                <p>Требуется оплата для доступа к ресурсу.</p>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 402


@lab1.route('/403')
def forbidden():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>403 Forbidden</h1>
            <div class="info-box">
                <p>Доступ к запрошенному ресурсу запрещен.</p>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 403


@lab1.route('/405')
def method_not_allowed():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>405 Method Not Allowed</h1>
            <div class="info-box">
                <p>Метод запроса не поддерживается для данного ресурса.</p>
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 405


@lab1.route('/418')
def teapot():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html><html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>418 I'm a teapot</h1>
            <div class="info-box">
                <p>Я - чайник. Не могу заварить кофе. ☕→❌</p>
                <p>Но могу предложить вам чай! :)→✅</p>
            </div>
            <div class="big-emoji">💖</div>
            <div class="text-center">
                <a href="/" class="btn btn-small">🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>''', 418