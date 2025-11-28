from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopopg2.connect(
            host='127.0.0.1',
            database='viktoria_zhuravleva_knowledge_base',
            user='viktoria_zhuravleva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "knowledge_base.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def execute_query(cur, query, params):
    """Универсальная функция для выполнения запросов с правильными параметрами"""
    if current_app.config.get('DB_TYPE') == 'postgres':
        formatted_query = query.replace('?', '%s')
    else:
        formatted_query = query.replace('%s', '?')
    
    cur.execute(formatted_query, params)

@lab5.route('/lab5')
def main():
    username = session.get('username', 'Anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    username_input = request.form.get('login')
    password = request.form.get('password')

    if not (username_input and password):
        return render_template('lab5/login.html', error="Заполните все поля")
    
    try:
        conn, cur = db_connect()

        execute_query(cur, "SELECT * FROM users WHERE login = ?;", (username_input,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['username'] = username_input
        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    username_input = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')

    if not (username_input and password):
        return render_template('lab5/register.html', error='Заполните логин и пароль')

    try:
        conn, cur = db_connect()

        execute_query(cur, "SELECT login FROM users WHERE login = ?;", (username_input,))
        existing_user = cur.fetchone()
        
        if existing_user:
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        
        execute_query(cur, "INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                     (username_input, password_hash, real_name))
        
        session['username'] = username_input
        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    username = session.get('username')
    
    conn, cur = db_connect()

    if username and username != 'Anonymous':
        # Для авторизованных пользователей - их статьи + публичные статьи других
        execute_query(cur, "SELECT id FROM users WHERE login = ?;", (username,))
        user = cur.fetchone()
        
        if user:
            user_id = user['id']
            # Сначала любимые статьи, затем остальные, сначала свои, затем публичные других
            execute_query(cur, """
                SELECT a.*, u.login as author_login 
                FROM articles a 
                JOIN users u ON a.login_id = u.id 
                WHERE a.login_id = ? OR a.is_public = 1 
                ORDER BY a.is_favorite DESC, a.login_id = ? DESC, a.created_at DESC
            """, (user_id, user_id))
        else:
            execute_query(cur, "SELECT a.*, u.login as author_login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.is_public = 1 ORDER BY a.created_at DESC;", ())
    else:
        # Для неавторизованных - только публичные статьи
        execute_query(cur, "SELECT a.*, u.login as author_login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.is_public = 1 ORDER BY a.created_at DESC;", ())

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, username=username)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 1 if request.form.get('is_favorite') else 0
    is_public = 1 if request.form.get('is_public') else 0

    if not (title and article_text):
        return render_template('lab5/create_article.html', error="Заполните заголовок и текст")

    try:
        conn, cur = db_connect()

        execute_query(cur, "SELECT id FROM users WHERE login = ?;", (username,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error="Пользователь не найден")

        user_id = user["id"]

        execute_query(cur, "INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
                   (user_id, title, article_text, is_favorite, is_public))

        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    execute_query(cur, "SELECT a.* FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id = ? AND u.login = ?;", 
                 (article_id, username))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для редактирования", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 1 if request.form.get('is_favorite') else 0
    is_public = 1 if request.form.get('is_public') else 0

    if not (title and article_text):
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Заполните все поля")

    try:
        execute_query(cur, "UPDATE articles SET title = ?, article_text = ?, is_favorite = ?, is_public = ? WHERE id = ?;", 
                     (title, article_text, is_favorite, is_public, article_id))
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    execute_query(cur, "SELECT a.* FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id = ? AND u.login = ?;", 
                 (article_id, username))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для удаления", 404

    try:
        execute_query(cur, "DELETE FROM articles WHERE id = ?;", (article_id,))
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        db_close(conn, cur)
        return f'Ошибка базы данных: {str(e)}', 500

@lab5.route('/lab5/users')
def list_users():
    """Страница со списком всех пользователей"""
    conn, cur = db_connect()
    execute_query(cur, "SELECT login, real_name FROM users ORDER BY login;", ())
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def edit_profile():
    """Страница изменения имени и пароля"""
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')

    if request.method == 'GET':
        conn, cur = db_connect()
        execute_query(cur, "SELECT login, real_name FROM users WHERE login = ?;", (username,))
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    # Обработка формы
    real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    try:
        conn, cur = db_connect()

        # Получаем текущего пользователя
        execute_query(cur, "SELECT * FROM users WHERE login = ?;", (username,))
        user = cur.fetchone()

        # Проверяем текущий пароль если меняется пароль
        if new_password:
            if not current_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Введите текущий пароль")
            
            if not check_password_hash(user['password'], current_password):
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Неверный текущий пароль")
            
            if new_password != confirm_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Новый пароль и подтверждение не совпадают")
            
            # Хешируем новый пароль
            new_password_hash = generate_password_hash(new_password)
            execute_query(cur, "UPDATE users SET real_name = ?, password = ? WHERE login = ?;", 
                         (real_name, new_password_hash, username))
        else:
            # Меняем только имя
            execute_query(cur, "UPDATE users SET real_name = ? WHERE login = ?;", 
                         (real_name, username))

        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/logout')
def logout():
    session.pop('username', None)
    return redirect('/lab5')