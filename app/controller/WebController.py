from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps

from app.controller import AuthController, DosenController, KelasController, JadwalController, RuanganController
from app.model.dosen import Dosen
from app.model.kelas import Kelas
from app.model.ruangan import Ruangan
from app.model.jadwal import Jadwal

web = Blueprint('web', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function


@web.route('/')
def index():
    return 'SIPKR Flask is running'


@web.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user'):
        return redirect(url_for('web.dashboard'))
    return AuthController.login()


@web.route('/dashboard')
@login_required
def dashboard():
    total_dosen = Dosen.query.count()
    total_kelas = Kelas.query.count()
    total_ruangan = Ruangan.query.count()
    jadwal_aktif = Jadwal.query.count()

    return render_template(
        'dashboard.html',
        total_dosen=total_dosen,
        total_kelas=total_kelas,
        total_ruangan=total_ruangan,
        jadwal_aktif=jadwal_aktif
    )


@web.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('web.login'))


@web.route('/dosen')
@login_required
def dosen_index():
    return DosenController.index()


@web.route('/dosen/tambah', methods=['GET', 'POST'])
@login_required
def dosen_create():
    return DosenController.create()


@web.route('/dosen/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def dosen_edit(id):
    return DosenController.edit(id)


@web.route('/dosen/hapus/<int:id>', methods=['POST'])
@login_required
def dosen_delete(id):
    return DosenController.delete(id)


@web.route('/kelas')
@login_required
def kelas_index():
    return KelasController.index()


@web.route('/kelas/tambah', methods=['GET', 'POST'])
@login_required
def kelas_create():
    return KelasController.create()


@web.route('/kelas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def kelas_edit(id):
    return KelasController.edit(id)


@web.route('/kelas/hapus/<int:id>', methods=['POST'])
@login_required
def kelas_delete(id):
    return KelasController.delete(id)


@web.route('/jadwal')
@login_required
def jadwal_index():
    return JadwalController.index()


@web.route('/jadwal/tambah', methods=['GET', 'POST'])
@login_required
def jadwal_create():
    return JadwalController.create()


@web.route('/jadwal/edit/<id>', methods=['GET', 'POST'])
@login_required
def jadwal_edit(id):
    return JadwalController.edit(id)


@web.route('/jadwal/hapus/<id>', methods=['POST'])
@login_required
def jadwal_delete(id):
    return JadwalController.delete(id)


@web.route('/ruangan')
@login_required
def ruangan_index():
    return RuanganController.index()


@web.route('/ruangan/tambah', methods=['GET', 'POST'])
@login_required
def ruangan_create():
    return RuanganController.create()


@web.route('/ruangan/hapus/<id>', methods=['POST'])
@login_required
def ruangan_delete(id):
    return RuanganController.delete(id)


@web.route('/ruangan/edit/<id>', methods=['GET', 'POST'])
@login_required
def ruangan_edit(id):
    return RuanganController.edit(id)
