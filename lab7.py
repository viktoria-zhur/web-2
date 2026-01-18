from flask import Blueprint, jsonify, request

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "id": 1,
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.",
        "director": "Кристофер Нолан",
        "rating": 8.6
    },
    {
        "id": 2,
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кобб — талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим.",
        "director": "Кристофер Нолан",
        "rating": 8.8
    },
    {
        "id": 3,
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки.",
        "director": "Фрэнк Дарабонт",
        "rating": 9.3
    },
    {
        "id": 4,
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": "Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы Готэма от преступности.",
        "director": "Кристофер Нолан",
        "rating": 9.0
    }
]

@lab7.route('/')
def index():
    css_path = "/static/lab1/lab1.css"
    
    films_html = ''
    for film in films:
        films_html += f'''
        <div class="film-card">
            <div class="film-header">
                <h3>{film['title_ru']} ({film['title']})</h3>
                <span class="film-year">{film['year']}</span>
            </div>
            <div class="film-info">
                <p><strong>Режиссер:</strong> {film['director']}</p>
                <p><strong>Рейтинг:</strong> {film['rating']}/10</p>
                <p>{film['description'][:150]}...</p>
            </div>
            <div class="film-actions">
                <button onclick="viewFilm({film['id']})" class="btn-small">👁️ Просмотр</button>
                <button onclick="editFilm({film['id']})" class="btn-small">✏️ Редактировать</button>
                <button onclick="deleteFilm({film['id']})" class="btn-small btn-danger">🗑️ Удалить</button>
            </div>
        </div>
        '''
    
    return f'''<!doctype html>
<html>
<head>
    <title>Лабораторная 7</title>
    <link rel="stylesheet" href="{css_path}">
    <style>
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        .film-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .film-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: white; }}
        .film-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .film-header h3 {{ margin: 0; font-size: 1.2em; }}
        .film-year {{ background: #667eea; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.9em; }}
        .film-info p {{ margin: 5px 0; color: #666; font-size: 0.9em; }}
        .film-actions {{ display: flex; gap: 5px; margin-top: 10px; }}
        .btn-small {{ padding: 5px 10px; font-size: 0.8em; border: none; border-radius: 3px; cursor: pointer; }}
        .btn-danger {{ background: #e74c3c; color: white; }}
        .api-panel {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .api-methods {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }}
        .method-card {{ background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #667eea; }}
        pre {{ background: #333; color: #fff; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 8px; box-sizing: border-box; }}
    </style>
    <script>
        async function loadFilms() {{
            try {{
                const response = await fetch('/lab7/api/films/');
                const films = await response.json();
                updateFilmsList(films);
            }} catch (error) {{
                alert('Ошибка загрузки фильмов: ' + error);
            }}
        }}
        
        function updateFilmsList(films) {{
            const container = document.getElementById('filmsContainer');
            if (!container) return;
            
            let html = '';
            films.forEach(film => {{
                html += `
                <div class="film-card">
                    <div class="film-header">
                        <h3>${{film.title_ru}} (${{film.title}})</h3>
                        <span class="film-year">${{film.year}}</span>
                    </div>
                    <div class="film-info">
                        <p><strong>ID:</strong> ${{film.id}}</p>
                        <p>${{film.description.substring(0, 150)}}...</p>
                    </div>
                    <div class="film-actions">
                        <button onclick="viewFilm(${{film.id}})" class="btn-small">👁️ Просмотр</button>
                        <button onclick="editFilm(${{film.id}})" class="btn-small">✏️ Редактировать</button>
                        <button onclick="deleteFilm(${{film.id}})" class="btn-small btn-danger">🗑️ Удалить</button>
                    </div>
                </div>
                `;
            }});
            
            container.innerHTML = html || '<p>Нет фильмов</p>';
            document.getElementById('filmsCount').textContent = films.length;
        }}
        
        async function viewFilm(id) {{
            try {{
                const response = await fetch(`/lab7/api/films/${{id}}`);
                const film = await response.json();
                
                alert(`Фильм #${{film.id}}\\nНазвание: ${{film.title_ru}} (${{film.title}})\\nГод: ${{film.year}}\\nОписание: ${{film.description}}`);
            }} catch (error) {{
                alert('Ошибка загрузки фильма: ' + error);
            }}
        }}
        
        async function deleteFilm(id) {{
            if (!confirm('Удалить фильм?')) return;
            
            try {{
                const response = await fetch(`/lab7/api/films/${{id}}`, {{
                    method: 'DELETE'
                }});
                
                if (response.ok) {{
                    alert('Фильм удален!');
                    loadFilms();
                }} else {{
                    alert('Ошибка удаления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        function showAddForm() {{
            const form = `
            <div id="addForm" style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #667eea;">
                <h3>➕ Добавить новый фильм</h3>
                <form onsubmit="addFilm(event)">
                    <div class="form-group">
                        <label for="title">Английское название:</label>
                        <input type="text" id="title" name="title" required>
                    </div>
                    <div class="form-group">
                        <label for="title_ru">Русское название:</label>
                        <input type="text" id="title_ru" name="title_ru" required>
                    </div>
                    <div class="form-group">
                        <label for="year">Год:</label>
                        <input type="number" id="year" name="year" min="1900" max="2024" required>
                    </div>
                    <div class="form-group">
                        <label for="director">Режиссер:</label>
                        <input type="text" id="director" name="director" required>
                    </div>
                    <div class="form-group">
                        <label for="rating">Рейтинг:</label>
                        <input type="number" id="rating" name="rating" min="0" max="10" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Описание:</label>
                        <textarea id="description" name="description" rows="4" required></textarea>
                    </div>
                    <div>
                        <button type="submit" class="btn">💾 Сохранить</button>
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
        
        async function addFilm(event) {{
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const film = {{
                title: formData.get('title'),
                title_ru: formData.get('title_ru'),
                year: parseInt(formData.get('year')),
                director: formData.get('director'),
                rating: parseFloat(formData.get('rating')),
                description: formData.get('description')
            }};
            
            try {{
                const response = await fetch('/lab7/api/films/', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(film)
                }});
                
                if (response.ok) {{
                    alert('Фильм добавлен!');
                    hideAddForm();
                    loadFilms();
                }} else {{
                    alert('Ошибка добавления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        async function editFilm(id) {{
            try {{
                const response = await fetch(`/lab7/api/films/${{id}}`);
                const film = await response.json();
                
                const form = `
                <div id="editForm" style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #f39c12;">
                    <h3>✏️ Редактировать фильм #${{film.id}}</h3>
                    <form onsubmit="updateFilm(event, ${{film.id}})">
                        <div class="form-group">
                            <label for="edit_title">Английское название:</label>
                            <input type="text" id="edit_title" name="title" value="${{film.title}}" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_title_ru">Русское название:</label>
                            <input type="text" id="edit_title_ru" name="title_ru" value="${{film.title_ru}}" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_year">Год:</label>
                            <input type="number" id="edit_year" name="year" value="${{film.year}}" min="1900" max="2024" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_director">Режиссер:</label>
                            <input type="text" id="edit_director" name="director" value="${{film.director}}" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_rating">Рейтинг:</label>
                            <input type="number" id="edit_rating" name="rating" value="${{film.rating}}" min="0" max="10" step="0.1" required>
                        </div>
                        <div class="form-group">
                            <label for="edit_description">Описание:</label>
                            <textarea id="edit_description" name="description" rows="4" required>${{film.description}}</textarea>
                        </div>
                        <div>
                            <button type="submit" class="btn">💾 Сохранить изменения</button>
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
        
        async function updateFilm(event, id) {{
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const film = {{
                title: formData.get('title'),
                title_ru: formData.get('title_ru'),
                year: parseInt(formData.get('year')),
                director: formData.get('director'),
                rating: parseFloat(formData.get('rating')),
                description: formData.get('description')
            }};
            
            try {{
                const response = await fetch(`/lab7/api/films/${{id}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(film)
                }});
                
                if (response.ok) {{
                    const updatedFilm = await response.json();
                    alert('Фильм обновлен!');
                    hideEditForm();
                    loadFilms();
                }} else {{
                    alert('Ошибка обновления фильма');
                }}
            }} catch (error) {{
                alert('Ошибка: ' + error);
            }}
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            loadFilms();
        }});
    </script>
</head>
<body>
    <div class="container">
        <h1>🎬 Лабораторная работа 7</h1>
        <p>REST API для управления фильмами (CRUD операции)</p>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
            <h2>📊 Статистика</h2>
            <div style="font-size: 3em; font-weight: bold;" id="filmsCount">{len(films)}</div>
            <p>фильмов в базе</p>
        </div>
        
        <div class="btn-group" style="margin: 20px 0;">
            <button onclick="showAddForm()" class="btn" style="padding: 10px 20px; background: #2ecc71; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">➕ Добавить фильм</button>
            <button onclick="loadFilms()" class="btn" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">🔄 Обновить список</button>
            <a href="/" class="btn" style="padding: 10px 20px; background: #95a5a6; color: white; text-decoration: none; border-radius: 5px; font-size: 1em;">🏠 На главную</a>
        </div>
        
        <div id="addFormContainer"></div>
        <div id="editFormContainer"></div>
        
        <h2>🎥 Список фильмов</h2>
        <div id="filmsContainer" class="film-grid">
            {films_html}
        </div>
        
        <div class="api-panel">
            <h2>📡 REST API</h2>
            <p>Доступные endpoints для работы с фильмами:</p>
            
            <div class="api-methods">
                <div class="method-card">
                    <h4>GET /api/films/</h4>
                    <p>Получить список всех фильмов</p>
                </div>
                <div class="method-card">
                    <h4>GET /api/films/{'{id}'}</h4>
                    <p>Получить фильм по ID</p>
                </div>
                <div class="method-card">
                    <h4>POST /api/films/</h4>
                    <p>Добавить новый фильм</p>
                </div>
                <div class="method-card">
                    <h4>PUT /api/films/{'{id}'}</h4>
                    <p>Обновить фильм по ID</p>
                </div>
                <div class="method-card">
                    <h4>DELETE /api/films/{'{id}'}</h4>
                    <p>Удалить фильм по ID</p>
                </div>
            </div>
            
            <h3>Пример запроса POST:</h3>
            <pre>
{{
    "title": "New Film",
    "title_ru": "Новый фильм",
    "year": 2024,
    "director": "Режиссер",
    "rating": 8.5,
    "description": "Описание фильма"
}}</pre>
            
            <h3>Тестирование API:</h3>
            <div style="margin: 15px 0;">
                <button onclick="fetch('/lab7/api/films/').then(r => r.json()).then(data => alert(JSON.stringify(data, null, 2)))" class="btn-small">📋 Получить все фильмы</button>
                <button onclick="fetch('/lab7/api/films/1').then(r => r.json()).then(data => alert(JSON.stringify(data, null, 2)))" class="btn-small">🔍 Получить фильм #1</button>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🎬 База данных фильмов с полным CRUD функционалом</p>
            <p>Журавлева Виктория Александровна, ФБИ-34</p>
        </div>
    </div>
</body>
</html>'''

@lab7.route('/api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/api/films/<int:id>', methods=['GET'])
def get_film(id):
    film = next((f for f in films if f['id'] == id), None)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(film)

@lab7.route('/api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    global films
    film = next((f for f in films if f['id'] == id), None)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    
    films = [f for f in films if f['id'] != id]
    return '', 204

@lab7.route('/api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = next((f for f in films if f['id'] == id), None)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных"}), 400
    
    # Обновляем фильм
    index = next(i for i, f in enumerate(films) if f['id'] == id)
    films[index] = {**films[index], **data, 'id': id}
    
    return jsonify(films[index])

@lab7.route('/api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных"}), 400
    
    # Генерируем новый ID
    new_id = max([f['id'] for f in films], default=0) + 1
    new_film = {
        'id': new_id,
        'title': data.get('title', ''),
        'title_ru': data.get('title_ru', ''),
        'year': data.get('year', 2024),
        'director': data.get('director', ''),
        'rating': data.get('rating', 0),
        'description': data.get('description', '')
    }
    
    films.append(new_film)
    return jsonify({"id": new_id}), 201