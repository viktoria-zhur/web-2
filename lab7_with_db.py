from flask import Blueprint, jsonify, request
from datetime import datetime
import sqlite3
from os import path

lab7_db = Blueprint('lab7_db', __name__)

# Путь к базе данных
DB_PATH = path.join(path.dirname(__file__), 'lab7.db')

def init_db():
    """Инициализация базы данных фильмов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_title TEXT,
            russian_title TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Добавляем тестовые данные если таблица пуста
    cursor.execute('SELECT COUNT(*) as count FROM movies')
    count = cursor.fetchone()[0]
    
    if count == 0:
        test_movies = [
            ('Interstellar', 'Интерстеллар', 2014, 'Фантастический фильм о путешествии через червоточину для спасения человечества.'),
            ('Inception', 'Начало', 2010, 'Фильм о технологии внедрения в сны и краже идей.'),
            ('The Matrix', 'Матрица', 1999, 'Киберпанк-фильм о виртуальной реальности, контролирующей человечество.')
        ]
        
        for original, russian, year, desc in test_movies:
            cursor.execute(
                'INSERT INTO movies (original_title, russian_title, year, description) VALUES (?, ?, ?, ?)',
                (original, russian, year, desc)
            )
    
    conn.commit()
    conn.close()

# Инициализируем базу данных при импорте
init_db()

def get_db_connection():
    """Подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def movie_to_dict(row):
    """Преобразование строки из БД в словарь"""
    return {
        "id": row['id'],
        "title": row['original_title'] or row['russian_title'],
        "title_ru": row['russian_title'],
        "year": row['year'],
        "description": row['description'],
        "created_at": row['created_at']
    }

