from flask import Blueprint, render_template, redirect, url_for, session
from app.controller import AuthController

web = Blueprint('web', __name__)

@web.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login()

@web.route('/dashboard')
def dashboard():
    if not session.get('user'):
        return redirect(url_for('web.login'))
    return render_template('dashboard.html')


@web.route('/')
def index():
    return 'SIPKR Flask is running'