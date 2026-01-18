# __init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev-key-123'
    
    # АБСОЛЮТНЫЕ импорты (без точки в начале)
    try:
        from lab7 import lab7
        app.register_blueprint(lab7, url_prefix='/lab7')
        print("✅ Lab7 зарегистрирована")
    except ImportError as e:
        print(f"⚠️ Ошибка загрузки lab7: {e}")
    
    try:
        from lab7_with_db import lab7_db
        app.register_blueprint(lab7_db, url_prefix='/lab7-db')
        print("✅ Lab7 с БД зарегистрирована")
    except ImportError as e:
        print(f"⚠️ Ошибка загрузки lab7 с БД: {e}")
    
    @app.route('/')
    def index():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Лабораторные работы</title>
            <style>
                body { font-family: Arial; margin: 40px; }
                h1 { color: #333; }
                .menu { background: #f5f5f5; padding: 20px; border-radius: 8px; }
                .btn { display: inline-block; padding: 10px 20px; margin: 10px 5px; 
                       background: #4CAF50; color: white; text-decoration: none; 
                       border-radius: 4px; }
                .btn:hover { background: #45a049; }
                .btn-db { background: #9C27B0; }
                .btn-db:hover { background: #7b1fa2; }
            </style>
        </head>
        <body>
            <h1>Лабораторные работы</h1>
            <div class="menu">
                <h2>Лабораторная работа 7</h2>
                <a href="/lab7" class="btn">Базовая версия</a>
                <a href="/lab7-db" class="btn btn-db">Версия с БД (доп. задание)</a>
                <p><strong>Дополнительное задание:</strong> реализована валидация и база данных</p>
            </div>
        </body>
        </html>
        '''
    
    return app

app = create_app()