from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="404_image.png") 
    
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Страница не найдена</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <!-- Милые сердечки в углах -->
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
                        <li>Проверьте правильность адреса</li>
                        <li>Вернитесь на главную страницу</li>
                        <li>Или просто полюбуйтесь нашими сердечками 💖</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                    color: white; text-decoration: none; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);">
                    🏠 Вернуться на главную</a>
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
            <!-- Милые сердечки в углах -->
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
                        <li><a href="/lab1/error500">Тест ошибки 500</a></li>
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
# Обработчик ошибки 500
@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Ошибка сервера</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <!-- Милые сердечки в углах -->
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            <div class="corner-heart">💔</div>
            
            <div class="container">
                <h1>💥 Ой! Что-то пошло не так 💥</h1>
                
                <div class="image-wrapper">
                    <div style="font-size: 80px; margin: 20px 0;">😵</div>
                    <div class="image-caption">500 - Внутренняя ошибка сервера</div>
                </div>
                
                <div class="info-box">
                    <h2>Что случилось?</h2>
                    <p>На сервере произошла непредвиденная ошибка. Не волнуйтесь, наши инженеры уже работают над решением проблемы!</p>
                    <ul>
                        <li>Попробуйте обновить страницу позже</li>
                        <li>Вернитесь на главную страницу</li>
                        <li>Если проблема повторяется, сообщите администратору</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                    color: white; text-decoration: none; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);">
                    🏠 Вернуться на главную</a>
                </div>
            </div>
        </body>
    </html>
    ''', 500

# Страница, вызывающая ошибку 500
@app.route('/lab1/error500')
def cause_error():
    my_list = [1, 2, 3]
    return my_list[10] 
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
            <!-- Милые сердечки в углах -->
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
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="/" style="display: inline-block; padding: 10px 25px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                    color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                    🏠 Вернуться на главную</a>
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
                    <h1>web-cepsep на flask</h1>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                        color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                        🏠 Вернуться на главную</a>
                    </div>
                </div>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Tipe': 'text/plain; charset-utf-8'
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
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                        color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                        🏠 Вернуться на главную</a>
                    </div>
                </div>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    image_path = url_for("static", filename="a.png")
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Самостоятельное задание💕</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <!-- Милые сердечки в углах -->
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
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
    </html>      
    '''

count = 0

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
                    <div style="text-align: center;">
                        <a href="/lab1/reset_counter" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                        color: white; text-decoration: none; border-radius: 20px; font-weight: bold; margin-right: 10px;">
                        🗑️ Очистить счётчик</a>
                        <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #a0d8ff, #4a90e2); 
                        color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                        🏠 На главную</a>
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
                <div style="text-align: center;">
                    <a href="/lab1/counter" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                    color: white; text-decoration: none; border-radius: 20px; font-weight: bold; margin-right: 10px;">
                    🔄 Вернуться к счётчику</a>
                    <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #a0d8ff, #4a90e2); 
                    color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                    🏠 На главную</a>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/created")
def created():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>🎉 Создано успешно</h1>
            <div class="info-box">
                <div><i>что-то создано...</i></div>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 201

# Страницы с кодами ответов HTTP
@app.route('/400')
def bad_request():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>400 Bad Request</h1>
            <div class="info-box">
                <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 400

@app.route('/401')
def unauthorized():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>401 Unauthorized</h1>
            <div class="info-box">
                <p>Требуется аутентификация для доступа к ресурсу.</p>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 401

@app.route('/402')
def payment_required():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>402 Payment Required</h1>
            <div class="info-box">
                <p>Требуется оплата для доступа к ресурсу.</p>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 402

@app.route('/403')
def forbidden():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>403 Forbidden</h1>
            <div class="info-box">
                <p>Доступ к запрошенному ресурсу запрещен.</p>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 403

@app.route('/405')
def method_not_allowed():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>405 Method Not Allowed</h1>
            <div class="info-box">
                <p>Метод запроса не поддерживается для данного ресурса.</p>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 405

@app.route('/418')
def teapot():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
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
            <div style="text-align: center; font-size: 60px; margin: 20px 0;">💖 </div>
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ffb6c1, #ff69b4); 
                color: white; text-decoration: none; border-radius: 20px; font-weight: bold;">
                🏠 Вернуться на главную</a>
            </div>
        </div>
    </body>
</html>
''', 418