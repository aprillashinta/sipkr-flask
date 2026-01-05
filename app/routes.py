from flask import Blueprint, render_template, redirect, url_for, session
# Pastikan import DosenController dari package controller
from app.controller import AuthController, DosenController 

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return 'TEST'

@web.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login()

@web.route('/dashboard')
def dashboard():
    if not session.get('user'):
        return redirect(url_for('web.login'))
    return render_template('dashboard.html')

# ==========================================
# ROUTING CRUD DOSEN
# ==========================================

# 1. READ - Menampilkan daftar semua dosen
@web.route('/dosen')
def dosen_index():
    # Proteksi: hanya user login yang bisa akses
    if not session.get('user'):
        return redirect(url_for('web.login'))
    
    return DosenController.index()

# 2. CREATE - Form tambah dan Proses simpan
@web.route('/dosen/tambah', methods=['GET', 'POST'])
def dosen_create():
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return DosenController.create()

# 3. UPDATE - Form edit dan Proses update berdasarkan ID
@web.route('/dosen/edit/<int:id>', methods=['GET', 'POST'])
def dosen_edit(id):
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return DosenController.edit(id)

# 4. DELETE - Proses hapus data
# Menggunakan POST untuk keamanan (mencegah hapus via link langsung)
@web.route('/dosen/hapus/<int:id>', methods=['POST'])
def dosen_delete(id):
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return DosenController.delete(id)