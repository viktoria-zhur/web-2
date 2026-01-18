from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# ТОЛЬКО ОДНА БАЗА ДАННЫХ для всего приложения
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

db = SQLAlchemy(app)

# Модель для офисов
class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    tenant = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)

# Модель для фильмов
class Movie(db.Model):
    __tablename__ = 'movies_final'
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

# ================= МОДЕЛИ ДЛЯ LAB8 =================
class User(db.Model):
    __tablename__ = 'lab8_users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    
    # Для Flask-Login
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
    __tablename__ = 'lab8_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('lab8_users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# ================= FLASK-LOGIN НАСТРОЙКА =================
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) if user_id else None

# ================= BLUEPRINTS =================
# Импортируем blueprint'ы других лабораторных
try:
    from lab1 import lab1
    app.register_blueprint(lab1, url_prefix='/lab1')
except:
    pass

try:
    from lab2 import lab2
    app.register_blueprint(lab2, url_prefix='/lab2')
except:
    pass

try:
    from lab3 import lab3
    app.register_blueprint(lab3, url_prefix='/lab3')
except:
    pass

try:
    from lab4 import lab4
    app.register_blueprint(lab4, url_prefix='/lab4')
except:
    pass

try:
    from lab5 import lab5
    app.register_blueprint(lab5, url_prefix='/lab5')
except:
    pass

try:
    from lab6 import lab6
    app.register_blueprint(lab6, url_prefix='/lab6')
except:
    pass

try:
    from lab7 import lab7
    app.register_blueprint(lab7, url_prefix='/lab7')
except:
    pass

try:
    from lab7_with_db import lab7_db
    app.register_blueprint(lab7_db, url_prefix='/lab7-db')
except:
    pass

# ================= СОЗДАНИЕ ТАБЛИЦ =================
with app.app_context():
    try:
        print("=" * 60)
        print("СОЗДАНИЕ ТАБЛИЦ БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        # Создаем все таблицы
        db.create_all()
        print("✓ Все таблицы созданы успешно")
        
        # Проверяем существующие таблицы
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Существующие таблицы: {tables}")
        
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        import traceback
        traceback.print_exc()

# ================= ГЛАВНАЯ СТРАНИЦА =================
@app.route('/')
@app.route('/index')
def index():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Главная - Лабораторные работы</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #333; 
                text-align: center;
                margin-bottom: 10px;
            }
            h2 {
                color: #666;
                text-align: center;
                margin-top: 0;
                margin-bottom: 30px;
            }
            .lab-list { 
                list-style: none; 
                padding: 0; 
            }
            .lab-list li { 
                margin: 15px 0; 
            }
            .lab-list a { 
                display: block; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px; 
                text-decoration: none; 
                color: white;
                transition: transform 0.3s, box-shadow 0.3s;
                font-size: 18px;
                font-weight: bold;
            }
            .lab-list a:hover { 
                transform: translateY(-5px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.6);
            }
            .lab-number {
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
            }
            .student-info {
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
            }
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
            </ul>
            
            <div class="student-info">
                <p><strong>Журавлева Виктория Александровна, ФБИ-34</strong></p>
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
    <head><title>Lab 7</title></head>
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
    <head><title>404</title></head>
    <body>
        <h1>404 - Страница не найдена</h1>
        <p>Запрошенная страница не существует.</p>
        <a href="/">На главную</a>
    </body>
    </html>
    ''', 404

# Импортируем lab8 в самом конце
try:
    from lab8 import lab8
    app.register_blueprint(lab8, url_prefix='/lab8')
    print("✓ Blueprint lab8 зарегистрирован")
except Exception as e:
    print(f"✗ Ошибка при регистрации lab8: {e}")

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("ЗАПУСК ПРИЛОЖЕНИЯ")
    print("=" * 60)
    print("Сервер запущен по адресу: http://127.0.0.1:5000")
    print("Страница lab8: http://127.0.0.1:5000/lab8/")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)