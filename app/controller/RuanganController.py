from app.model.ruangan import Ruangan
from app import db, response
from flask import Blueprint, request

ruangan_bp = Blueprint('ruangan_bp', __name__)

@ruangan_bp.route('/ruangan', methods=['GET', 'POST'])

def index():
    try:
        ruangan = Ruangan.query.all()
        data = [{'id': r.id, 'nama': r.nama_ruang, 'kapasitas': r.kapasitas} for r in ruangan]
        return response.success(data, "Berhasil mengambil data ruangan")
    except Exception as e:
        return response.error([], str(e))

def store():
    try:
        nama = request.form.get('nama_ruang')
        kapasitas = request.form.get('kapasitas')
        
        baru = Ruangan(nama_ruang=nama, kapasitas=kapasitas)
        db.session.add(baru)
        db.session.commit()
        return response.success('', 'Ruangan berhasil ditambahkan!')
    except Exception as e:
        return response.error([], str(e))