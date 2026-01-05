from flask import Blueprint, render_template, redirect, url_for, session
from app.controller import AuthController

# Inisialisasi Blueprint dengan nama 'web'
web = Blueprint('web', __name__)

@web.route('/')
def index():
    return 'SIPKR Flask is running'

@web.route('/login', methods=['GET', 'POST'])
def login():
    # Jika user sudah login, langsung lempar ke dashboard
    if session.get('user'):
        return redirect(url_for('web.dashboard'))
    
    # Memanggil logika login dari AuthController
    return AuthController.login()

@web.route('/dashboard')
def dashboard():
    # Proteksi halaman: Jika belum login, tendang ke halaman login
    if not session.get('user'):
        return redirect(url_for('web.login'))
    
    # Temanmu nanti tinggal mengisi dashboard.html
    return render_template('dashboard.html')

@web.route('/logout')
def logout():
    # Menghapus session user saat logout
    session.clear()
    return redirect(url_for('web.login'))