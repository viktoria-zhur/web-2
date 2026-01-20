from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

# Сначала создаем экземпляры расширений
db = SQLAlchemy()
login_manager = LoginManager()

# Потом создаем приложение
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# Одна база данных для всего
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "lab8.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key-for-lab8'

# Инициализируем расширения с приложением
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'lab8.login'

# Модели должны быть определены ПОСЛЕ инициализации db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # Flask-Login
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    is_favorite = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Загрузчик пользователя
@login_manager.user_loader
def load_user(user_id):
    # Используем контекст приложения
    with app.app_context():
        return db.session.get(User, int(user_id)) if user_id else None

# Главная страница
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
        {'number': 8, 'title': 'Flask и БД (ORM)', 'url': '/lab8/'},
        {'number': 9, 'title': 'Поздравление с Новым Годом', 'url': '/lab9/'},
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
                <li><a href="/lab8/"><span class="lab-number">8</span> Лабораторная работа 8 - Flask и БД (ORM)</a></li>
                <li><a href="/lab9/"><span class="lab-number">9</span> Лабораторная работа 9 - Поздравление с Новым Годом (ORM)</a></li>
            </ul>
            
            <div class="student-info">
                <p><span class="heart">💖</span> Журавлева Виктория Александровна, ФБИ-34 <span class="heart">💖</span></p>
                <p>3 курс, 2025 год</p>
            </div>
        </div>
    </body>
    </html>
    '''

# Обработчики ошибок
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

# Импортируем и регистрируем blueprints ПОСЛЕ определения всех моделей
# Калькулятор
@app.route('/calc')
def calc_page():
    return '''
    <html>
    <body>
        <h1>Калькулятор (серверный)</h1>
        <form method="POST" action="/calculate">
            <input name="num1" placeholder="Первое число">
            <select name="operation">
                <option>+</option>
                <option>-</option>
                <option>*</option>
                <option>/</option>
            </select>
            <input name="num2" placeholder="Второе число">
            <button type="submit">=</button>
        </form>
    </body>
    </html>
    '''

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operation = request.form.get('operation')
    
    if not num1 or not num2:
        return "Ошибка: заполните все поля"
    
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        return "Ошибка: введите числа"

    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 == 0:
            return "Ошибка: деление на ноль"
        result = num1 / num2
    else:
        return "Ошибка: неизвестная операция"
    
    return f'''
    <html>
    <body>
        <h1>Результат: {result}</h1>
        <a href="/calc">Новый расчет</a>
    </body>
    </html>
    '''
with app.app_context():
    # Создаем таблицы
    db.create_all()
    print("=" * 60)
    print("БАЗА ДАННЫХ СОЗДАНА")
    print("=" * 60)
    
    # Теперь импортируем blueprints
    try:
        from lab9 import lab9
        app.register_blueprint(lab9, url_prefix='/lab9')
        print("lab9 blueprint зарегистрирован")
    except ImportError as e:
        print(f"lab9.py не найден: {e}")
    
    try:
        from lab8 import lab8
        app.register_blueprint(lab8, url_prefix='/lab8')
        print("lab8 blueprint зарегистрирован")
    except ImportError as e:
        print(f"lab8.py не найден: {e}")
    
    # Простые заглушки для других лабораторных
    try:
        from lab1 import lab1
        app.register_blueprint(lab1, url_prefix='/lab1')
    except ImportError:
        pass
    
    try:
        from lab2 import lab2
        app.register_blueprint(lab2, url_prefix='/lab2')
    except ImportError:
        pass
    
    try:
        from lab3 import lab3
        app.register_blueprint(lab3, url_prefix='/lab3')
    except ImportError:
        pass
    
    try:
        from lab4 import lab4
        app.register_blueprint(lab4, url_prefix='/lab4')
    except ImportError:
        pass
    
    try:
        from lab5 import lab5
        app.register_blueprint(lab5, url_prefix='/lab5')
    except ImportError:
        pass
    
    try:
        from lab6 import lab6
        app.register_blueprint(lab6, url_prefix='/lab6')
    except ImportError:
        pass
    
    try:
        from lab7 import lab7
        app.register_blueprint(lab7, url_prefix='/lab7')
    except ImportError:
        pass
    
    try:
        from lab7_with_db import lab7_db
        app.register_blueprint(lab7_db, url_prefix='/lab7-db')
    except ImportError:
        pass

if __name__ == '__main__':
    print("=" * 60)
    print("ЗАПУСК СЕРВЕРА")
    print("=" * 60)
    print("Откройте браузер и перейдите по адресу:")
    print("http://127.0.0.1:5000/")
    print("Для lab8 перейдите по адресу:")
    print("http://127.0.0.1:5000/lab8/")
    print("Для lab9 перейдите по адресу:")
    print("http://127.0.0.1:5000/lab9/")
    print("=" * 60)
    app.run(debug=True)