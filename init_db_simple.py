# init_db_simple.py
from app import app
from app import db

with app.app_context():
    print("Создаем таблицы...")
    db.create_all()
    print("✅ Все таблицы созданы!")
    
    # Проверяем
    from app import User, Article
    print(f"Таблица: {User.__tablename__}")
    print(f"Таблица: {Article.__tablename__}")