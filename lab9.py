# lab9.py
from flask import Blueprint, render_template, session, jsonify, request
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

# Хранилище открытых коробок
opened_gifts = {}

# Новогодние поздравления
gifts_data = {
    1: {"text": "С Новым Годом! Пусть сбываются самые заветные мечты!", "image": "🎁", "requires_auth": False},
    2: {"text": "Желаем крепкого здоровья и безграничного счастья в новом году!", "image": "🎄", "requires_auth": False},
    3: {"text": "Пусть удача всегда будет на вашей стороне во всех начинаниях!", "image": "🌟", "requires_auth": False},
    4: {"text": "Счастья, любви и благополучия вашей прекрасной семье!", "image": "❤️", "requires_auth": True},  # Требует авторизации
    5: {"text": "Успехов в работе, творческих побед и новых достижений!", "image": "🏆", "requires_auth": False},
    6: {"text": "Мира, добра, уютных вечеров в кругу близких!", "image": "🏡", "requires_auth": True},  # Требует авторизации
    7: {"text": "Финансового процветания, стабильности и изобилия!", "image": "💰", "requires_auth": False},
    8: {"text": "Интересных путешествий, ярких впечатлений и новых знакомств!", "image": "✈️", "requires_auth": True},  # Требует авторизации
    9: {"text": "Крепкого здоровья, бодрости духа и энергии на весь год!", "image": "💪", "requires_auth": False},
    10: {"text": "Исполнения всех желаний и волшебства в новом году!", "image": "✨", "requires_auth": False}
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
                         opened_gifts=opened_gift_ids,
                         is_authenticated=session.get('is_authenticated', False))

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
    
    # Проверка авторизации для специальных подарков (дополнительное задание)
    gift_info = gifts_data[gift_id]
    if gift_info.get('requires_auth', False) and not session.get('is_authenticated', False):
        return jsonify({'error': 'Этот подарок доступен только авторизованным пользователям! Войдите как Дед Мороз.'})
    
    # Открываем коробку
    opened_gift_ids.append(gift_id)
    
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
        'can_open_more': opened_count < 3,
        'requires_auth': gift_info.get('requires_auth', False)
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
        'can_open_more': opened_count < 3,
        'is_authenticated': session.get('is_authenticated', False)
    })

# Дополнительное задание: авторизация
@lab9.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Простая авторизация (в реальном приложении используйте базу данных)
    if username == 'dedmoroz' and password == '2025':
        session['is_authenticated'] = True
        session['username'] = 'Дед Мороз'
        return jsonify({'success': True, 'message': 'Добро пожаловать, Дед Мороз! Теперь доступны все подарки!'})
    
    return jsonify({'success': False, 'error': 'Неверные данные! Попробуйте: dedmoroz / 2025'})

@lab9.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_authenticated', None)
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Вы вышли из системы.'})

@lab9.route('/admin/status')
def admin_status():
    return jsonify({
        'is_authenticated': session.get('is_authenticated', False),
        'username': session.get('username', 'Гость')
    })

@lab9.route('/admin/reset_all', methods=['POST'])
def admin_reset_all():
    # Только для авторизованных пользователей (Дед Мороз)
    if not session.get('is_authenticated', False):
        return jsonify({'error': 'Эта функция доступна только Деду Морозу! Авторизуйтесь сначала.'})
    
    # Очищаем ВСЕ открытые подарки для ВСЕХ пользователей
    opened_gifts.clear()
    
    return jsonify({
        'success': True,
        'message': '🎅 Все подарки во всех сессиях восстановлены! Все коробки снова полны!'
    })