@lab7_db.route('/')
def index():
    css_path = "/static/lab1/lab1.css"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM movies')
    films_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT * FROM movies ORDER BY created_at DESC')
    movies = cursor.fetchall()
    conn.close()
    
    movies_html = ''
    for movie in movies:
        movie_dict = movie_to_dict(movie)
        movies_html += f'''
        <div class="movie-card">
            <div class="movie-header">
                <h3>{movie_dict['title_ru']} ({movie_dict['title']})</h3>
                <span class="movie-year">{movie_dict['year']}</span>
            </div>
            <div class="movie-info">
                <p><strong>ID:</strong> {movie_dict['id']}</p>
                <p><strong>Описание:</strong> {movie_dict['description'][:100]}...</p>
                <p><strong>Добавлен:</strong> {movie_dict['created_at']}</p>
            </div>
            <div class="movie-actions">
                <button onclick="viewMovie({movie_dict['id']})" class="btn-small">👁️ Просмотр</button>
                <button onclick="editMovie({movie_dict['id']})" class="btn-small">✏️ Редактировать</button>
                <button onclick="deleteMovie({movie_dict['id']})" class="btn-small btn-danger">🗑️ Удалить</button>
            </div>
        </div>
        '''
    
    return f'''<!doctype html>
<html>
<head>
    <title>База данных фильмов</title>
    <link rel="stylesheet" href="{css_path}">
    <style>
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        .movie-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .movie-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: white; }}
        .movie-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .movie-header h3 {{ margin: 0; font-size: 1.2em; }}
        .movie-year {{ background: #667eea; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.9em; }}
        .movie-info p {{ margin: 5px 0; color: #666; font-size: 0.9em; }}
        .movie-actions {{ display: flex; gap: 5px; margin-top: 10px; }}
        .btn-small {{ padding: 5px 10px; font-size: 0.8em; border: none; border-radius: 3px; cursor: pointer; }}
        .btn-danger {{ background: #e74c3c; color: white; }}
        .stats {{ background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }}
        .stat-number {{ font-size: 3em; font-weight: bold; }}
        .api-info {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        pre {{ background: #333; color: #fff; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 8px; box-sizing: border-box; }}
    </style>
    <script>
        async function loadMovies() {{
            try {{
                const response = await fetch('/lab7-db/api/films/');
                const movies = await response.json();
                updateMoviesList(movies);
            }} catch (error) {{
                alert('Ошибка загрузки фильмов: ' + error);
            }}
        }}
        
        function updateMoviesList(movies) {{
            const container = document.getElementById('moviesContainer');
            if (!container) return;
            
            let html = '';
            movies.forEach(movie => {{
                html += `
                <div class="movie-card">
                    <div class="movie-header">
                        <h3>${{movie.title_ru}} (${{movie.title}})</h3>
                        <span class="movie-year">${{movie.year}}</span>
                    </div>
                    <div class="movie-info">
                        <p><strong>ID:</strong> ${{movie.id}}</p>
                        <p>${{movie.description.substring(0, 100)}}...</p>
                    </div>
                    <div class="movie-actions">
                        <button onclick="viewMovie(${{movie.id}})" class="btn-small">👁️ Просмотр</button>
                        <button onclick="editMovie(${{movie.id}})" class="btn-small">✏️ Редактировать</button>
                        <button onclick="deleteMovie(${{movie.id}})" class="btn-small btn-danger">🗑️ Удалить</button>
                    </div>
                </div>
                `;
            }});
            
            container.innerHTML = html || '<p>Нет фильмов в базе данных</p>';
            document.getElementById('moviesCount').textContent = movies.length;
        }}
        
        async function viewMovie(id) {{
            try {{
                const response = await fetch(`/lab7-db/api/films/${{id}}`);
                const movie = await response.json();
                
                alert(`Фильм #${{movie.id}}\\nНазвание: ${{movie.title_ru}} (${{movie.title}})\\nГод: ${{movie.year}}\\nОписание: ${{movie.description}}`);
            }} catch (error) {{
                alert('Ошибка загрузки фильма: ' + error);
            }}
        }}
        
        async function deleteMovie(id) {{
            if (!confirm('Удалить фильм из базы данных?')) return;
            
            try {{
                const response = await fetch(`/lab7-db/api/films/${{id}}`, {{
                    method: 'DELETE'
                }});
                
                if (response.ok) {{
                    alert('Фильм удален из базы данных!');
                    loadMovies();
                }} else {{
                    alert('Ошибка удаления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        function showAddForm() {{
            const form = `
            <div id="addForm" style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #2ecc71;">
                <h3>➕ Добавить новый фильм в БД</h3>
                <form onsubmit="addMovie(event)">
                    <div class="form-group">
                        <label for="title">Оригинальное название:</label>
                        <input type="text" id="title" name="title" placeholder="На английском">
                    </div>
                    <div class="form-group">
                        <label for="title_ru">Русское название:</label>
                        <input type="text" id="title_ru" name="title_ru" required placeholder="На русском">
                    </div>
                    <div class="form-group">
                        <label for="year">Год выхода:</label>
                        <input type="number" id="year" name="year" min="1900" max="2024" required value="2024">
                    </div>
                    <div class="form-group">
                        <label for="description">Описание:</label>
                        <textarea id="description" name="description" rows="4" required placeholder="Описание фильма"></textarea>
                    </div>
                    <div>
                        <button type="submit" class="btn" style="background: #2ecc71;">💾 Сохранить в БД</button>
                        <button type="button" onclick="hideAddForm()" class="btn btn-danger">❌ Отмена</button>
                    </div>
                </form>
            </div>
            `;
            
            document.getElementById('addFormContainer').innerHTML = form;
        }}
        
        function hideAddForm() {{
            document.getElementById('addFormContainer').innerHTML = '';
        }}
        
        async function addMovie(event) {{
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const movie = {{
                title: formData.get('title'),
                title_ru: formData.get('title_ru'),
                year: parseInt(formData.get('year')),
                description: formData.get('description')
            }};
            
            try {{
                const response = await fetch('/lab7-db/api/films/', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(movie)
                }});
                
                if (response.status === 201) {{
                    const result = await response.json();
                    alert(`Фильм добавлен в базу данных! ID: ${{result.id}}`);
                    hideAddForm();
                    loadMovies();
                }} else {{
                    alert('Ошибка добавления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        async function editMovie(id) {{
            try {{
                const response = await fetch(`/lab7-db/api/films/${{id}}`);
                const movie = await response.json();
                
                const form = `
                <div id="editForm" style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #f39c12;">
                    <h3>✏️ Редактировать фильм #${{movie.id}}</h3>
                    <form onsubmit="updateMovie(event, ${{movie.id}})">
                        <div class="form-group">
                            <label for="edit_title">Оригинальное название:</label>
                            <input type="text" id="edit_title" name="title" value="${{movie.title}}" placeholder="На английском">
                        </div>
                        <div class="form-group">
                            <label for="edit_title_ru">Русское название:</label>
                            <input type="text" id="edit_title_ru" name="title_ru" value="${{movie.title_ru}}" required placeholder="На русском">
                        </div>
                        <div class="form-group">
                            <label for="edit_year">Год выхода:</label>
                            <input type="number" id="edit_year" name="year" value="${{movie.year}}" min="1900" max="2024" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_description">Описание:</label>
                            <textarea id="edit_description" name="description" rows="4" required>${{movie.description}}</textarea>
                        </div>
                        <div>
                            <button type="submit" class="btn" style="background: #f39c12;">💾 Обновить в БД</button>
                            <button type="button" onclick="hideEditForm()" class="btn btn-danger">❌ Отмена</button>
                        </div>
                    </form>
                </div>
                `;
                
                document.getElementById('editFormContainer').innerHTML = form;
            }} catch (error) {{
                alert('Ошибка загрузки фильма: ' + error);
            }}
        }}
        
        function hideEditForm() {{
            document.getElementById('editFormContainer').innerHTML = '';
        }}
        
        async function updateMovie(event, id) {{
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const movie = {{
                title: formData.get('title'),
                title_ru: formData.get('title_ru'),
                year: parseInt(formData.get('year')),
                description: formData.get('description')
            }};
            
            try {{
                const response = await fetch(`/lab7-db/api/films/${{id}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(movie)
                }});
                
                if (response.ok) {{
                    const updatedMovie = await response.json();
                    alert('Фильм обновлен в базе данных!');
                    hideEditForm();
                    loadMovies();
                }} else {{
                    alert('Ошибка обновления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        function initDatabase() {{
            if (confirm('Пересоздать базу данных с тестовыми фильмами?')) {{
                fetch('/lab7-db/init-db')
                    .then(() => {{
                        alert('База данных инициализирована!');
                        loadMovies();
                    }})
                    .catch(error => alert('Ошибка: ' + error));
            }}
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            loadMovies();
        }});
    </script>
</head>
<body>
    <div class="container">
        <h1>🎬 База данных фильмов (SQLAlchemy)</h1>
        <p>Дополнительное задание к лабораторной работе 7 - работа с SQLAlchemy ORM</p>
        
        <div class="stats">
            <div class="stat-number" id="moviesCount">{films_count}</div>
            <p>фильмов в базе данных</p>
        </div>
        
        <div class="btn-group" style="margin: 20px 0;">
            <button onclick="showAddForm()" class="btn" style="padding: 10px 20px; background: #2ecc71; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">➕ Добавить фильм</button>
            <button onclick="loadMovies()" class="btn" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">🔄 Обновить список</button>
            <button onclick="initDatabase()" class="btn" style="padding: 10px 20px; background: #9b59b6; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">🗃️ Инициализировать БД</button>
            <a href="/lab7" class="btn" style="padding: 10px 20px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; font-size: 1em;">🎬 К обычной версии</a>
            <a href="/" class="btn" style="padding: 10px 20px; background: #95a5a6; color: white; text-decoration: none; border-radius: 5px; font-size: 1em;">🏠 На главную</a>
        </div>
        
        <div id="addFormContainer"></div>
        <div id="editFormContainer"></div>
        
        <h2>📋 Фильмы в базе данных</h2>
        <div id="moviesContainer" class="movie-grid">
            {movies_html}
        </div>
        
        <div class="api-info">
            <h2>📡 REST API с SQLAlchemy</h2>
            <p>Полноценное REST API для работы с базой данных фильмов через SQLAlchemy ORM</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db;">
                    <h4>GET /api/films/</h4>
                    <p>Получить все фильмы из БД</p>
                </div>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #2ecc71;">
                    <h4>GET /api/films/{'{id}'}</h4>
                    <p>Получить фильм по ID</p>
                </div>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #f39c12;">
                    <h4>POST /api/films/</h4>
                    <p>Добавить фильм в БД</p>
                </div>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #9b59b6;">
                    <h4>PUT /api/films/{'{id}'}</h4>
                    <p>Обновить фильм в БД</p>
                </div>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #e74c3c;">
                    <h4>DELETE /api/films/{'{id}'}</h4>
                    <p>Удалить фильм из БД</p>
                </div>
            </div>
            
            <h3>Пример добавления фильма:</h3>
            <pre>
{{
    "title": "The Godfather",
    "title_ru": "Крестный отец",
    "year": 1972,
    "description": "Эпическая история семьи мафиози Корлеоне."
}}</pre>
            
            <h3>Тестирование API:</h3>
            <div style="margin: 15px 0;">
                <button onclick="fetch('/lab7-db/api/films/').then(r => r.json()).then(data => console.log(data) || alert('Фильмы загружены (см. консоль)'))" class="btn-small">📋 Получить все фильмы</button>
                <button onclick="fetch('/lab7-db/api/films/1').then(r => r.json()).then(data => alert(JSON.stringify(data, null, 2)))" class="btn-small">🔍 Получить фильм #1</button>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🎬 База данных на SQLite с SQLAlchemy ORM</p>
            <p>Журавлева Виктория Александровна, ФБИ-34</p>
        </div>
    </div>
</body>
</html>'''

