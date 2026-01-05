from app.model.dosen import Dosen
from app import db, response
from flask import request

def index():
    try:
        dosen = Dosen.query.all()
        data = transform(dosen)
        return response.success(data, "Berhasil mengambil data dosen")
    except Exception as e:
        print(e)
        return response.error([], "Gagal mengambil data")

def transform(dosen):
    array = []
    for i in dosen:
        array.append({
            'id': i.id,
            'nidn': i.nidn,
            'nama': i.nama,
            'phone': i.phone,
            'alamat': i.alamat
        })
    return array

def store():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        dosen_baru = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        
        db.session.add(dosen_baru)
        db.session.commit()

        return response.success('', 'Dosen berhasil ditambahkan!')
    except Exception as e:
        print(e)
        return response.error([], 'Gagal menambahkan dosen')