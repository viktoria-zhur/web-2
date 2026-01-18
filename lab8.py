from flask import Blueprint, render_template_string, request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

lab8 = Blueprint('lab8', __name__)

# Получаем db из текущего приложения
def get_db():
    from app import db
    return db

def get_models():
    from app import User, Article
    return User, Article

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =================
def format_text(text, max_length=200):
    """Обрезает текст если слишком длинный"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

# ================= ОСНОВНЫЕ МАРШРУТЫ =================

# Главная страница lab8
@lab8.route('/')
def index():
    user_info = ''
    menu = ''
    
    if current_user.is_authenticated:
        user_info = f'Вы вошли как: <strong>{current_user.login}</strong>'
        menu = '''
            <a href="/lab8/articles/" class="btn">📝 Мои статьи</a>
            <a href="/lab8/create/" class="btn" style="background:#28a745;">➕ Создать статью</a>
            <a href="/lab8/public/" class="btn">🌐 Публичные статьи</a>
            <a href="/lab8/logout/" class="btn" style="background:#dc3545;">🚪 Выход</a>
        '''
    else:
        user_info = 'Вы не авторизованы'
        menu = '''
            <a href="/lab8/login/" class="btn">🔑 Вход</a>
            <a href="/lab8/register/" class="btn" style="background:#28a745;">📝 Регистрация</a>
            <a href="/lab8/public/" class="btn">🌐 Публичные статьи</a>
        '''
    
    # Проверяем есть ли сообщения в URL
    message_html = ''
    if request.args.get('message'):
        message = request.args.get('message')
        message_type = request.args.get('type', 'success')
        message_html = f'''
        <div class="alert alert-{message_type}" style="padding:15px; border-radius:5px; margin-bottom:20px; 
                background:{"#d4edda" if message_type=="success" else "#f8d7da"}; 
                color:{"#155724" if message_type=="success" else "#721c24"};
                border:1px solid {"#c3e6cb" if message_type=="success" else "#f5c6cb"};">
            {message}
        </div>
        '''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Lab 8 - База знаний</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }}
            .user-info {{
                text-align: center;
                padding: 15px;
                background: #e9ecef;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .menu {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 30px 0;
                justify-content: center;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
                border: none;
                font-size: 16px;
                cursor: pointer;
            }}
            .btn:hover {{
                background: #5a67d8;
                text-decoration: none;
                color: white;
            }}
            .test-actions {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
                text-align: center;
            }}
            .article-card {{
                border: 1px solid #ddd;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                background: #f8f9fa;
            }}
            .article-actions {{
                margin-top: 15px;
                display: flex;
                gap: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>База знаний</h1>
            <div class="subtitle">Лабораторная работа 8 - Flask и БД (ORM)</div>
            
            {message_html}
            
            <div class="user-info">
                {user_info}
            </div>
            
            <div class="menu">
                {menu}
            </div>
            
            <div class="test-actions">
                <h3>Быстрые действия:</h3>
                <p>Для тестирования создайте таблицы и тестового пользователя:</p>
                <div style="margin: 15px 0;">
                    <a href="/lab8/create-tables/" class="btn" style="background:#17a2b8;">🗃️ Создать таблицы</a>
                    <a href="/lab8/test-data/" class="btn" style="background:#17a2b8;">🧪 Тестовые данные</a>
                </div>
                <p><small>Логин: <code>testuser</code>, Пароль: <code>test123</code></small></p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #666;">
                <p>Журавлева Виктория Александровна, ФБИ-34</p>
                <a href="/" style="color: #667eea;">← На главную страницу</a>
            </div>
        </div>
    </body>
    </html>
    '''

# ================= АВТОРИЗАЦИЯ =================

# Вход
@lab8.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        error_html = ''
        if request.args.get('error'):
            error_html = f'<div class="error">{request.args.get("error")}</div>'
        
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Вход</title>
            <style>
                body {{ max-width: 400px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #555; }}
                input {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }}
                .btn {{ display: block; width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                .btn:hover {{ background: #5a67d8; }}
                .error {{ color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #f5c6cb; }}
                .links {{ text-align: center; margin-top: 20px; }}
                .links a {{ color: #667eea; text-decoration: none; }}
                .links a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Вход в систему</h1>
                {error_html}
                <form method="post">
                    <div class="form-group">
                        <label>Логин:</label>
                        <input type="text" name="login" required>
                    </div>
                    <div class="form-group">
                        <label>Пароль:</label>
                        <input type="password" name="password" required>
                    </div>
                    <button type="submit" class="btn">Войти</button>
                </form>
                <div class="links">
                    <p>Нет аккаунта? <a href="/lab8/register/">Зарегистрироваться</a></p>
                    <p><a href="/lab8/">← Назад на главную lab8</a></p>
                </div>
            </div>
        </body>
        </html>
        '''
    
    login_form = request.form['login']
    password_form = request.form['password']
    
    User, Article = get_models()
    user = User.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user)
        return redirect('/lab8/?message=Вы успешно вошли в систему!&type=success')
    else:
        return redirect('/lab8/login/?error=Неверный логин или пароль')

# Регистрация
@lab8.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        error_html = ''
        if request.args.get('error'):
            error_html = f'<div class="error">{request.args.get("error")}</div>'
        
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Регистрация</title>
            <style>
                body {{ max-width: 400px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #555; }}
                input {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }}
                .btn {{ display: block; width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                .btn:hover {{ background: #218838; }}
                .error {{ color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #f5c6cb; }}
                .links {{ text-align: center; margin-top: 20px; }}
                .links a {{ color: #667eea; text-decoration: none; }}
                .links a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Регистрация</h1>
                {error_html}
                <form method="post">
                    <div class="form-group">
                        <label>Логин:</label>
                        <input type="text" name="login" required>
                    </div>
                    <div class="form-group">
                        <label>Пароль:</label>
                        <input type="password" name="password" required>
                    </div>
                    <button type="submit" class="btn">Зарегистрироваться</button>
                </form>
                <div class="links">
                    <p>Уже есть аккаунт? <a href="/lab8/login/">Войти</a></p>
                    <p><a href="/lab8/">← Назад на главную lab8</a></p>
                </div>
            </div>
        </body>
        </html>
        '''
    
    login_form = request.form['login']
    password_form = request.form['password']
    
    User, Article = get_models()
    db = get_db()
    
    if User.query.filter_by(login=login_form).first():
        return redirect('/lab8/register/?error=Пользователь с таким логином уже существует')
    
    hashed_password = generate_password_hash(password_form)
    new_user = User(login=login_form, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    return redirect('/lab8/?message=Регистрация прошла успешно! Вы вошли в систему.&type=success')

# ================= УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ =================

# Создание таблиц
@lab8.route('/create-tables/')
def create_tables():
    db = get_db()
    db.create_all()
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Таблицы созданы</title>
        <style>
            body { max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; background: #f5f5f5; }
            .success { color: #28a745; font-size: 24px; margin-bottom: 20px; }
            .btn { display: inline-block; padding: 10px 20px; margin: 10px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
            .btn:hover { background: #5a67d8; }
        </style>
    </head>
    <body>
        <div class="success">✅ Таблицы созданы!</div>
        <p>Таблицы <strong>users</strong> и <strong>articles</strong> успешно созданы.</p>
        <div>
            <a href="/lab8/" class="btn">На главную lab8</a>
            <a href="/lab8/test-data/" class="btn">Создать тестовые данные</a>
        </div>
    </body>
    </html>
    '''

# Тестовые данные
@lab8.route('/test-data/')
def test_data():
    User, Article = get_models()
    db = get_db()
    
    # Создаем тестового пользователя
    test_user = User.query.filter_by(login='testuser').first()
    if not test_user:
        test_user = User(login='testuser', password=generate_password_hash('test123'))
        db.session.add(test_user)
        db.session.commit()
    
    # Создаем тестовые статьи
    test_articles = [
        {
            'title': 'Добро пожаловать в базу знаний!',
            'text': 'Это демонстрационная публичная статья. Здесь вы можете размещать любую полезную информацию. База знаний позволяет хранить статьи, заметки и другие материалы.',
            'public': True,
            'favorite': True
        },
        {
            'title': 'Руководство по использованию',
            'text': 'В этом руководстве описаны основные возможности системы:\n1. Создание статей\n2. Редактирование статей\n3. Публикация статей\n4. Просмотр публичных статей\n5. Управление своими статьями',
            'public': True,
            'favorite': False
        },
        {
            'title': 'Личные заметки',
            'text': 'Эта статья приватная и видна только автору. Здесь можно хранить личные заметки и черновики. Используйте приватные статьи для хранения информации, которую не хотите делать публичной.',
            'public': False,
            'favorite': True
        }
    ]
    
    articles_created = 0
    for article_data in test_articles:
        article = Article.query.filter_by(title=article_data['title'], user_id=test_user.id).first()
        if not article:
            new_article = Article(
                user_id=test_user.id,
                title=article_data['title'],
                article_text=article_data['text'],
                is_public=article_data['public'],
                is_favorite=article_data['favorite'],
                likes=0
            )
            db.session.add(new_article)
            articles_created += 1
    
    db.session.commit()
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Тестовые данные</title>
        <style>
            body {{ max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; background: #f5f5f5; }}
            .success {{ color: #28a745; font-size: 24px; margin-bottom: 20px; }}
            .info {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: left; }}
            .btn {{ display: inline-block; padding: 10px 20px; margin: 10px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
            .btn:hover {{ background: #5a67d8; }}
        </style>
    </head>
    <body>
        <div class="success">✅ Тестовые данные созданы!</div>
        
        <div class="info">
            <h3 style="margin-top: 0;">Данные для входа:</h3>
            <p><strong>Логин:</strong> testuser</p>
            <p><strong>Пароль:</strong> test123</p>
            <p><strong>Создано:</strong> {articles_created} новых статей</p>
            <p><strong>Тестовый пользователь:</strong> {'уже существовал (не создавался заново)' if articles_created == 0 else 'создан/обновлен'}</p>
        </div>
        
        <div>
            <a href="/lab8/login/" class="btn">Войти с тестовым аккаунтом</a>
            <a href="/lab8/" class="btn">На главную lab8</a>
        </div>
        
        <p style="margin-top: 20px; color: #666;"><small>Если тестовый пользователь уже существовал, статьи могли не добавиться повторно.</small></p>
    </body>
    </html>
    '''

# ================= СТАТЬИ =================

# Публичные статьи (доступно всем)
@lab8.route('/public/')
def public_articles():
    User, Article = get_models()
    articles = Article.query.filter_by(is_public=True).order_by(Article.created_at.desc()).all()
    
    articles_html = ''
    if articles:
        for article in articles:
            user = User.query.get(article.user_id)
            author = user.login if user else "Неизвестный автор"
            
            articles_html += f'''
            <div class="article-card">
                <h3 style="margin-top: 0; color: #333;">{article.title}</h3>
                <p style="line-height: 1.6; white-space: pre-wrap;">{format_text(article.article_text, 300)}</p>
                <div style="color: #666; font-size: 14px; border-top: 1px solid #ddd; padding-top: 10px;">
                    <span>👤 Автор: <strong>{author}</strong></span> | 
                    <span>⭐ Избранное: {'⭐' if article.is_favorite else '☆'}</span> | 
                    <span>❤️ Лайки: {article.likes}</span> | 
                    <span>🌐 Публичная: {'✅' if article.is_public else '❌'}</span>
                </div>
            </div>
            '''
    else:
        articles_html = '''
        <div style="text-align: center; padding: 40px; color: #666;">
            <h3>Публичных статей пока нет</h3>
            <p>Будьте первым, кто создаст публичную статью!</p>
            <p>Войдите в систему и создайте свою первую статью.</p>
        </div>
        '''
    
    # Кнопки в зависимости от авторизации
    auth_buttons = ''
    if current_user.is_authenticated:
        auth_buttons = '''
            <a href="/lab8/articles/" class="btn">📝 Мои статьи</a>
            <a href="/lab8/create/" class="btn" style="background:#28a745;">➕ Создать статью</a>
        '''
    else:
        auth_buttons = '''
            <a href="/lab8/login/" class="btn">🔑 Войти</a>
            <a href="/lab8/register/" class="btn" style="background:#28a745;">📝 Зарегистрироваться</a>
        '''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Публичные статьи</title>
        <style>
            body {{ max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 10px; }}
            .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }}
            .btn:hover {{ background: #5a67d8; text-decoration: none; color: white; }}
            .article-card {{ border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; background: #f8f9fa; }}
            .header-actions {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; gap: 15px; }}
            @media (max-width: 768px) {{
                .header-actions {{ flex-direction: column; align-items: stretch; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 Публичные статьи</h1>
            <div class="subtitle">Все публичные статьи: {len(articles)}</div>
            
            <div class="header-actions">
                <div>
                    <a href="/lab8/" class="btn">← На главную lab8</a>
                </div>
                <div>
                    {auth_buttons}
                </div>
            </div>
            
            {articles_html}
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/lab8/" class="btn">← На главную lab8</a>
            </div>
        </div>
    </body>
    </html>
    '''

# Мои статьи (только для авторизованных)
@lab8.route('/articles/')
@login_required
def articles():
    User, Article = get_models()
    user_articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.created_at.desc()).all()
    
    articles_html = ''
    if user_articles:
        for article in user_articles:
            articles_html += f'''
            <div class="article-card">
                <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 10px;">
                    <h3 style="margin-top: 0; color: #333; flex: 1;">{article.title}</h3>
                    <div class="article-actions">
                        <a href="/lab8/edit/{article.id}/" class="btn" style="padding: 8px 16px; background: #ffc107; color: #212529; text-decoration: none;">✏️ Редактировать</a>
                        <a href="/lab8/delete/{article.id}/" class="btn" style="padding: 8px 16px; background: #dc3545; color: white; text-decoration: none;" 
                           onclick="return confirm('Вы уверены, что хотите удалить статью \\'{article.title}\\'?')">🗑️ Удалить</a>
                    </div>
                </div>
                
                <div style="margin: 15px 0;">
                    <p style="line-height: 1.6; white-space: pre-wrap;">{format_text(article.article_text, 200)}</p>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; color: #666; font-size: 14px; border-top: 1px solid #ddd; padding-top: 10px; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span>🌐 Публичная: {'✅' if article.is_public else '❌'}</span> | 
                        <span>⭐ Избранное: {'⭐' if article.is_favorite else '☆'}</span> | 
                        <span>❤️ Лайки: {article.likes}</span>
                    </div>
                    <div style="text-align: right; font-size: 12px;">
                        <span>Создано: {article.created_at.strftime("%d.%m.%Y %H:%M") if article.created_at else "Неизвестно"}</span>
                    </div>
                </div>
            </div>
            '''
    else:
        articles_html = '''
        <div style="text-align: center; padding: 40px; color: #666;">
            <h3>У вас еще нет статей</h3>
            <p>Создайте свою первую статью, нажав на кнопку ниже!</p>
        </div>
        '''
    
    message_html = ''
    if request.args.get('message'):
        message = request.args.get('message')
        message_type = request.args.get('type', 'success')
        message_html = f'''
        <div class="alert alert-{message_type}" style="padding:15px; border-radius:5px; margin-bottom:20px; 
                background:{"#d4edda" if message_type=="success" else "#f8d7da"}; 
                color:{"#155724" if message_type=="success" else "#721c24"};
                border:1px solid {"#c3e6cb" if message_type=="success" else "#f5c6cb"};">
            {message}
        </div>
        '''
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Мои статьи</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 10px; }}
            .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; transition: background 0.3s; border: none; cursor: pointer; font-size: 14px; }}
            .btn:hover {{ background: #5a67d8; text-decoration: none; color: white; }}
            .btn-success {{ background: #28a745; }}
            .btn-success:hover {{ background: #218838; }}
            .btn-secondary {{ background: #6c757d; }}
            .header-actions {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; gap: 15px; }}
            .article-card {{ border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; background: #f8f9fa; }}
            .article-actions {{ margin-top: 10px; display: flex; gap: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 Мои статьи</h1>
            <div class="subtitle">Всего статей: {len(user_articles)}</div>
            
            {message_html}
            
            <div class="header-actions">
                <a href="/lab8/create/" class="btn btn-success">➕ Создать новую статью</a>
                <div>
                    <a href="/lab8/public/" class="btn">🌐 Публичные статьи</a>
                    <a href="/lab8/" class="btn">← На главную lab8</a>
                </div>
            </div>
            
            {articles_html}
            
            {f'<div style="text-align: center; margin-top: 30px; color: #666;">Показано {len(user_articles)} статей</div>' if user_articles else ''}
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/lab8/create/" class="btn btn-success">➕ Создать ещё одну статью</a>
            </div>
        </div>
        
        <script>
            // Обработка подтверждения удаления
            document.addEventListener('DOMContentLoaded', function() {{
                const deleteLinks = document.querySelectorAll('a[href*="/lab8/delete/"]');
                deleteLinks.forEach(link => {{
                    link.addEventListener('click', function(e) {{
                        if (!confirm('Вы уверены, что хотите удалить эту статью?')) {{
                            e.preventDefault();
                        }}
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    '''

# Создать статью
@lab8.route('/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <html>
        <head>
            <title>Создать статью</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; text-align: center; margin-bottom: 30px; }
                .form-group { margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
                input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }
                textarea { height: 200px; resize: vertical; font-family: inherit; }
                .checkbox-group { display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
                .checkbox-group label { display: flex; align-items: center; gap: 5px; font-weight: normal; cursor: pointer; }
                .checkbox-group input[type="checkbox"] { width: auto; }
                .btn { display: inline-block; padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background 0.3s; text-decoration: none; }
                .btn:hover { background: #5a67d8; }
                .btn-success { background: #28a745; }
                .btn-secondary { background: #6c757d; }
                .links { text-align: center; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>➕ Создать статью</h1>
                
                <form method="post">
                    <div class="form-group">
                        <label for="title">Название статьи:</label>
                        <input type="text" id="title" name="title" required maxlength="100" placeholder="Введите название статьи (макс. 100 символов)">
                        <div id="title-counter" style="font-size: 12px; color: #666; margin-top: 5px;">0/100 символов</div>
                    </div>
                    
                    <div class="form-group">
                        <label for="text">Текст статьи:</label>
                        <textarea id="text" name="text" required placeholder="Напишите текст вашей статьи..."></textarea>
                        <div id="text-counter" style="font-size: 12px; color: #666; margin-top: 5px;">0 символов</div>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" name="is_public" checked>
                            🌐 Публичная статья (видят все)
                        </label>
                        <label>
                            <input type="checkbox" name="is_favorite">
                            ⭐ В избранное
                        </label>
                    </div>
                    
                    <button type="submit" class="btn btn-success">📝 Создать статью</button>
                </form>
                
                <div class="links">
                    <a href="/lab8/articles/" class="btn btn-secondary">← К списку статей</a>
                    <a href="/lab8/" class="btn btn-secondary">← На главную lab8</a>
                </div>
            </div>
            
            <script>
                // Подсчёт символов в заголовке
                const titleInput = document.getElementById('title');
                const titleCounter = document.getElementById('title-counter');
                
                titleInput.addEventListener('input', function() {
                    const length = this.value.length;
                    titleCounter.textContent = length + '/100 символов';
                    if (length > 100) {
                        titleCounter.style.color = '#dc3545';
                    } else if (length > 80) {
                        titleCounter.style.color = '#ffc107';
                    } else {
                        titleCounter.style.color = '#28a745';
                    }
                });
                
                // Подсчёт символов в тексте
                const textInput = document.getElementById('text');
                const textCounter = document.getElementById('text-counter');
                
                textInput.addEventListener('input', function() {
                    const length = this.value.length;
                    textCounter.textContent = length + ' символов';
                    if (length > 5000) {
                        textCounter.style.color = '#dc3545';
                    } else if (length > 3000) {
                        textCounter.style.color = '#ffc107';
                    } else {
                        textCounter.style.color = '#28a745';
                    }
                });
            </script>
        </body>
        </html>
        '''
    
    title = request.form['title']
    text = request.form['text']
    is_public = 'is_public' in request.form
    is_favorite = 'is_favorite' in request.form
    
    if not title or not text:
        return redirect('/lab8/create/?error=Название и текст статьи не могут быть пустыми')
    
    User, Article = get_models()
    db = get_db()
    
    article = Article(
        user_id=current_user.id,
        title=title[:100],
        article_text=text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(article)
    db.session.commit()
    
    return redirect('/lab8/articles/?message=Статья успешно создана!&type=success')

# Редактировать статью
@lab8.route('/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    User, Article = get_models()
    db = get_db()
    
    article = Article.query.get_or_404(article_id)
    
    # Проверяем права доступа
    if article.user_id != current_user.id:
        return redirect('/lab8/articles/?error=У вас нет прав для редактирования этой статьи&type=error')
    
    if request.method == 'GET':
        is_public_checked = 'checked' if article.is_public else ''
        is_favorite_checked = 'checked' if article.is_favorite else ''
        
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Редактировать статью</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; color: #555; font-weight: bold; }}
                input[type="text"], textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }}
                textarea {{ height: 300px; resize: vertical; font-family: inherit; }}
                .checkbox-group {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
                .checkbox-group label {{ display: flex; align-items: center; gap: 5px; font-weight: normal; cursor: pointer; }}
                .checkbox-group input[type="checkbox"] {{ width: auto; }}
                .btn-group {{ display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background 0.3s; text-decoration: none; }}
                .btn:hover {{ background: #5a67d8; }}
                .btn-success {{ background: #28a745; }}
                .btn-danger {{ background: #dc3545; }}
                .btn-secondary {{ background: #6c757d; }}
                .btn-warning {{ background: #ffc107; color: #212529; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✏️ Редактировать статью</h1>
                
                <form method="post">
                    <div class="form-group">
                        <label for="title">Название статьи:</label>
                        <input type="text" id="title" name="title" value="{article.title}" required maxlength="100">
                        <div id="title-counter" style="font-size: 12px; color: #666; margin-top: 5px;">0/100 символов</div>
                    </div>
                    
                    <div class="form-group">
                        <label for="text">Текст статьи:</label>
                        <textarea id="text" name="text" required>{article.article_text}</textarea>
                        <div id="text-counter" style="font-size: 12px; color: #666; margin-top: 5px;">0 символов</div>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" name="is_public" {is_public_checked}>
                            🌐 Публичная статья
                        </label>
                        <label>
                            <input type="checkbox" name="is_favorite" {is_favorite_checked}>
                            ⭐ В избранное
                        </label>
                    </div>
                    
                    <div class="btn-group">
                        <button type="submit" class="btn btn-success">💾 Сохранить изменения</button>
                        <a href="/lab8/articles/" class="btn btn-secondary">↩️ Отмена</a>
                        <a href="/lab8/delete/{article_id}/" class="btn btn-danger" 
                           onclick="return confirm('Вы уверены, что хотите удалить статью \\'{article.title}\\'?')">🗑️ Удалить статью</a>
                    </div>
                </form>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/lab8/articles/" class="btn">← К списку статей</a>
                    <a href="/lab8/" class="btn">← На главную lab8</a>
                </div>
            </div>
            
            <script>
                // Подсчёт символов в заголовке
                const titleInput = document.getElementById('title');
                const titleCounter = document.getElementById('title-counter');
                
                titleInput.addEventListener('input', function() {{
                    const length = this.value.length;
                    titleCounter.textContent = length + '/100 символов';
                    if (length > 100) {{
                        titleCounter.style.color = '#dc3545';
                    }} else if (length > 80) {{
                        titleCounter.style.color = '#ffc107';
                    }} else {{
                        titleCounter.style.color = '#28a745';
                    }}
                }});
                
                // Инициализация счётчика заголовка
                titleInput.dispatchEvent(new Event('input'));
                
                // Подсчёт символов в тексте
                const textInput = document.getElementById('text');
                const textCounter = document.getElementById('text-counter');
                
                textInput.addEventListener('input', function() {{
                    const length = this.value.length;
                    textCounter.textContent = length + ' символов';
                    if (length > 10000) {{
                        textCounter.style.color = '#dc3545';
                    }} else if (length > 5000) {{
                        textCounter.style.color = '#ffc107';
                    }} else {{
                        textCounter.style.color = '#28a745';
                    }}
                }});
                
                // Инициализация счётчика текста
                textInput.dispatchEvent(new Event('input'));
            </script>
        </body>
        </html>
        '''
    
    # Обработка POST запроса (сохранение изменений)
    title = request.form['title']
    text = request.form['text']
    is_public = 'is_public' in request.form
    is_favorite = 'is_favorite' in request.form
    
    if not title or not text:
        return redirect(f'/lab8/edit/{article_id}/?error=Название и текст статьи не могут быть пустыми')
    
    # Обновляем статью
    article.title = title[:100]
    article.article_text = text
    article.is_public = is_public
    article.is_favorite = is_favorite
    
    db.session.commit()
    
    return redirect('/lab8/articles/?message=Статья успешно обновлена!&type=success')

# Удалить статью
@lab8.route('/delete/<int:article_id>/')
@login_required
def delete_article(article_id):
    User, Article = get_models()
    db = get_db()
    
    article = Article.query.get_or_404(article_id)
    
    # Проверяем права доступа
    if article.user_id != current_user.id:
        return redirect('/lab8/articles/?error=У вас нет прав для удаления этой статьи&type=error')
    
    article_title = article.title
    
    # Удаляем статью
    db.session.delete(article)
    db.session.commit()
    
    return redirect(f'/lab8/articles/?message=Статья "{article_title}" успешно удалена!&type=success')

# Выход
@lab8.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/?message=Вы вышли из системы&type=success')