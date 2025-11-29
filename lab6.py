from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

lab6 = Blueprint('lab6', __name__)

# Глобальный список офисов с разной стоимостью
offices = []
for i in range(1, 11):
    # Разная стоимость: 900 + номер_офиса * 100
    offices.append({"number": i, "tenant": "", "price": 900 + i * 100})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['login'] = request.form.get('login')
        return redirect(url_for('lab6.main'))
    return '''
        <form method="post">
            <input type="text" name="login" placeholder="Введите логин" required>
            <input type="submit" value="Войти">
        </form>
    '''

@lab6.route('/lab6/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab6.main'))

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json()
    
    # Проверяем корректность запроса
    if not data or 'jsonrpc' not in data or data['jsonrpc'] != '2.0':
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": None
        })
    
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')
    
    # Метод info доступен без авторизации
    if method == 'info':
        return jsonify({
            'jsonrpc': '2.0',
            'result': offices,
            'id': request_id
        })
    
    # Для методов бронирования и отмены нужна авторизация
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': request_id
        })
    
    if method == 'booking':
        office_number = params.get('number')
        
        for office in offices:
            if office['number'] == office_number:
                # Проверка: офис не должен быть уже арендован
                if office['tenant']:
                    return jsonify({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': f'Office {office_number} is already booked'
                        },
                        'id': request_id
                    })
                # Бронируем офис
                office['tenant'] = login 
                return jsonify({
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                })
        
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': f'Office {office_number} not found'
            },
            'id': request_id
        })
    
    elif method == 'cancellation':
        office_number = params.get('number')
        
        for office in offices:
            if office['number'] == office_number:
                # Проверка: офис должен быть арендован
                if not office['tenant']:
                    return jsonify({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 5,
                            'message': f'Office {office_number} is not booked'
                        },
                        'id': request_id
                    })
                # Проверка: офис должен быть арендован текущим пользователем
                if office['tenant'] != login:
                    return jsonify({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You can only cancel your own bookings'
                        },
                        'id': request_id
                    })
                # Снимаем аренду
                office['tenant'] = ""
                return jsonify({
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                })
        
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': f'Office {office_number} not found'
            },
            'id': request_id
        })
    
    # Если метод не найден
    return jsonify({
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': request_id
    })