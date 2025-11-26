from flask import Flask, url_for, request, redirect, abort, render_template, current_app
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = 'sqlite' 

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

access_log = []
count = 0  

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1/lab1.css")
    image_path = url_for("static", filename="lab1/404_image.png")
    favicon_path = url_for("static", filename="lab1/favicon.ico")
    
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    log_entry = f"{access_time} — IP: {client_ip} — Запрошен несуществующий адрес: {request.path}"
    access_log.append(log_entry)
   
    if len(access_log) > 20:
        access_log.pop(0)

    log_entries_html = "<br>".join(access_log)
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="icon" type="image/x-icon" href="{favicon_path}"> 
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
    css_path = url_for("static", filename="lab1/lab1.css")
    favicon_path = url_for("static", filename="lab1/favicon.ico")
    lab1_url = url_for('lab1.lab11')
    lab2_url = url_for('lab2.lab22')
    lab3_url = url_for('lab3.lab')
    lab4_url = url_for('lab4.lab')
    lab5_url = url_for('lab5.main')

    return f'''
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <link rel="stylesheet" href="{css_path}">
            <link rel="icon" href="{favicon_path}">
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                </header>
                
                <main>
                    <div class="labs-list">
                        <h2>Список лабораторных работ:</h2>
                        <ul>
                            <li><a href="{lab1_url}">Лабораторная работа 1</a></li>
                            <li><a href="{lab2_url}">Лабораторная работа 2</a></li>
                            <li><a href="{lab3_url}">Лабораторная работа 3</a></li>
                            <li><a href="{lab4_url}">Лабораторная работа 4</a></li>
                            <li><a href="{lab5_url}">Лабораторная работа 5</a></li>  
                        </ul>
                    </div>
                </main>
                
                <footer>
                    <hr>
                    <p>Журавлева Виктория Александровна, ФБИ-34, 3 курс, 2025</p>
                </footer>
            </div>
        </body>
    </html>
    '''

@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1/lab1.css")
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