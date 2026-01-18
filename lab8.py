from flask import Blueprint, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from os import path

lab8 = Blueprint('lab8', __name__)

# Заглушка для базы данных - будет заменена позже
class User:
    def __init__(self, id, login):
        self.id = id
        self.login = login
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

@lab8.route('/')
def index():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/index.html', username=username)

@lab8.route('/lab8/login/')
def login():
    return "Страница входа (будет реализована позже)"

@lab8.route('/lab8/register/')
def register():
    return "Страница регистрации (будет реализована позже)"

@lab8.route('/lab8/articles/')
def articles():
    return "Список статей (будет реализован позже)"

@lab8.route('/lab8/create/')
def create_article():
    return "Создание статьи (будет реализовано позже)"