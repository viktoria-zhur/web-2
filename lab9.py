from flask import Blueprint, render_template, session, jsonify, request
import random

lab9_bp = Blueprint('lab9', __name__)

# Хранилище подарков (в памяти)
gifts = {
    i: f"Поздравление {i}: С Новым Годом! 🎄"
    for i in range(1, 11)
}

opened_gifts = set()

@lab9_bp.route('/')
def index():
    return render_template('lab9/index.html')