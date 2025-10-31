
from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab33():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('/lab3/lab3/lab3.html', name=name, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('name_color', '', expires=0)
    return resp