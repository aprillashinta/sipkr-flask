from flask import Blueprint, render_template, redirect, url_for, session
from app.controller import AuthController, DosenController, KelasController, JadwalController

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

# 1. READ - Menampilkan daftar kelas
@web.route('/kelas')
def kelas_index():
    if not session.get('user'):
        return redirect(url_for('web.login'))
    
    # Memanggil fungsi index() dari KelasController.py
    return KelasController.index()

# 2. CREATE - Form tambah kelas dan Proses simpan
@web.route('/kelas/tambah', methods=['GET', 'POST'])
def kelas_create():
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return KelasController.create()

# 3. UPDATE - Form edit kelas dan Proses update
@web.route('/kelas/edit/<int:id>', methods=['GET', 'POST'])
def kelas_edit(id):
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return KelasController.edit(id)

# 4. DELETE - Proses hapus kelas
@web.route('/kelas/hapus/<int:id>', methods=['POST'])
def kelas_delete(id):
    if not session.get('user'):
        return redirect(url_for('web.login'))
        
    return KelasController.delete(id)

@web.route('/jadwal')
def jadwal_index():
    return JadwalController.index()

@web.route('/jadwal/tambah', methods=['GET', 'POST'])
def jadwal_create():
    return JadwalController.create()