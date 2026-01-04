from app import app
from app.controller import AuthController

@app.route('/')
def index():
    return "SIPKR Flask is running"

@app.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login()

from flask import render_template

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
