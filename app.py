from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <body>
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
                <p>Журавлева Виктория Александровна, ФБИ-34, 3 курс, </p>
            </footer>
        </body>
    </html>
    '''

@app.route("/lab1")
def lab1():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
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
            
            <p><a href="/">Вернуться на главную</a></p>
            
            <footer>
                <hr>
                <p>Журавлева Виктория Александровна, ФБИ-34, 3 курс, </p>
            </footer>
        </body>
    </html>
    '''

@app.route("/lab1/web")
def start():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-cepsep на flask</h1>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Tipe': 'text/plain; charset-utf-8'
            }

@app.route("/lab1/author") 
def author():
    name = "Журавлева Виктория Александровна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    image_path = url_for("static", filename="a.png")
    css_path = url_for("static", filename="lab1.css")
    headers = {
        'Content-Language': 'ru',
        'X-Generator': 'Flask-lab1',
        'X-Custom-Header': 'This is a custom header value'
    }
    return '''
    <!doctype html>
   <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Самостоятельное задание💕</title>
    <!-- Подключение CSS через url_for() -->
    <link rel="stylesheet" href=" ''' + css_path + '''">
</head>
<body>
    <!-- Милые сердечки в углах -->
    <div class="corner-heart">💗</div>
    <div class="corner-heart">💖</div>
    <div class="corner-heart">💝</div>
    <div class="corner-heart">💞</div>
    
    <div class="container">
        <h1>💖</h1>
               
        <div class="image-wrapper">
            <img src=" ''' + image_path + '''" 
                 alt="Милое изображение" 
                 class="styled-image">
            <div class="image-caption">✨ Toyota Supra JZA80 ✨</div>
        </div>       
    </div>
</body>
</html>      
'''
count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
        <!doctype html>
        <html>
            <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                Дата и время: ''' + str(time) + '''<br>
                Запрошенный адрес: ''' + url + '''<br>
                Ваш IP адрес: ''' + client_ip + '''<br>
                <hr>
                <a href="/lab1/reset_counter">Очистить счётчик</a>
            </body>
        </html>
        '''
@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
    <!doctype html>
    <html>
        <body>
            <h2>Счётчик очищен!</h2>
            <p>Текущее значение счетчика: ''' + str(count) + '''</p>
            <a href="/lab1/counter">Вернуться к счётчику</a>
        </body>
    </html>
    '''

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201