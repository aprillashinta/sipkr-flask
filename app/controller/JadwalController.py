from app.model.jadwal import Jadwal
from app import db, response
from flask import Blueprint, request

jadwal_bp = Blueprint('jadwal_bp', __name__)

@jadwal_bp.route('/jadwal', methods=['GET', 'POST'])

def index():
    try:
        jadwal = Jadwal.query.all()
        data = []
        for j in jadwal:
            data.append({
                'id': j.id,
                'hari': j.hari,
                'jam_mulai': str(j.jam_mulai),
                'dosen': j.dosen.nama,
                'ruangan': j.ruangan.nama_ruang,
                'mata_kuliah': j.kelas.nama_mk
            })
        return response.success(data, "Berhasil mengambil jadwal")
    except Exception as e:
        return response.error([], str(e))

def store():
    try:
        hari = request.form.get('hari')
        jam_mulai = request.form.get('jam_mulai')
        jam_selesai = request.form.get('jam_selesai')
        dosen_id = request.form.get('dosen_id')
        ruangan_id = request.form.get('ruangan_id')
        kelas_id = request.form.get('kelas_id')

        # LOGIKA CEK BENTROK RUANGAN
        bentrok_ruangan = Jadwal.query.filter_by(hari=hari, ruangan_id=ruangan_id).filter(
            (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
        ).first()
        
        if bentrok_ruangan:
            return response.error([], "Ruangan sudah terpakai di jam tersebut!")

        # LOGIKA CEK BENTROK DOSEN
        bentrok_dosen = Jadwal.query.filter_by(hari=hari, dosen_id=dosen_id).filter(
            (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
        ).first()

        if bentrok_dosen:
            return response.error([], "Dosen sudah memiliki jadwal lain di jam tersebut!")

        # Jika tidak bentrok, simpan
        baru = Jadwal(hari=hari, jam_mulai=jam_mulai, jam_selesai=jam_selesai, 
                      dosen_id=dosen_id, ruangan_id=ruangan_id, kelas_id=kelas_id)
        db.session.add(baru)
        db.session.commit()
        
        return response.success('', 'Jadwal berhasil dibuat!')
    except Exception as e:
        return response.error([], str(e))