from flask import Blueprint, request, session, redirect
import sqlite3
from os import path
import hashlib

lab5 = Blueprint('lab5', __name__)

# Путь к базе данных
DB_PATH = path.join(path.dirname(__file__), 'knowledge_base.db')

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            real_name TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_favorite BOOLEAN DEFAULT 0,
            is_public BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Инициализируем базу данных при импорте
init_db()

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """Получение подключения к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user():
    """Получение текущего пользователя из сессии"""
    username = session.get('username')
    if not username:
        return None
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE login = ?', (username,)).fetchone()
    conn.close()
    return user

@lab5.route('/')
def index():
    user = get_current_user()
    
    if user:
        user_info = f'<h2>👋 Добро пожаловать, {user["real_name"] or user["login"]}!</h2>'
        user_links = '''
        <div class="btn-group">
            <a href="/lab5/profile" class="btn">👤 Профиль</a>
            <a href="/lab5/list" class="btn">📝 Мои статьи</a>
            <a href="/lab5/create" class="btn">➕ Новая статья</a>
            <a href="/lab5/logout" class="btn btn-danger">🚪 Выйти</a>
        </div>
        '''
    else:
        user_info = '<h2>🔐 База знаний</h2>'
        user_links = '''
        <div class="auth-buttons">
            <a href="/lab5/login" class="btn">🔐 Войти</a>
            <a href="/lab5/register" class="btn">📝 Регистрация</a>
        </div>
        '''
    
    return f'''<!doctype html>
<html>
<head>
    <title>База знаний</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
    <style>
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .btn {{ display: inline-block; padding: 10px 20px; margin: 5px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
        .btn-danger {{ background: #e74c3c; }}
        .btn-small {{ padding: 5px 10px; font-size: 0.9em; }}
        .article-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; }}
        .form-group input, .form-group textarea, .form-group select {{ width: 100%; padding: 8px; box-sizing: border-box; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 База знаний</h1>
        {user_info}
        <p>Платформа для создания и обмена знаниями</p>
        
        {user_links}
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="/" class="btn btn-small">🏠 На главную</a>
        </div>
    </div>
</body>
</html>'''

@lab5.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''<!doctype html>
<html>
<head>
    <title>Вход</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
    <style>
        .container { max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input { width: 100%; padding: 8px; box-sizing: border-box; }
        .error { color: red; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Вход в систему</h1>
        <p>Введите ваши учетные данные</p>
        
        <form method="POST" action="/lab5/login">
            <div class="form-group">
                <label for="login">Логин:</label>
                <input type="text" id="login" name="login" required>
            </div>
            
            <div class="form-group">
                <label for="password">Пароль:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div>
                <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">🔓 Войти</button>
                <a href="/lab5/register" style="margin-left: 10px;">📝 Регистрация</a>
            </div>
        </form>
        
        <div style="margin-top: 20px;">
            <a href="/lab5/" class="btn-small">← Назад</a>
        </div>
    </div>
</body>
</html>'''
    
    login_input = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    
    if not login_input or not password:
        return '''<!doctype html>
<html>
<head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Заполните все поля</p><a href="/lab5/login">← Назад</a></div></body>
</html>'''
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE login = ?', (login_input,)).fetchone()
    conn.close()
    
    if not user or user['password'] != hash_password(password):
        return '''<!doctype html>
<html>
<head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Неверный логин или пароль</p><a href="/lab5/login">← Назад</a></div></body>
</html>'''
    
    session['username'] = login_input
    return redirect('/lab5')

@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''<!doctype html>
<html>
<head>
    <title>Регистрация</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container" style="max-width: 400px; margin: 50px auto;">
        <h1>📝 Регистрация</h1>
        <p>Создайте новый аккаунт</p>
        
        <form method="POST" action="/lab5/register">
            <div class="form-group">
                <label for="login">Логин:</label>
                <input type="text" id="login" name="login" required>
            </div>
            
            <div class="form-group">
                <label for="password">Пароль:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="real_name">Ваше имя:</label>
                <input type="text" id="real_name" name="real_name" required>
            </div>
            
            <div>
                <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">📝 Зарегистрироваться</button>
                <a href="/lab5/login" style="margin-left: 10px;">🔐 Уже есть аккаунт?</a>
            </div>
        </form>
        
        <div style="margin-top: 20px;">
            <a href="/lab5/" class="btn-small">← Назад</a>
        </div>
    </div>
</body>
</html>'''
    
    login_input = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    real_name = request.form.get('real_name', '').strip()
    
    if not login_input or not password or not real_name:
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Заполните все поля</p><a href="/lab5/register">← Назад</a></div></body>
</html>'''
    
    conn = get_db_connection()
    
    # Проверка существующего пользователя
    existing = conn.execute('SELECT id FROM users WHERE login = ?', (login_input,)).fetchone()
    if existing:
        conn.close()
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Логин уже занят</p><a href="/lab5/register">← Назад</a></div></body>
</html>'''
    
    # Создание нового пользователя
    password_hash = hash_password(password)
    conn.execute('INSERT INTO users (login, password, real_name) VALUES (?, ?, ?)',
                (login_input, password_hash, real_name))
    conn.commit()
    conn.close()
    
    session['username'] = login_input
    return redirect('/lab5')

@lab5.route('/list')
def list_articles():
    user = get_current_user()
    
    if not user:
        return redirect('/lab5/login')
    
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles WHERE user_id = ? ORDER BY created_at DESC', (user['id'],)).fetchall()
    conn.close()
    
    articles_html = ''
    for article in articles:
        articles_html += f'''
        <div class="article-card">
            <h3>{article["title"]}</h3>
            <p>{article["content"][:100]}...</p>
            <div>
                <small>{article["created_at"]}</small>
                {'⭐' if article['is_favorite'] else ''}
                {'🌐' if article['is_public'] else '🔒'}
                <a href="/lab5/edit/{article["id"]}">✏️</a>
                <a href="/lab5/delete/{article["id"]}" onclick="return confirm('Удалить?')">🗑️</a>
            </div>
        </div>
        '''
    
    if not articles_html:
        articles_html = '<p>У вас пока нет статей</p>'
    
    return f'''<!doctype html>
<html>
<head>
    <title>Мои статьи</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container">
        <h1>📚 Мои статьи</h1>
        <p><a href="/lab5/create">➕ Создать новую статью</a></p>
        {articles_html}
        <div style="margin-top: 20px;">
            <a href="/lab5/" class="btn-small">🏠 На главную</a>
        </div>
    </div>
</body>
</html>'''

@lab5.route('/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    
    if not user:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return '''<!doctype html>
<html>
<head>
    <title>Новая статья</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container" style="max-width: 600px;">
        <h1>✏️ Новая статья</h1>
        
        <form method="POST" action="/lab5/create">
            <div class="form-group">
                <label for="title">Заголовок:</label>
                <input type="text" id="title" name="title" required maxlength="100">
            </div>
            
            <div class="form-group">
                <label for="content">Текст статьи:</label>
                <textarea id="content" name="content" rows="10" required></textarea>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_favorite" value="1">
                    ⭐ Добавить в избранное
                </label>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_public" value="1">
                    🌐 Сделать публичной
                </label>
            </div>
            
            <div>
                <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">💾 Сохранить</button>
                <a href="/lab5/list" style="margin-left: 10px;">← Назад к статьям</a>
            </div>
        </form>
    </div>
</body>
</html>'''
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    is_favorite = 1 if request.form.get('is_favorite') else 0
    is_public = 1 if request.form.get('is_public') else 0
    
    if not title or not content:
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Заполните заголовок и текст</p><a href="/lab5/create">← Назад</a></div></body>
</html>'''
    
    conn = get_db_connection()
    conn.execute('INSERT INTO articles (user_id, title, content, is_favorite, is_public) VALUES (?, ?, ?, ?, ?)',
                (user['id'], title, content, is_favorite, is_public))
    conn.commit()
    conn.close()
    
    return redirect('/lab5/list')

@lab5.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    
    if not user:
        return redirect('/lab5/login')
    
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ? AND user_id = ?', 
                          (article_id, user['id'])).fetchone()
    
    if not article:
        conn.close()
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Статья не найдена</p><a href="/lab5/list">← Назад</a></div></body>
</html>'''
    
    if request.method == 'GET':
        checked_favorite = 'checked' if article['is_favorite'] else ''
        checked_public = 'checked' if article['is_public'] else ''
        
        html = f'''<!doctype html>
<html>
<head>
    <title>Редактирование</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container" style="max-width: 600px;">
        <h1>✏️ Редактирование статьи</h1>
        
        <form method="POST" action="/lab5/edit/{article_id}">
            <div class="form-group">
                <label for="title">Заголовок:</label>
                <input type="text" id="title" name="title" value="{article['title']}" required maxlength="100">
            </div>
            
            <div class="form-group">
                <label for="content">Текст статьи:</label>
                <textarea id="content" name="content" rows="10" required>{article['content']}</textarea>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_favorite" value="1" {checked_favorite}>
                    ⭐ Добавить в избранное
                </label>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_public" value="1" {checked_public}>
                    🌐 Сделать публичной
                </label>
            </div>
            
            <div>
                <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">💾 Сохранить</button>
                <a href="/lab5/list" style="margin-left: 10px;">← Назад к статьям</a>
            </div>
        </form>
    </div>
</body>
</html>'''
        conn.close()
        return html
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    is_favorite = 1 if request.form.get('is_favorite') else 0
    is_public = 1 if request.form.get('is_public') else 0
    
    if not title or not content:
        conn.close()
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Заполните заголовок и текст</p><a href="/lab5/edit/{article_id}">← Назад</a></div></body>
</html>'''
    
    conn.execute('UPDATE articles SET title = ?, content = ?, is_favorite = ?, is_public = ? WHERE id = ?',
                (title, content, is_favorite, is_public, article_id))
    conn.commit()
    conn.close()
    
    return redirect('/lab5/list')

@lab5.route('/delete/<int:article_id>')
def delete_article(article_id):
    user = get_current_user()
    
    if not user:
        return redirect('/lab5/login')
    
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ? AND user_id = ?', 
                          (article_id, user['id'])).fetchone()
    
    if not article:
        conn.close()
        return '''<!doctype html>
<html><head><title>Ошибка</title></head>
<body><div class="container"><h1>Ошибка</h1><p>Статья не найдена</p><a href="/lab5/list">← Назад</a></div></body>
</html>'''
    
    conn.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    
    return redirect('/lab5/list')

@lab5.route('/profile')
def profile():
    user = get_current_user()
    
    if not user:
        return redirect('/lab5/login')
    
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN is_favorite = 1 THEN 1 ELSE 0 END) as favorites,
            SUM(CASE WHEN is_public = 1 THEN 1 ELSE 0 END) as public
        FROM articles WHERE user_id = ?
    ''', (user['id'],)).fetchone()
    conn.close()
    
    return f'''<!doctype html>
<html>
<head>
    <title>Профиль</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container">
        <h1>👤 Профиль</h1>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <p><strong>Логин:</strong> {user['login']}</p>
            <p><strong>Имя:</strong> {user['real_name'] or 'Не указано'}</p>
        </div>
        
        <div style="display: flex; gap: 20px; margin: 20px 0;">
            <div style="text-align: center; padding: 15px; background: #667eea; color: white; border-radius: 10px; flex: 1;">
                <div style="font-size: 24px; font-weight: bold;">{stats['total'] or 0}</div>
                <div>Всего статей</div>
            </div>
            <div style="text-align: center; padding: 15px; background: #f39c12; color: white; border-radius: 10px; flex: 1;">
                <div style="font-size: 24px; font-weight: bold;">{stats['favorites'] or 0}</div>
                <div>Избранные</div>
            </div>
            <div style="text-align: center; padding: 15px; background: #2ecc71; color: white; border-radius: 10px; flex: 1;">
                <div style="font-size: 24px; font-weight: bold;">{stats['public'] or 0}</div>
                <div>Публичные</div>
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <a href="/lab5/list" class="btn">📝 Мои статьи</a>
            <a href="/lab5/" class="btn">🏠 На главную</a>
        </div>
    </div>
</body>
</html>'''

@lab5.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/lab5')