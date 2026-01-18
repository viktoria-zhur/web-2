from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

# Функция для получения доступа к БД
def get_db():
    from app import db, User, Article
    return db, User, Article

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =================
def execute_in_app_context(func):
    """Декоратор для выполнения функции в контексте приложения"""
    def wrapper(*args, **kwargs):
        from app import app
        with app.app_context():
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ================= МАРШРУТЫ =================
@lab8.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Lab 8 - База знаний</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .menu {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 30px 0;
                justify-content: center;
            }
            .btn {
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
            }
            .btn:hover {
                background: #5a67d8;
                text-decoration: none;
                color: white;
            }
            .btn-secondary {
                background: #6c757d;
            }
            .btn-success {
                background: #28a745;
            }
            .btn-danger {
                background: #dc3545;
            }
            .btn-info {
                background: #17a2b8;
            }
            .btn-warning {
                background: #ffc107;
                color: #212529;
            }
            .flash-messages {
                margin: 20px 0;
            }
            .alert {
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .alert-success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .alert-error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .user-info {
                text-align: center;
                padding: 15px;
                background: #e9ecef;
                border-radius: 5px;
                margin: 20px 0;
            }
            .db-actions {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 База знаний</h1>
            <div class="subtitle">Лабораторная работа 8 - Flask и БД (ORM)</div>
            
            <div class="flash-messages">
                <!-- Сообщения будут здесь -->
            </div>
            
            <div class="user-info">
                <!-- Информация о пользователе -->
            </div>
            
            <div class="menu">
                <!-- Меню -->
            </div>
            
            <div class="db-actions">
                <h3>Управление базой данных</h3>
                <p>Для тестирования используйте эти ссылки:</p>
                <div style="margin: 15px 0;">
                    <a href="/lab8/create-tables/" class="btn btn-info">Создать таблицы</a>
                    <a href="/lab8/check-db/" class="btn btn-info">Проверить БД</a>
                    <a href="/lab8/test-data/" class="btn btn-info">Тестовые данные</a>
                </div>
                <p><small>После создания таблиц и тестовых данных используйте:</small></p>
                <p><small>Логин: <code>testuser</code>, Пароль: <code>test123</code></small></p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #666;">
                <p>Журавлева Виктория Александровна, ФБИ-34</p>
                <a href="/" style="color: #667eea;">← На главную страницу</a>
            </div>
        </div>
        
        <script>
            // Динамическое заполнение информации
            const userInfo = document.querySelector('.user-info');
            const menu = document.querySelector('.menu');
            
            // Проверяем авторизацию через fetch
            fetch('/lab8/check-auth')
                .then(response => response.json())
                .then(data => {
                    if (data.authenticated) {
                        userInfo.innerHTML = `<p>Вы вошли как: <strong>${data.user_login}</strong></p>`;
                        menu.innerHTML = `
                            <a href="/lab8/articles/" class="btn">📄 Мои статьи</a>
                            <a href="/lab8/create/" class="btn btn-success">✏️ Создать статью</a>
                            <a href="/lab8/logout/" class="btn btn-danger">🚪 Выход</a>
                        `;
                    } else {
                        userInfo.innerHTML = '<p>Вы не авторизованы. Войдите или зарегистрируйтесь.</p>';
                        menu.innerHTML = `
                            <a href="/lab8/login/" class="btn">🔐 Вход</a>
                            <a href="/lab8/register/" class="btn btn-success">📝 Регистрация</a>
                        `;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    userInfo.innerHTML = '<p>Ошибка загрузки данных пользователя.</p>';
                    menu.innerHTML = `
                        <a href="/lab8/login/" class="btn">Вход</a>
                        <a href="/lab8/register/" class="btn btn-success">Регистрация</a>
                    `;
                });
            
            // Показываем flash сообщения
            const urlParams = new URLSearchParams(window.location.search);
            const message = urlParams.get('message');
            const type = urlParams.get('type');
            
            if (message) {
                const flashMessages = document.querySelector('.flash-messages');
                const div = document.createElement('div');
                div.className = 'alert alert-' + (type || 'success');
                div.textContent = decodeURIComponent(message);
                flashMessages.appendChild(div);
                
                // Очищаем URL от параметров
                window.history.replaceState({}, document.title, window.location.pathname);
            }
        </script>
    </body>
    </html>
    '''

@lab8.route('/check-auth')
def check_auth():
    """Проверка авторизации через AJAX"""
    if current_user.is_authenticated:
        return {
            'authenticated': True,
            'user_login': current_user.login
        }
    return {'authenticated': False}

@lab8.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <html>
        <head>
            <title>Вход в систему</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 400px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    text-align: center;
                    color: #333;
                    margin-bottom: 30px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    color: #555;
                    font-weight: bold;
                }
                input[type="text"],
                input[type="password"] {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                .checkbox-group {
                    margin: 15px 0;
                }
                .checkbox-group label {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-weight: normal;
                    cursor: pointer;
                }
                .checkbox-group input[type="checkbox"] {
                    width: auto;
                }
                .btn {
                    display: block;
                    width: 100%;
                    padding: 12px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                .btn:hover {
                    background: #5a67d8;
                }
                .error {
                    color: #dc3545;
                    background: #f8d7da;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border: 1px solid #f5c6cb;
                }
                .links {
                    text-align: center;
                    margin-top: 20px;
                }
                .links a {
                    color: #667eea;
                    text-decoration: none;
                }
                .links a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔐 Вход в систему</h1>
                
                <form action="/lab8/login/" method="post">
                    <div class="form-group">
                        <label for="login">Логин:</label>
                        <input type="text" id="login" name="login" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Пароль:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" name="remember">
                            Запомнить меня
                        </label>
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
    
    # Обработка POST запроса
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'
    
    if not login_form or not password_form:
        return redirect(url_for('lab8.login') + '?message=' + 'Логин и пароль не могут быть пустыми' + '&type=error')
    
    from app import app
    with app.app_context():
        db, User, Article = get_db()
        user = User.query.filter_by(login=login_form).first()
        
        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect(url_for('lab8.index') + '?message=' + 'Вы успешно вошли в систему!' + '&type=success')
        else:
            return redirect(url_for('lab8.login') + '?message=' + 'Неверный логин или пароль' + '&type=error')

@lab8.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <html>
        <head>
            <title>Регистрация</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 400px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    text-align: center;
                    color: #333;
                    margin-bottom: 30px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    color: #555;
                    font-weight: bold;
                }
                input[type="text"],
                input[type="password"] {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                .btn {
                    display: block;
                    width: 100%;
                    padding: 12px;
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                .btn:hover {
                    background: #218838;
                }
                .error {
                    color: #dc3545;
                    background: #f8d7da;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border: 1px solid #f5c6cb;
                }
                .links {
                    text-align: center;
                    margin-top: 20px;
                }
                .links a {
                    color: #667eea;
                    text-decoration: none;
                }
                .links a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📝 Регистрация</h1>
                
                <form action="/lab8/register/" method="post">
                    <div class="form-group">
                        <label for="login">Логин:</label>
                        <input type="text" id="login" name="login" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Пароль:</label>
                        <input type="password" id="password" name="password" required>
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
    
    # Обработка POST запроса
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        return redirect(url_for('lab8.register') + '?message=' + 'Логин и пароль не могут быть пустыми' + '&type=error')
    
    from app import app
    with app.app_context():
        db, User, Article = get_db()
        
        existing_user = User.query.filter_by(login=login_form).first()
        if existing_user:
            return redirect(url_for('lab8.register') + '?message=' + 'Пользователь с таким логином уже существует' + '&type=error')
        
        hashed_password = generate_password_hash(password_form)
        new_user = User(login=login_form, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user, remember=False)
        return redirect(url_for('lab8.index') + '?message=' + 'Регистрация прошла успешно! Вы вошли в систему.' + '&type=success')

@lab8.route('/articles/')
@login_required
def articles():
    from app import app
    with app.app_context():
        db, User, Article = get_db()
        
        user_articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.created_at.desc() if hasattr(Article, 'created_at') else Article.id.desc()).all()
        
        articles_html = ''
        if user_articles:
            for article in user_articles:
                # Безопасное получение даты создания
                created_date = ''
                if hasattr(article, 'created_at') and article.created_at:
                    created_date = article.created_at.strftime("%d.%m.%Y %H:%M")
                else:
                    created_date = "Неизвестно"
                
                # Безопасное получение даты обновления
                updated_date = ''
                if hasattr(article, 'updated_at') and article.updated_at:
                    updated_date = f'<br><span>Обновлено: {article.updated_at.strftime("%d.%m.%Y %H:%M")}</span>'
                
                articles_html += f'''
                <div style="border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; background: #f8f9fa;">
                    <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 10px;">
                        <h3 style="margin-top: 0; color: #333; flex: 1;">{article.title}</h3>
                        <div style="display: flex; gap: 10px;">
                            <a href="/lab8/edit/{article.id}/" class="btn" style="padding: 8px 16px; background: #ffc107; color: #212529; text-decoration: none;">✏️ Редактировать</a>
                            <a href="/lab8/delete/{article.id}/" class="btn" style="padding: 8px 16px; background: #dc3545; color: white; text-decoration: none;" 
                               onclick="return confirm('Вы уверены, что хотите удалить эту статью?')">🗑️ Удалить</a>
                        </div>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <p style="line-height: 1.6; white-space: pre-wrap;">{article.article_text[:300]}{'...' if len(article.article_text) > 300 else ''}</p>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; color: #666; font-size: 14px; border-top: 1px solid #ddd; padding-top: 10px; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <span>Публичная: {'✅' if article.is_public else '❌'}</span> | 
                            <span>Избранное: {'⭐' if article.is_favorite else '☆'}</span> | 
                            <span>Лайки: {article.likes}</span>
                        </div>
                        <div style="text-align: right;">
                            <span>Создано: {created_date}</span>
                            {updated_date}
                        </div>
                    </div>
                </div>
                '''
        else:
            articles_html = '''
            <div style="text-align: center; padding: 40px; color: #666;">
                <h3>📝 У вас еще нет статей</h3>
                <p>Создайте свою первую статью, нажав на кнопку ниже!</p>
            </div>
            '''
        
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Мои статьи</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1000px;
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
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background 0.3s;
                    border: none;
                    cursor: pointer;
                    font-size: 14px;
                }}
                .btn:hover {{
                    background: #5a67d8;
                    text-decoration: none;
                    color: white;
                }}
                .btn-success {{
                    background: #28a745;
                }}
                .btn-success:hover {{
                    background: #218838;
                }}
                .btn-secondary {{
                    background: #6c757d;
                }}
                .header-actions {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    flex-wrap: wrap;
                    gap: 15px;
                }}
                .article-actions {{
                    display: flex;
                    gap: 5px;
                }}
                @media (max-width: 768px) {{
                    .header-actions {{
                        flex-direction: column;
                        align-items: stretch;
                    }}
                    .article-actions {{
                        margin-top: 15px;
                        justify-content: flex-start;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📄 Мои статьи</h1>
                <div class="subtitle">Всего статей: {len(user_articles)}</div>
                
                <div class="header-actions">
                    <a href="/lab8/create/" class="btn btn-success">➕ Создать новую статью</a>
                    <div>
                        <a href="/lab8/" class="btn">← На главную lab8</a>
                        <a href="/lab8/logout/" class="btn btn-secondary">🚪 Выход</a>
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
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    color: #555;
                    font-weight: bold;
                }
                input[type="text"],
                textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                textarea {
                    height: 200px;
                    resize: vertical;
                    font-family: inherit;
                }
                .checkbox-group {
                    display: flex;
                    gap: 20px;
                    margin: 20px 0;
                    flex-wrap: wrap;
                }
                .checkbox-group label {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-weight: normal;
                    cursor: pointer;
                }
                .checkbox-group input[type="checkbox"] {
                    width: auto;
                }
                .btn {
                    display: inline-block;
                    padding: 12px 24px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                    text-decoration: none;
                }
                .btn:hover {
                    background: #5a67d8;
                }
                .btn-success {
                    background: #28a745;
                }
                .btn-secondary {
                    background: #6c757d;
                }
                .links {
                    text-align: center;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✏️ Создать статью</h1>
                
                <form action="/lab8/create/" method="post">
                    <div class="form-group">
                        <label for="title">Название статьи:</label>
                        <input type="text" id="title" name="title" required maxlength="50" placeholder="Введите название статьи (макс. 50 символов)">
                    </div>
                    
                    <div class="form-group">
                        <label for="article_text">Текст статьи:</label>
                        <textarea id="article_text" name="article_text" required placeholder="Напишите текст вашей статьи..."></textarea>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" name="is_public">
                            Публичная статья
                        </label>
                        <label>
                            <input type="checkbox" name="is_favorite">
                            В избранное
                        </label>
                    </div>
                    
                    <button type="submit" class="btn btn-success">Создать статью</button>
                </form>
                
                <div class="links">
                    <a href="/lab8/articles/" class="btn btn-secondary">← К списку статей</a>
                    <a href="/lab8/" class="btn btn-secondary">← На главную lab8</a>
                </div>
            </div>
            
            <script>
                // Подсчёт символов в заголовке
                const titleInput = document.getElementById('title');
                const charCounter = document.createElement('div');
                charCounter.style.marginTop = '5px';
                charCounter.style.fontSize = '12px';
                charCounter.style.color = '#666';
                titleInput.parentNode.appendChild(charCounter);
                
                titleInput.addEventListener('input', function() {
                    const length = this.value.length;
                    charCounter.textContent = `${length}/50 символов`;
                    if (length > 50) {
                        charCounter.style.color = '#dc3545';
                    } else if (length > 40) {
                        charCounter.style.color = '#ffc107';
                    } else {
                        charCounter.style.color = '#28a745';
                    }
                });
                
                // Подсчёт символов в тексте
                const textInput = document.getElementById('article_text');
                const textCounter = document.createElement('div');
                textCounter.style.marginTop = '5px';
                textCounter.style.fontSize = '12px';
                textCounter.style.color = '#666';
                textInput.parentNode.appendChild(textCounter);
                
                textInput.addEventListener('input', function() {
                    const length = this.value.length;
                    textCounter.textContent = `${length} символов`;
                    if (length > 1000) {
                        textCounter.style.color = '#dc3545';
                    } else if (length > 500) {
                        textCounter.style.color = '#ffc107';
                    } else {
                        textCounter.style.color = '#28a745';
                    }
                });
            </script>
        </body>
        </html>
        '''
    
    # Обработка POST запроса
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return redirect(url_for('lab8.create_article') + '?message=' + 'Название и текст статьи не могут быть пустыми' + '&type=error')
    
    from app import app
    with app.app_context():
        db, User, Article = get_db()
        
        new_article = Article(
            user_id=current_user.id,
            title=title[:50],
            article_text=article_text,
            is_public=is_public,
            is_favorite=is_favorite,
            likes=0
        )
        
        db.session.add(new_article)
        db.session.commit()
        
        return redirect(url_for('lab8.articles') + '?message=' + 'Статья успешно создана!' + '&type=success')

@lab8.route('/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    """Редактирование существующей статьи"""
    from app import app
    
    with app.app_context():
        db, User, Article = get_db()
        
        # Получаем статью
        article = Article.query.get_or_404(article_id)
        
        # Проверяем, что статья принадлежит текущему пользователю
        if article.user_id != current_user.id:
            return redirect(url_for('lab8.articles') + '?message=' + 'У вас нет прав для редактирования этой статьи' + '&type=error')
        
        if request.method == 'GET':
            # Показываем форму с текущими данными
            return f'''
            <!doctype html>
            <html>
            <head>
                <title>Редактировать статью</title>
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
                        margin-bottom: 30px;
                    }}
                    .form-group {{
                        margin-bottom: 20px;
                    }}
                    label {{
                        display: block;
                        margin-bottom: 5px;
                        color: #555;
                        font-weight: bold;
                    }}
                    input[type="text"],
                    textarea {{
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                        box-sizing: border-box;
                    }}
                    textarea {{
                        height: 300px;
                        resize: vertical;
                        font-family: inherit;
                    }}
                    .checkbox-group {{
                        display: flex;
                        gap: 20px;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }}
                    .checkbox-group label {{
                        display: flex;
                        align-items: center;
                        gap: 5px;
                        font-weight: normal;
                        cursor: pointer;
                    }}
                    .checkbox-group input[type="checkbox"] {{
                        width: auto;
                    }}
                    .btn-group {{
                        display: flex;
                        gap: 10px;
                        margin-top: 20px;
                        flex-wrap: wrap;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 12px 24px;
                        background: #667eea;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        cursor: pointer;
                        transition: background 0.3s;
                        text-decoration: none;
                    }}
                    .btn:hover {{
                        background: #5a67d8;
                    }}
                    .btn-success {{
                        background: #28a745;
                    }}
                    .btn-danger {{
                        background: #dc3545;
                    }}
                    .btn-secondary {{
                        background: #6c757d;
                    }}
                    .btn-warning {{
                        background: #ffc107;
                        color: #212529;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✏️ Редактировать статью</h1>
                    
                    <form action="/lab8/edit/{article_id}/" method="post">
                        <div class="form-group">
                            <label for="title">Название статьи:</label>
                            <input type="text" id="title" name="title" value="{article.title}" required maxlength="50">
                        </div>
                        
                        <div class="form-group">
                            <label for="article_text">Текст статьи:</label>
                            <textarea id="article_text" name="article_text" required>{article.article_text}</textarea>
                        </div>
                        
                        <div class="checkbox-group">
                            <label>
                                <input type="checkbox" name="is_public" {'checked' if article.is_public else ''}>
                                Публичная статья
                            </label>
                            <label>
                                <input type="checkbox" name="is_favorite" {'checked' if article.is_favorite else ''}>
                                В избранное
                            </label>
                        </div>
                        
                        <div class="btn-group">
                            <button type="submit" class="btn btn-success">💾 Сохранить изменения</button>
                            <a href="/lab8/articles/" class="btn btn-secondary">↩️ Отмена</a>
                            <a href="/lab8/delete/{article_id}/" class="btn btn-danger" 
                               onclick="return confirm('Вы уверены, что хотите удалить эту статью?')">🗑️ Удалить статью</a>
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
                    const charCounter = document.createElement('div');
                    charCounter.style.marginTop = '5px';
                    charCounter.style.fontSize = '12px';
                    charCounter.style.color = '#666';
                    titleInput.parentNode.appendChild(charCounter);
                    
                    titleInput.addEventListener('input', function() {{
                        const length = this.value.length;
                        charCounter.textContent = `${{length}}/50 символов`;
                        if (length > 50) {{
                            charCounter.style.color = '#dc3545';
                        }} else if (length > 40) {{
                            charCounter.style.color = '#ffc107';
                        }} else {{
                            charCounter.style.color = '#28a745';
                        }}
                    }});
                    
                    // Инициализация счётчика
                    titleInput.dispatchEvent(new Event('input'));
                    
                    // Подсчёт символов в тексте
                    const textInput = document.getElementById('article_text');
                    const textCounter = document.createElement('div');
                    textCounter.style.marginTop = '5px';
                    textCounter.style.fontSize = '12px';
                    textCounter.style.color = '#666';
                    textInput.parentNode.appendChild(textCounter);
                    
                    textInput.addEventListener('input', function() {{
                        const length = this.value.length;
                        textCounter.textContent = `${{length}} символов`;
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
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == 'on'
        is_favorite = request.form.get('is_favorite') == 'on'
        
        if not title or not article_text:
            return redirect(url_for('lab8.edit_article', article_id=article_id) + 
                          '?message=' + 'Название и текст статьи не могут быть пустыми' + '&type=error')
        
        # Обновляем статью
        article.title = title[:50]
        article.article_text = article_text
        article.is_public = is_public
        article.is_favorite = is_favorite
        
        # Пытаемся обновить поле updated_at, если оно существует
        if hasattr(article, 'updated_at'):
            from datetime import datetime
            article.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return redirect(url_for('lab8.articles') + '?message=' + 'Статья успешно обновлена!' + '&type=success')

@lab8.route('/delete/<int:article_id>/')
@login_required
def delete_article(article_id):
    """Удаление статьи"""
    from app import app
    
    with app.app_context():
        db, User, Article = get_db()
        
        # Получаем статью
        article = Article.query.get_or_404(article_id)
        
        # Проверяем, что статья принадлежит текущему пользователю
        if article.user_id != current_user.id:
            return redirect(url_for('lab8.articles') + '?message=' + 'У вас нет прав для удаления этой статьи' + '&type=error')
        
        # Удаляем статью
        db.session.delete(article)
        db.session.commit()
        
        return redirect(url_for('lab8.articles') + '?message=' + 'Статья успешно удалена!' + '&type=success')

@lab8.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('lab8.index') + '?message=' + 'Вы вышли из системы' + '&type=success')

@lab8.route('/init-db/')
def init_db():
    return '''
    <!doctype html>
    <html>
    <head><title>Инициализация</title></head>
    <body>
        <h1>База данных уже инициализирована!</h1>
        <p>Таблицы создаются автоматически при запуске приложения.</p>
        <a href="/lab8/">На главную lab8</a>
    </body>
    </html>
    '''

@lab8.route('/test-data/')
def test_data():
    from app import app
    
    with app.app_context():
        db, User, Article = get_db()
        
        # Создаем тестового пользователя
        test_user = User.query.filter_by(login='testuser').first()
        if not test_user:
            test_user = User(
                login='testuser',
                password=generate_password_hash('test123')
            )
            db.session.add(test_user)
            db.session.commit()
            print("✓ Создан тестовый пользователь: testuser / test123")
        
        # Создаем тестовые статьи
        test_articles = [
            {
                'title': 'Тестовая статья 1', 
                'text': 'Это первая тестовая статья для демонстрации работы системы. Она является публичной и содержит базовую информацию о возможностях приложения.', 
                'public': True, 
                'favorite': False
            },
            {
                'title': 'Тестовая статья 2', 
                'text': 'Это вторая тестовая статья. Она отмечена как избранная и содержит более подробную информацию. Статья также является публичной.', 
                'public': True, 
                'favorite': True
            },
            {
                'title': 'Приватная статья', 
                'text': 'Эта статья не публичная и доступна только автору. Здесь может храниться личная информация или черновики.', 
                'public': False, 
                'favorite': False
            },
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
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .success {{
                    color: #28a745;
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                .info {{
                    background: #e9ecef;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                    text-align: left;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 10px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .btn:hover {{
                    background: #5a67d8;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✅ Тестовые данные созданы!</div>
                
                <div class="info">
                    <h3>Данные для входа:</h3>
                    <p><strong>Логин:</strong> testuser</p>
                    <p><strong>Пароль:</strong> test123</p>
                    <p><strong>Создано:</strong> {articles_created} новых статей</p>
                    <p><strong>Тестовый пользователь:</strong> уже существовал (не создавался заново)</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <a href="/lab8/login/" class="btn">Войти с тестовым аккаунтом</a>
                    <a href="/lab8/check-db/" class="btn">Проверить БД</a>
                    <a href="/lab8/" class="btn">На главную lab8</a>
                </div>
                
                <p><small>Если тестовый пользователь уже существовал, статьи могли не добавиться повторно.</small></p>
            </div>
        </body>
        </html>
        '''

@lab8.route('/check-db/')
def check_db_status():
    from app import app
    
    with app.app_context():
        db, User, Article = get_db()
        
        # Подсчет записей
        users_count = User.query.count()
        articles_count = Article.query.count()
        
        # Получаем список пользователей
        users = User.query.all()
        users_list = ''
        for user in users:
            user_articles_count = Article.query.filter_by(user_id=user.id).count()
            users_list += f'<li><strong>{user.login}</strong> (статей: {user_articles_count}, id: {user.id})</li>'
        
        # Получаем список статей
        articles = Article.query.all()
        articles_list = ''
        for article in articles[:10]:  # Ограничиваем вывод 10 статьями
            articles_list += f'<li><strong>{article.title}</strong> (автор id: {article.user_id}, публичная: {article.is_public}, лайки: {article.likes})</li>'
        
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Статус БД</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1000px;
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
                }}
                h2 {{
                    color: #555;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }}
                .stats {{
                    display: flex;
                    justify-content: space-around;
                    margin: 30px 0;
                }}
                .stat-box {{
                    text-align: center;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    flex: 1;
                    margin: 0 10px;
                }}
                .stat-number {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                    margin: 10px 0;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 10px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .btn:hover {{
                    background: #5a67d8;
                }}
                .list-box {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                .list-box ul {{
                    list-style-type: none;
                    padding-left: 0;
                }}
                .list-box li {{
                    padding: 8px;
                    border-bottom: 1px solid #dee2e6;
                }}
                .list-box li:last-child {{
                    border-bottom: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Статус базы данных</h1>
                
                <div class="stats">
                    <div class="stat-box">
                        <div>Пользователи</div>
                        <div class="stat-number">{users_count}</div>
                    </div>
                    <div class="stat-box">
                        <div>Статьи</div>
                        <div class="stat-number">{articles_count}</div>
                    </div>
                </div>
                
                <div class="list-box">
                    <h2>Зарегистрированные пользователи:</h2>
                    {'<ul>' + users_list + '</ul>' if users_list else '<p>Пользователей нет</p>'}
                </div>
                
                <div class="list-box">
                    <h2>Последние статьи (первые 10):</h2>
                    {'<ul>' + articles_list + '</ul>' if articles_list else '<p>Статей нет</p>'}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/lab8/test-data/" class="btn">Создать тестовые данные</a>
                    <a href="/lab8/create-tables/" class="btn">Создать таблицы</a>
                    <a href="/lab8/" class="btn">На главную lab8</a>
                </div>
            </div>
        </body>
        </html>
        '''

@lab8.route('/create-tables/')
def create_tables():
    from app import app
    
    with app.app_context():
        db, User, Article = get_db()
        
        # Создаем таблицы если их нет
        User.__table__.create(bind=db.engine, checkfirst=True)
        Article.__table__.create(bind=db.engine, checkfirst=True)
        
        return '''
        <!doctype html>
        <html>
        <head>
            <title>Таблицы созданы</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .success {
                    color: #28a745;
                    font-size: 24px;
                }
                .btn {
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 20px 10px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
                .btn:hover {
                    background: #5a67d8;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✅ Таблицы созданы/проверены!</div>
                <p>Таблицы <strong>users</strong> и <strong>articles</strong> были успешно созданы или уже существовали.</p>
                
                <div style="margin: 30px 0;">
                    <a href="/lab8/check-db/" class="btn">Проверить БД</a>
                    <a href="/lab8/test-data/" class="btn">Создать тестовые данные</a>
                    <a href="/lab8/" class="btn">На главную lab8</a>
                </div>
                
                <p><small>При создании таблиц автоматически добавляются необходимые индексы и связи между таблицами.</small></p>
            </div>
        </body>
        </html>
        '''