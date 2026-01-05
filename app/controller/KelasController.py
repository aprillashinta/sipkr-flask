from app.model.kelas import Kelas
from app import db, response
from flask import request

def index():
    try:
        kelas = Kelas.query.all()
        data = [{'id': k.id, 'nama_mk': k.nama_mk, 'sks': k.sks} for k in kelas]
        return response.success(data, "Berhasil mengambil data kelas")
    except Exception as e:
        return response.error([], str(e))

def store():
    try:
        nama_mk = request.form.get('nama_mk')
        sks = request.form.get('sks')
        
        baru = Kelas(nama_mk=nama_mk, sks=sks)
        db.session.add(baru)
        db.session.commit()
        return response.success('', 'Kelas berhasil ditambahkan!')
    except Exception as e:
        return response.error([], str(e))