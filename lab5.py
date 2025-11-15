from flask import Blueprint, render_template

lab5 = Blueprint('lab5', __name__)

@lab5.route('/')
def main():
    return render_template('lab5.html', username="anonymous")

@lab5.route('/login')
def login():
    return "форма авторизации"

@lab5.route('/register')
def register():
    return "форма регистрации"

@lab5.route('/list')
def list_articles():
    return "список статей"

@lab5.route('/create')
def create_article():
    return "форма создания статьи"