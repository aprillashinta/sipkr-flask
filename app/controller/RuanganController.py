from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.model.ruangan import Ruangan
from app import db

ruangan_bp = Blueprint('ruangan_bp', __name__)

@ruangan_bp.route('/ruangan', methods=['GET'])
def index():
    try:
        # Ambil semua data ruangan
        data_ruangan = Ruangan.query.all()
        return render_template('ruangan/index.html', data=data_ruangan)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('ruangan/index.html', data=[])

def create():
    if request.method == 'POST':
        try:
            nama_ruang = request.form.get('nama_ruang')
            kapasitas = request.form.get('kapasitas')
            jenis = request.form.get('jenis')
            
            baru = Ruangan(nama_ruang=nama_ruang, kapasitas=kapasitas, jenis=jenis)
            db.session.add(baru)
            db.session.commit()
            
            flash('Ruangan berhasil ditambahkan!', 'success')
            return redirect(url_for('web.ruangan_index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", 'danger')

    return render_template('ruangan/create.html')

def delete(id):
    try:
        ruangan = Ruangan.query.get(id)
        if ruangan:
            db.session.delete(ruangan)
            db.session.commit()
            flash('Data ruangan berhasil dihapus', 'success')
        return redirect(url_for('web.ruangan_index'))
    except Exception as e:
        return f"Error: {str(e)}"
    
def edit(id):
    # 1. Ambil data ruangan berdasarkan ID
    ruangan = Ruangan.query.get(id)
    
    if not ruangan:
        flash('Data ruangan tidak ditemukan!', 'danger')
        return redirect(url_for('web.ruangan_index'))

    if request.method == 'POST':
        try:
            # 2. Update data dengan inputan baru
            ruangan.nama_ruang = request.form.get('nama_ruang')
            ruangan.jenis = request.form.get('jenis')
            ruangan.kapasitas = request.form.get('kapasitas')
            
            # 3. Commit perubahan ke database
            db.session.commit()
            
            flash('Data ruangan berhasil diperbarui!', 'success')
            return redirect(url_for('web.ruangan_index'))
        except Exception as e:
            db.session.rollback()
            return f"Gagal update: {str(e)}"

    # 4. Tampilkan form edit dengan membawa data lama
    return render_template('ruangan/edit.html', data=ruangan)