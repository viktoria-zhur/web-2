from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Для обратной совместимости, добавим модели
class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'lab8'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    
    # Для Flask-Login
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Article(db.Model):
    __tablename__ = 'articles'
    __bind_key__ = 'lab8'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())