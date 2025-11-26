from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

# Сначала определяем Blueprint
lab5 = Blueprint('lab5', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='viktoria_zhuravleva_knowledge_base',
        user='viktoria_zhuravleva_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5')
def main():
    username = session.get('username', 'Anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните все поля")
    
    try:
        conn, cur = db_connect()

        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if not check_password_hash(user['password_hash'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['username'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    print("🎯 Функция register() вызвана")
    
    if request.method == 'GET':
        print("📝 GET запрос - показываем форму")
        return render_template('lab5/register.html')
    
    print("📨 POST запрос - обрабатываем данные")
    login = request.form.get('login')
    password = request.form.get('password')

    print(f"🔍 ДАННЫЕ ИЗ ФОРМЫ: login='{login}', password='{password}'")
    print(f"🔍 ВСЕ ДАННЫЕ ФОРМЫ: {dict(request.form)}")

    if not (login and password):
        print("❌ Ошибка: не заполнены все поля")
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        print("🔄 Попытка подключения к БД...")
        conn, cur = db_connect()
        print("✅ Подключение к БД установлено")

        print(f"🔍 Проверяем существующего пользователя: '{login}'")
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        existing_user = cur.fetchone()
        print(f"🔍 Результат проверки: {existing_user}")
        
        if existing_user:
            db_close(conn, cur)
            print("❌ Пользователь уже существует")
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        print("🔐 Генерируем хеш пароля...")
        password_hash = generate_password_hash(password)
        print(f"🔐 Сгенерирован хеш: {password_hash}")
        
        print(f"🚀 Выполняем INSERT в БД...")
        cur.execute("INSERT INTO users (login, password_hash) VALUES (%s, %s);", (login, password_hash))
        print("✅ INSERT выполнен")
        
        db_close(conn, cur)
        print("✅ Пользователь успешно добавлен в БД")
        
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        print(f"💥 ТРАССИРОВКА: {traceback.format_exc()}")
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    return "список статей"

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    login = session.get('username')  # Исправлено: используем 'username' из сессии
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')  

    if not (title and article_text):
        return render_template('lab5/create_article.html', error="Заполните все поля")

    try:
        conn, cur = db_connect()

        # Исправленный запрос
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error="Пользователь не найден")

        user_id = user["id"]

        # Исправленный запрос - используем параметризованный запрос
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                   (user_id, title, article_text))

        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')