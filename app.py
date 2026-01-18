from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Простая конфигурация - используем одну базу данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "lab8.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret-key-lab8')

# Единый экземпляр SQLAlchemy
db = SQLAlchemy(app)

# ================= МОДЕЛИ =================
class User(db.Model):
    __tablename__ = 'users'
    
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
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# ================= FLASK-LOGIN =================
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= BLUEPRINTS =================
# Импортируем lab8 и регистрируем
from lab8 import lab8
app.register_blueprint(lab8, url_prefix='/lab8')

# Создаем таблицы при запуске
with app.app_context():
    db.create_all()

# ================= ГЛАВНАЯ СТРАНИЦА =================
@app.route('/')
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
    ]

    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Лабораторные работы</title>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #667eea; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; }}
            h1 {{ color: #333; text-align: center; }}
            .lab-list {{ list-style: none; padding: 0; }}
            .lab-list li {{ margin: 15px 0; }}
            .lab-list a {{ display: block; padding: 20px; background: #667eea; color: white; 
                          text-decoration: none; border-radius: 10px; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Лабораторные работы</h1>
            <ul class="lab-list">
                <li><a href="/lab8/">Лабораторная работа 8 - Flask и БД (ORM)</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)