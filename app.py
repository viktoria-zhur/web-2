from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

# Глобальный список для хранения лога посещений
access_log = []
count = 0  # Инициализация счётчика

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="404_image.png")
    # Получаем IP-адрес пользователя и текущую дату/время
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Добавляем запись в лог
    log_entry = f"{access_time} — IP: {client_ip} — Запрошен несуществующий адрес: {request.path}"
    access_log.append(log_entry)
    # Ограничиваем количество записей в логе, чтобы не перегружать страницу
    if len(access_log) > 20:
        access_log.pop(0)
    # Формируем HTML-список записей лога
    log_entries_html = "<br>".join(access_log)
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Страница не найдена</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            <div class="container">
                <h1>💔 Ой-ой! Страница потерялась 💔</h1>
                <div class="image-wrapper">
                    <img src="{image_path}"
                         alt="Страница не найдена"
                         class="styled-image">
                    <div class="image-caption">404 - Страница не найдена</div>
                </div>
                <div class="info-box">
                    <h2>Что случилось?</h2>
                    <p>Похоже, эта страница отправилась в путешествие и не может найти дорогу домой!</p>
                    <ul>
                        <li>Ваш IP-адрес: {client_ip}</li>
                        <li>Дата доступа: {access_time}</li>
                        <li>Проверьте правильность адреса</li>
                        <li>Вернитесь на <a href="/">главную страницу</a></li>
                        <li>Или просто полюбуйтесь нашими сердечками 💖</li>
                    </ul>
                </div>
                <div class="text-center">
                    <a href="/" class="btn">🏠 Вернуться на главную</a>
                </div>
                <div class="log-box">
                    <h2>📜 Журнал посещений:</h2>
                    <div class="log-entries">
                        {log_entries_html}
                    </div>
                </div>
            </div>
        </body>
    </html>
    ''', 404

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="corner-heart">💗</div>
            <div class="corner-heart">💖</div>
            <div class="corner-heart">💝</div>
            <div class="corner-heart">💞</div>
            <div class="container">
                <header>
                    <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                </header>
                <nav>
                    <ul>
                        <li><a href="/lab1">Первая лабораторная</a></li>
                    </ul>
                </nav>
                <footer>
                    <hr>
                    <p>Журавлева Виктория Александровна, ФБИ-34, 3 курс, 2024</p>
                </footer>
            </div>
        </body>
    </html>
    '''

@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Внутренняя ошибка сервера</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <div class="corner-heart">💥</div>
            <div class="corner-heart">🔥</div>
            <div class="corner-heart">💥</div>
            <div class="corner-heart">🔥</div>
            <div class="container">
                <h1>🚨 Внутренняя ошибка сервера 🚨</h1>
                <div class="image-wrapper">
                    <div class="big-emoji">😵‍💫</div>
                    <div class="image-caption">500 - Сервер столкнулся с непредвиденной ошибкой</div>
                </div>
                <div class="info-box error-details">
                    <h2>Что произошло?</h2>
                    <p>На сервере произошла внутренняя ошибка. Наша команда уже уведомлена и работает над решением проблемы.</p>
                    <div class="error-actions">
                        <h3>Что можно сделать:</h3>
                        <ul>
                            <li>🔄 <strong>Обновите страницу</strong> - возможно, это временная проблема</li>
                            <li>⏰ <strong>Попробуйте позже</strong> - мы уже исправляем ошибку</li>
                            <li>📧 <strong>Сообщите администратору</strong> - если проблема повторяется</li>
                            <li>🏠 <strong>Вернитесь на главную</strong> - и продолжите работу с другими разделами</li>
                        </ul>
                    </div>
                    <div class="technical-info">
                        <details>
                            <summary>Техническая информация (для администратора)</summary>
                            <p><strong>Время ошибки:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                            <p><strong>Код ошибки:</strong> 500 Internal Server Error</p>
                        </details>
                    </div>
                </div>
                <div class="text-center">
                    <a href="/" class="btn btn-primary">🏠 Вернуться на главную</a>
                    <a href="/lab1" class="btn btn-secondary">📚 К лабораторным работам</a>
                </div>
                <footer class="error-footer">
                    <hr>
                    <p>Если ошибка повторяется, свяжитесь с технической поддержкой</p>
                </footer>
            </div>
        </body>
    </html>
    ''', 500

@app.route('/lab1/error500')
def cause_error():
    my_list = [1, 2, 3]
    return my_list[10]

@app.route('/lab1/divide_zero')
def divide_zero():
    result = 10 / 0
    return f"Результат: {result}"

@app.route('/lab1/type_mismatch')
def type_mismatch():
    text = "Текст: "
    number = 42
    return text + number

@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="lab1.css")
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/image')
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
            <div class="image-wrapper">
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

@app.route('/lab1/counter')
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

@app.route('/lab1/reset_counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/created")
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

@app.route('/400')
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

@app.route('/401')
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

@app.route('/402')
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

@app.route('/403')
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

@app.route('/405')
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

@app.route('/418')
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

@app.route('/lab2/a/')
def a_with_slash():
    return 'со слешем'

@app.route('/lab2/b')
def a_without_slash():
    return 'без слеша'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
        <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

 

if __name__ == '__main__':
    app.run(debug=True)