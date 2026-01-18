from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(basedir, 'instance', 'offices.db')
)

app.config['SQLALCHEMY_BINDS'] = {
    'films': 'sqlite:///' + os.path.join(basedir, 'films_final.db'),
    'lab7': 'sqlite:///' + os.path.join(basedir, 'lab7.db')
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

db = SQLAlchemy(app)

class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    tenant = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies_final'
    __bind_key__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(200))
    russian_title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.original_title or self.russian_title,
            "title_ru": self.russian_title,
            "year": self.year,
            "description": self.description
        }

# ================= BLUEPRINTS =================
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab7_with_db import lab7_db  
from lab8 import lab8


app.register_blueprint(lab1, url_prefix='/lab1')
app.register_blueprint(lab2, url_prefix='/lab2')
app.register_blueprint(lab3, url_prefix='/lab3')
app.register_blueprint(lab4, url_prefix='/lab4')
app.register_blueprint(lab5, url_prefix='/lab5')
app.register_blueprint(lab6, url_prefix='/lab6')
app.register_blueprint(lab7, url_prefix='/lab7')
app.register_blueprint(lab7_db, url_prefix='/lab7-db')  
app.register_blueprint(lab8, url_prefix='/lab8')


# ================= СОЗДАНИЕ ТАБЛИЦ =================
with app.app_context():
    db.create_all()

# ================= ГЛАВНАЯ СТРАНИЦА =================
@app.route('/')
@app.route('/index')
def index():
    labs = [
        {'number': 1, 'title': 'Основы Flask', 'url': '/lab1/'},
        {'number': 2, 'title': 'Jinja2', 'url': '/lab2/'},
        {'number': 3, 'title': 'Формы и Cookies', 'url': '/lab3/'},
        {'number': 4, 'title': 'Валидация и Сессии', 'url': '/lab4/'},
        {'number': 5, 'title': 'Базы данных', 'url': '/lab5/'},
        {'number': 6, 'title': 'JSON-RPC API', 'url': '/lab6/'},
        {'number': 7, 'title': 'REST API', 'url': '/lab7/'},
    ]

    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Главная</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{ 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #764ba2;
                padding-bottom: 10px;
            }}
            .lab-list {{ 
                list-style: none; 
                padding: 0; 
            }}
            .lab-list li {{ 
                margin: 15px 0; 
            }}
            .lab-list a {{ 
                display: block; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px; 
                text-decoration: none; 
                color: white;
                transition: transform 0.3s, box-shadow 0.3s;
                font-size: 18px;
                font-weight: bold;
            }}
            .lab-list a:hover {{ 
                transform: translateY(-5px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.6);
            }}
            .lab-number {{
                display: inline-block;
                background: white;
                color: #764ba2;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                text-align: center;
                line-height: 30px;
                margin-right: 15px;
                font-weight: bold;
            }}
            .student-info {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
            }}
            .heart {{ 
                color: #e74c3c;
                font-size: 24px;
                animation: heartbeat 1.5s infinite;
            }}
            @keyframes heartbeat {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Лабораторные работы</h1>
            <h2>Web-программирование</h2>
            
            <ul class="lab-list">
                <li><a href="/lab1/"><span class="lab-number">1</span> Лабораторная работа 1 - Основы Flask</a></li>
                <li><a href="/lab2/"><span class="lab-number">2</span> Лабораторная работа 2 - Jinja2</a></li>
                <li><a href="/lab3/"><span class="lab-number">3</span> Лабораторная работа 3 - Формы и Cookies</a></li>
                <li><a href="/lab4/"><span class="lab-number">4</span> Лабораторная работа 4 - Валидация и Сессии</a></li>
                <li><a href="/lab5/"><span class="lab-number">5</span> Лабораторная работа 5 - Базы данных</a></li>
                <li><a href="/lab6/"><span class="lab-number">6</span> Лабораторная работа 6 - JSON-RPC API</a></li>
                <li><a href="/lab7/"><span class="lab-number">7</span> Лабораторная работа 7 - REST API</a></li>
                <li><a href="/lab8/"><span class="lab-number">7</span> Лабораторная работа 8 - REST API</a></li>
            </ul>
            
            <div class="student-info">
                <p><span class="heart">💖</span> Журавлева Виктория Александровна, ФБИ-34 <span class="heart">💖</span></p>
                <p>3 курс, 2025 год</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/lab7-final')
def lab7_final():
    count = Movie.query.count()
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Lab 7</title>
    </head>
    <body>
        <h1>Lab 7 Final</h1>
        <p>Фильмов в базе: {count}</p>
        <a href="/">← На главную</a>
    </body>
    </html>
    '''

@app.route('/api/films')
def films():
    return jsonify([m.to_dict() for m in Movie.query.all()])

@app.errorhandler(404)
def not_found(e):
    return '''
    <!doctype html>
    <html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .error-container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{ 
                color: #d00; 
                font-size: 72px;
                margin: 0;
            }}
            p {{
                color: #666;
                font-size: 18px;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: transform 0.3s;
            }}
            .btn:hover {{
                transform: translateY(-3px);
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404</h1>
            <p>Страница не найдена</p>
            <p>Запрошенная страница не существует.</p>
            <a href="/" class="btn">← Вернуться на главную</a>
        </div>
    </body>
    </html>
    ''', 404

@app.errorhandler(500)
def server_error(e):
    return '''
    <!doctype html>
    <html>
    <head>
        <title>500 - Ошибка сервера</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .error-container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{ 
                color: #d00; 
                font-size: 72px;
                margin: 0;
            }}
            p {{
                color: #666;
                font-size: 18px;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: transform 0.3s;
            }}
            .btn:hover {{
                transform: translateY(-3px);
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>500</h1>
            <p>Ошибка сервера</p>
            <p>Что-то пошло не так на сервере.</p>
            <a href="/" class="btn">← Вернуться на главную</a>
        </div>
    </body>
    </html>
    ''', 500

if __name__ == '__main__':
    app.run(debug=True)