@lab7_db.route('/init-db')
def init_db_route():
    """Пересоздание базы данных с тестовыми данными"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS movies')
    cursor.execute('''
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_title TEXT,
            russian_title TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    test_movies = [
        ('Interstellar', 'Интерстеллар', 2014, 'Фантастический фильм о путешествии через червоточину для спасения человечества.'),
        ('Inception', 'Начало', 2010, 'Фильм о технологии внедрения в сны и краже идей.'),
        ('The Matrix', 'Матрица', 1999, 'Киберпанк-фильм о виртуальной реальности, контролирующей человечество.'),
        ('The Shawshank Redemption', 'Побег из Шоушенка', 1994, 'Драма о жизни в тюрьме и надежде.'),
        ('The Dark Knight', 'Тёмный рыцарь', 2008, 'Супергеройский фильм о Бэтмене и Джокере.')
    ]
    
    for original, russian, year, desc in test_movies:
        cursor.execute(
            'INSERT INTO movies (original_title, russian_title, year, description) VALUES (?, ?, ?, ?)',
            (original, russian, year, desc)
        )
    
    conn.commit()
    conn.close()
    
    return '''<!doctype html>
<html>
<head>
    <title>База данных инициализирована</title>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
</head>
<body>
    <div class="container">
        <h1>✅ База данных инициализирована!</h1>
        <p>Создано 5 тестовых фильмов.</p>
        <div style="margin-top: 20px;">
            <a href="/lab7-db/" class="btn">🎬 Вернуться к фильмам</a>
        </div>
    </div>
</body>
</html>'''

@lab7_db.route('/api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies ORDER BY created_at DESC')
    movies = cursor.fetchall()
    conn.close()
    
    return jsonify([movie_to_dict(movie) for movie in movies])

@lab7_db.route('/api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    movie = cursor.fetchone()
    conn.close()
    
    if not movie:
        return jsonify({"error": "Фильм не найден"}), 404
    
    return jsonify(movie_to_dict(movie))

@lab7_db.route('/api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    if not data or 'title_ru' not in data or 'year' not in data or 'description' not in data:
        return jsonify({"error": "Недостаточно данных"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO movies (original_title, russian_title, year, description) VALUES (?, ?, ?, ?)',
        (data.get('title'), data['title_ru'], data['year'], data['description'])
    )
    
    movie_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    
    return jsonify({"id": movie_id}), 201

@lab7_db.route('/api/films/<int:id>', methods=['PUT'])
def update_film(id):
    data = request.get_json()
    
    if not data or 'title_ru' not in data or 'year' not in data or 'description' not in data:
        return jsonify({"error": "Недостаточно данных"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Фильм не найден"}), 404
    
    cursor.execute(
        'UPDATE movies SET original_title = ?, russian_title = ?, year = ?, description = ? WHERE id = ?',
        (data.get('title'), data['title_ru'], data['year'], data['description'], id)
    )
    
    conn.commit()
    
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    movie = cursor.fetchone()
    conn.close()
    
    return jsonify(movie_to_dict(movie))

@lab7_db.route('/api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Фильм не найден"}), 404
    
    cursor.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return '', 204