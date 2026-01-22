from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.model.kelas import Kelas
from app import db

kelas_bp = Blueprint('kelas_bp', __name__)

# --- FUNGSI INDEX (DAFTAR KELAS) ---
def index():
    try:
        data_kelas = Kelas.query.all()
        return render_template('kelas/index.html', data=data_kelas)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('kelas/index.html', data=[])

# --- FUNGSI TAMBAH (CREATE) ---
def create():
    if request.method == 'POST':
        try:
            nama_mk = request.form.get('nama_mk')
            prodi = request.form.get('prodi')
            kode_mk = request.form.get('kode_mk')
            sks = request.form.get('sks')
            semester = request.form.get('semester')

            bentrok_kode = Kelas.query.filter_by(kode_mk=kode_mk).first()
            if bentrok_kode:
                flash('Kode mata kuliah sudah terdaftar!', 'error')
                return redirect(url_for('web.kelas_create'))

            baru = Kelas(
                nama_mk=nama_mk,
                prodi=prodi,
                kode_mk=kode_mk,
                sks=sks,
                semester=semester
            )

            db.session.add(baru)
            db.session.commit()

            flash('Mata Kuliah berhasil ditambahkan!', 'success')
            return redirect(url_for('web.kelas_index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Gagal menyimpan: {str(e)}", 'error')
            return redirect(url_for('web.kelas_create'))

    return render_template('kelas/create.html')

# --- FUNGSI EDIT (UPDATE) ---
def edit(id):
    kelas = Kelas.query.get(id)

    if not kelas:
        flash('Data mata kuliah tidak ditemukan!', 'error')
        return redirect(url_for('web.kelas_index'))

    if request.method == 'POST':
        try:
            kode_mk = request.form.get('kode_mk')
            nama_mk = request.form.get('nama_mk')
            prodi = request.form.get('prodi')
            sks = request.form.get('sks')
            semester = request.form.get('semester')

            bentrok_kode = Kelas.query.filter(
                Kelas.kode_mk == kode_mk,
                Kelas.id != id
            ).first()

            if bentrok_kode:
                flash('Kode mata kuliah sudah digunakan!', 'error')
                return redirect(url_for('web.kelas_edit', id=id))

            kelas.kode_mk = kode_mk
            kelas.nama_mk = nama_mk
            kelas.prodi = prodi
            kelas.sks = sks
            kelas.semester = semester

            db.session.commit()
            flash('Data mata kuliah berhasil diperbarui!', 'success')
            return redirect(url_for('web.kelas_index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Gagal update: {str(e)}', 'error')
            return redirect(url_for('web.kelas_edit', id=id))

    return render_template('kelas/edit.html', data=kelas)


# --- FUNGSI HAPUS (DELETE) ---
def delete(id):
    try:
        kelas = Kelas.query.get(id)
        if kelas:
            db.session.delete(kelas)
            db.session.commit()
            flash('Data mata kuliah berhasil dihapus', 'success')
        else:
            flash('Data tidak ditemukan', 'warning')
            
        return redirect(url_for('web.kelas_index'))
        
    except Exception as e:
        db.session.rollback()
        # Error biasanya karena data ini masih dipakai di Jadwal
        flash(f"Gagal hapus (Mungkin sedang dipakai di Jadwal): {str(e)}", 'danger')
        return redirect(url_for('web.kelas_index'))