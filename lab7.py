from flask import Blueprint, render_template, jsonify, request

lab7 = Blueprint('lab7', __name__)

# Список фильмов
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    }
]

@lab7.route('/')
def main():
    return render_template('lab7/index.html', films_count=len(films))

# Получение всех фильмов
@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получение одного фильма по ID
@lab7.route('/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(films[id])

# Удаление фильма по ID
@lab7.route('/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    films.pop(id)
    return '', 204

# Редактирование существующего фильма
@lab7.route('/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    
    new_film_data = request.get_json()
    
    # ЗАДАНИЕ 2: Если оригинальное название пустое, а русское задано
    if not new_film_data.get('title') or not new_film_data['title'].strip():
        if new_film_data.get('title_ru') and new_film_data['title_ru'].strip():
            new_film_data['title'] = new_film_data['title_ru']
    
    # ВАЛИДАЦИЯ
    errors = []
    
    if not new_film_data.get('title_ru') or not new_film_data['title_ru'].strip():
        errors.append({"field": "title_ru", "message": "Русское название обязательно"})
    
    if not new_film_data.get('year'):
        errors.append({"field": "year", "message": "Год обязателен"})
    elif not isinstance(new_film_data['year'], int) or new_film_data['year'] < 1895 or new_film_data['year'] > 2025:
        errors.append({"field": "year", "message": "Год должен быть в диапазоне 1895-2025"})
    
    if not new_film_data.get('description') or not new_film_data['description'].strip():
        errors.append({"field": "description", "message": "Описание обязательно"})
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    films[id] = new_film_data
    return jsonify(films[id])

# Добавление нового фильма
@lab7.route('/rest-api/films/', methods=['POST'])
def add_film():
    new_film_data = request.get_json()
    
    # ЗАДАНИЕ 2: Если оригинальное название пустое, а русское задано
    if not new_film_data.get('title') or not new_film_data['title'].strip():
        if new_film_data.get('title_ru') and new_film_data['title_ru'].strip():
            new_film_data['title'] = new_film_data['title_ru']
    
    # ВАЛИДАЦИЯ
    errors = []
    
    if not new_film_data.get('title_ru') or not new_film_data['title_ru'].strip():
        errors.append({"field": "title_ru", "message": "Русское название обязательно"})
    
    if not new_film_data.get('year'):
        errors.append({"field": "year", "message": "Год обязателен"})
    elif not isinstance(new_film_data['year'], int) or new_film_data['year'] < 1895 or new_film_data['year'] > 2025:
        errors.append({"field": "year", "message": "Год должен быть в диапазоне 1895-2025"})
    
    if not new_film_data.get('description') or not new_film_data['description'].strip():
        errors.append({"field": "description", "message": "Описание обязательно"})
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    films.append(new_film_data)
    return jsonify({"id": len(films) - 1}), 201