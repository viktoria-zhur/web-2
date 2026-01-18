# database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(200), nullable=True)
    russian_title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.original_title or self.russian_title,
            "title_ru": self.russian_title,
            "year": self.year,
            "description": self.description
        }

def init_db(app):
    """Инициализация базы данных"""
    db.init_app(app)
    
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        
        # Добавляем тестовые данные, если таблица пуста
        if Movie.query.count() == 0:
            test_movies = [
                Movie(
                    original_title="Interstellar",
                    russian_title="Интерстеллар",
                    year=2014,
                    description="Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
                ),
                Movie(
                    original_title="The Shawshank Redemption",
                    russian_title="Побег из Шоушенка",
                    year=1994,
                    description="Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
                )
            ]
            db.session.add_all(test_movies)
            db.session.commit()