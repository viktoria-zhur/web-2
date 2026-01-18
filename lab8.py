from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

# Функция для доступа к моделям и БД
def get_db_context():
    from app import db, User, Article
    return {'db': db, 'User': User, 'Article': Article}

@lab8.route('/')
def index():
    return render_template('lab8/index.html')

@lab8.route('/login/', methods=['GET', 'POST'])
def login():
    ctx = get_db_context()
    User = ctx['User']
    
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        flash('Логин и пароль не могут быть пустыми', 'error')
        return render_template('lab8/login.html')
    
    user = User.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        flash('Вы успешно вошли в систему!', 'success')
        return redirect(url_for('lab8.index'))
    else:
        flash('Неверный логин или пароль', 'error')
        return render_template('lab8/login.html')

@lab8.route('/register/', methods=['GET', 'POST'])
def register():
    ctx = get_db_context()
    db = ctx['db']
    User = ctx['User']
    
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        flash('Логин и пароль не могут быть пустыми', 'error')
        return render_template('lab8/register.html')
    
    existing_user = User.query.filter_by(login=login_form).first()
    if existing_user:
        flash('Пользователь с таким логином уже существует', 'error')
        return render_template('lab8/register.html')
    
    hashed_password = generate_password_hash(password_form)
    new_user = User(login=login_form, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    flash('Регистрация прошла успешно! Вы вошли в систему.', 'success')
    return redirect(url_for('lab8.index'))

@lab8.route('/articles/')
@login_required
def articles():
    ctx = get_db_context()
    Article = ctx['Article']
    
    user_articles = Article.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    ctx = get_db_context()
    db = ctx['db']
    Article = ctx['Article']
    
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        flash('Название и текст статьи не могут быть пустыми', 'error')
        return render_template('lab8/create_article.html')
    
    new_article = Article(
        user_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    flash('Статья успешно создана!', 'success')
    return redirect(url_for('lab8.articles'))

@lab8.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('lab8.index'))

@lab8.route('/init-db/')
def init_db():
    return '''
    <!doctype html>
    <html>
    <head><title>Инициализация</title></head>
    <body>
        <h1>База данных уже инициализирована!</h1>
        <p>Таблицы создаются автоматически при запуске приложения.</p>
        <p>Файл базы данных: lab8.db</p>
        <a href="/lab8/">На главную</a>
    </body>
    </html>
    '''

@lab8.route('/test-data/')
def test_data():
    ctx = get_db_context()
    db = ctx['db']
    User = ctx['User']
    Article = ctx['Article']
    
    # Создаем тестового пользователя
    test_user = User.query.filter_by(login='testuser').first()
    if not test_user:
        test_user = User(
            login='testuser',
            password=generate_password_hash('test123')
        )
        db.session.add(test_user)
        db.session.commit()
    
    # Создаем тестовые статьи
    test_articles = [
        {'title': 'Тестовая статья 1', 'text': 'Это первая тестовая статья.', 'public': True},
        {'title': 'Тестовая статья 2', 'text': 'Это вторая тестовая статья.', 'public': True},
    ]
    
    for article_data in test_articles:
        article = Article.query.filter_by(title=article_data['title']).first()
        if not article:
            new_article = Article(
                user_id=test_user.id,
                title=article_data['title'],
                article_text=article_data['text'],
                is_public=article_data['public'],
                is_favorite=False,
                likes=0
            )
            db.session.add(new_article)
    
    db.session.commit()
    
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Тестовые данные</title>
        <style>
            body { font-family: Arial; margin: 40px; text-align: center; }
            .success { color: green; font-size: 24px; }
            .btn { display: inline-block; padding: 10px 20px; margin: 10px; 
                   background: #667eea; color: white; text-decoration: none; 
                   border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="success">✅ Тестовые данные созданы!</div>
        <p>Логин: testuser</p>
        <p>Пароль: test123</p>
        <a href="/lab8/login/" class="btn">Войти</a>
        <a href="/lab8/" class="btn">На главную</a>
    </body>
    </html>
    '''