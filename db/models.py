from datetime import datetime
from . import db
from flask_login import UserMixin

class users(db.Model, UserMixin):
    """Модель таблицы пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    articles = db.relationship('articles', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.login}>'


class articles(db.Model):
    """Модель таблицы статей"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Article {self.title}>'