from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Все таблицы созданы!")
    
    # Проверяем
    from app import User, Article
    print(f"Таблица users: {User.__tablename__}")
    print(f"Таблица articles: {Article.__tablename__}")