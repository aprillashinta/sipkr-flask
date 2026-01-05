from app.model.dosen import Dosen
from app import db, response
from flask import Blueprint, request, flash, redirect, url_for, render_template

dosen_bp = Blueprint('dosen_bp', __name__)

@dosen_bp.route('/dosen', methods=['GET', 'POST'])

def index():
    try:
        # Ambil data asli dari database
        dosen_list = Dosen.query.all()
        # Kirim ke template (data=dosen_list)
        return render_template('dosen/index.html', data=dosen_list)
    except Exception as e:
        print(e)
        flash("Gagal memuat data dosen", "danger")
        return redirect(url_for('web.dashboard'))

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
    
def create():
    if request.method == 'POST':
        # Logika simpan data
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        
        dosen_baru = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(dosen_baru)
        db.session.commit()
        return redirect(url_for('web.dosen_index'))
    
    # Menampilkan form HTML (Jangan pakai response.error lagi!)
    return render_template('dosen/create.html')

def delete(id):
    try:
        dosen = Dosen.query.get_or_404(id)
        db.session.delete(dosen)
        db.session.commit()
        flash('Dosen berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Gagal menghapus data.', 'danger')
        
    return redirect(url_for('web.dosen_index'))

def edit(id):
    dosen = Dosen.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Ambil data dari form
            dosen.nidn = request.form.get('nidn')
            dosen.nama = request.form.get('nama')
            dosen.phone = request.form.get('phone')
            dosen.alamat = request.form.get('alamat')
            
            db.session.commit()
            return redirect(url_for('web.dosen_index'))
            
        except Exception as e:
            # Jika error, batalkan proses database dan tampilkan errornya
            db.session.rollback()
            return f"Terjadi Error Database: {str(e)}" 
            
    return render_template('dosen/edit.html', dosen=dosen)