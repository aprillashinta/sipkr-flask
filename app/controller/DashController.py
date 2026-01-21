from flask import Blueprint, render_template
from app.models import Dosen, Kelas, Ruangan, Jadwal

dash_bp = Blueprint('dash_bp', __name__)

@dash_bp.route('/dashboard')
def dashboard():
    total_dosen = Dosen.query.count()
    total_kelas = Kelas.query.count()
    total_ruangan = Ruangan.query.count()

    # sementara: hitung semua jadwal
    jadwal_aktif = Jadwal.query.count()

    # kalau tabel jadwal punya kolom status:
    # jadwal_aktif = Jadwal.query.filter_by(status='aktif').count()

    return render_template(
        'dashboard.html',
        total_dosen=total_dosen,
        total_kelas=total_kelas,
        total_ruangan=total_ruangan,
        jadwal_aktif=jadwal_aktif
    )
