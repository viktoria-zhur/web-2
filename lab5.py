from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
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
        # Для PostgreSQL используем %s
        formatted_query = query.replace('?', '%s')
    else:
        # Для SQLite используем ?
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
        return render_template('lab5/success_login.html', login=username_input)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    username_input = request.form.get('login')
    password = request.form.get('password')

    if not (username_input and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        execute_query(cur, "SELECT login FROM users WHERE login = ?;", (username_input,))
        existing_user = cur.fetchone()
        
        if existing_user:
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        
        execute_query(cur, "INSERT INTO users (login, password) VALUES (?, ?);", (username_input, password))
        
        # АВТОМАТИЧЕСКАЯ АВТОРИЗАЦИЯ ПОСЛЕ РЕГИСТРАЦИИ
        session['username'] = username_input
        
        db_close(conn, cur)
        return redirect('/lab5')  # Перенаправляем в главное меню лаб. работы 5
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    execute_query(cur, "SELECT id FROM users WHERE login = ?;", (username,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']

    execute_query(cur, "SELECT * FROM articles WHERE user_id = ?;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    username = session.get('username')
    if not username:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error="Заполните все поля")

    try:
        conn, cur = db_connect()

        execute_query(cur, "SELECT id FROM users WHERE login = ?;", (username,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error="Пользователь не найден")

        user_id = user["id"]

        execute_query(cur, "INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", 
                   (user_id, title, article_text))

        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')   
@lab5.route('/lab5/logout')
def logout():
    session.pop('username', None)
    return redirect('/lab5')