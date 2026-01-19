# lab9.py
from flask import Blueprint, render_template, session, jsonify, request
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

# Хранилище открытых коробок
opened_gifts = {}

# Новогодние поздравления
gifts_data = {
    1: {"text": "С Новым Годом! Пусть сбываются самые заветные мечты!", "image": "🎁"},
    2: {"text": "Желаем крепкого здоровья и безграничного счастья в новом году!", "image": "🎄"},
    3: {"text": "Пусть удача всегда будет на вашей стороне во всех начинаниях!", "image": "🌟"},
    4: {"text": "Счастья, любви и благополучия вашей прекрасной семье!", "image": "❤️"},
    5: {"text": "Успехов в работе, творческих побед и новых достижений!", "image": "🏆"},
    6: {"text": "Мира, добра, уютных вечеров в кругу близких!", "image": "🏡"},
    7: {"text": "Финансового процветания, стабильности и изобилия!", "image": "💰"},
    8: {"text": "Интересных путешествий, ярких впечатлений и новых знакомств!", "image": "✈️"},
    9: {"text": "Крепкого здоровья, бодрости духа и энергии на весь год!", "image": "💪"},
    10: {"text": "Исполнения всех желаний и волшебства в новом году!", "image": "✨"}
}

@lab9.route('/')
def index():
    # Инициализация сессии
    if 'session_id' not in session:
        session['session_id'] = datetime.now().strftime("%Y%m%d%H%M%S%f")
        opened_gifts[session['session_id']] = []
    
    session_id = session['session_id']
    opened_gift_ids = opened_gifts.get(session_id, [])
    
    # Статистика
    total_gifts = len(gifts_data)
    opened_count = len(opened_gift_ids)
    remaining = total_gifts - opened_count
    
    return render_template('lab9/index.html',
                         total_gifts=total_gifts,
                         opened_count=opened_count,
                         remaining=remaining,
                         opened_gifts=opened_gift_ids)

@lab9.route('/open_gift/<int:gift_id>', methods=['POST'])
def open_gift(gift_id):
    # Проверка ID
    if gift_id < 1 or gift_id > len(gifts_data):
        return jsonify({'error': 'Неверный номер подарка!'})
    
    # Инициализация сессии
    if 'session_id' not in session:
        session['session_id'] = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    session_id = session['session_id']
    if session_id not in opened_gifts:
        opened_gifts[session_id] = []
    
    opened_gift_ids = opened_gifts[session_id]
    
    # Проверка лимита
    if len(opened_gift_ids) >= 3:
        return jsonify({'error': 'Можно открыть не более 3 коробок!'})
    
    # Проверка на уже открытую коробку
    if gift_id in opened_gift_ids:
        return jsonify({'error': 'Эта коробка уже пуста!'})
    
    # Открываем коробку
    opened_gift_ids.append(gift_id)
    
    # Получаем данные подарка
    gift_info = gifts_data[gift_id]
    
    # Статистика
    opened_count = len(opened_gift_ids)
    remaining = len(gifts_data) - opened_count
    
    return jsonify({
        'success': True,
        'message': gift_info['text'],
        'image': gift_info['image'],
        'gift_id': gift_id,
        'opened_count': opened_count,
        'remaining': remaining,
        'can_open_more': opened_count < 3
    })

@lab9.route('/reset_gifts', methods=['POST'])
def reset_gifts():
    if 'session_id' in session:
        session_id = session['session_id']
        if session_id in opened_gifts:
            opened_gifts[session_id] = []
    
    return jsonify({
        'success': True,
        'message': '🎅 Все подарки восстановлены! Можете открывать снова!',
        'total_gifts': len(gifts_data),
        'remaining': len(gifts_data)
    })

@lab9.route('/status')
def get_status():
    if 'session_id' not in session:
        opened_count = 0
        opened_gift_ids = []
    else:
        session_id = session['session_id']
        opened_gift_ids = opened_gifts.get(session_id, [])
        opened_count = len(opened_gift_ids)
    
    remaining = len(gifts_data) - opened_count
    
    return jsonify({
        'total_gifts': len(gifts_data),
        'opened_count': opened_count,
        'remaining': remaining,
        'opened_gifts': opened_gift_ids,
        'can_open_more': opened_count < 3
    })

@lab9.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('username') == 'dedmoroz' and data.get('password') == '2025':
        session['is_admin'] = True
        return jsonify({'success': True, 'message': 'Добро пожаловать, Дед Мороз!'})
    return jsonify({'success': False, 'error': 'Неверные данные!'})

@lab9.route('/admin/reset_all', methods=['POST'])
def admin_reset_all():
    if not session.get('is_admin'):
        return jsonify({'error': 'Только для Деда Мороза!'})
    
    opened_gifts.clear()
    
    return jsonify({
        'success': True,
        'message': '🎅 Все подарки во всех сессиях восстановлены!'
    })