from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.model.jadwal import Jadwal
from app.model.dosen import Dosen
from app.model.kelas import Kelas
from app.model.ruangan import Ruangan
from app import db

jadwal_bp = Blueprint('jadwal_bp', __name__)

@jadwal_bp.route('/jadwal', methods=['GET'])

def index():
    try:
        jadwal = Jadwal.query.all()
        return render_template('jadwal/index.html', data=jadwal)
    except Exception as e:
        # Jika error (misal tabel belum ada), cetak di terminal dan tampilkan pesan
        print(f"Error Database Jadwal: {str(e)}")
        return f"Terjadi kesalahan pada database: {str(e)}"

def create():
    if request.method == 'POST':
        try:
            # Ambil data dari form
            hari = request.form.get('hari')
            jam_mulai = request.form.get('jam_mulai')
            jam_selesai = request.form.get('jam_selesai')
            dosen_id = request.form.get('dosen_id')
            ruangan_id = request.form.get('ruangan_id')
            kelas_id = request.form.get('kelas_id')

            # --- LOGIKA CEK BENTROK (Sama seperti kodemu sebelumnya) ---
            bentrok_ruangan = Jadwal.query.filter_by(hari=hari, ruangan_id=ruangan_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()
            
            if bentrok_ruangan:
                flash("Ruangan sudah terpakai di jam tersebut!", "danger")
                return redirect(url_for('web.jadwal_create'))
            
            # --- TAMBAHAN: CEK BENTROK DOSEN ---
            # Cek apakah Dosen sudah mengajar di tempat lain di jam yang sama
            bentrok_dosen = Jadwal.query.filter_by(hari=hari, dosen_id=dosen_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()
            
            if bentrok_dosen:
                flash("Dosen sudah ada jadwal mengajar di jam tersebut!", "danger")
                return redirect(url_for('web.jadwal_create'))

            # --- TAMBAHAN: CEK BENTROK KELAS ---
            # Cek apakah Kelas ini sudah ada kuliah lain di jam yang sama
            bentrok_kelas = Jadwal.query.filter_by(hari=hari, kelas_id=kelas_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()
            
            if bentrok_kelas:
                flash("Kelas ini sudah ada jadwal kuliah di jam tersebut!", "danger")
                return redirect(url_for('web.jadwal_create'))
            
            # Simpan jika tidak bentrok
            baru = Jadwal(hari=hari, jam_mulai=jam_mulai, jam_selesai=jam_selesai, 
                          dosen_id=dosen_id, ruangan_id=ruangan_id, kelas_id=kelas_id)
            db.session.add(baru)
            db.session.commit()
            
            flash('Jadwal berhasil disimpan!', 'success')
            return redirect(url_for('web.jadwal_index'))
            
        except Exception as e:
            db.session.rollback()
            return f"Error saat simpan: {str(e)}"

    # GET: Tampilkan Form Tambah
    dosen = Dosen.query.all()
    kelas = Kelas.query.all()
    ruangan = Ruangan.query.all()
    return render_template('jadwal/create.html', dosen=dosen, kelas=kelas, ruangan=ruangan)

def edit(id):
    # 1. Ambil data jadwal yang mau diedit
    jadwal = Jadwal.query.get(id)
    
    # 2. Ambil semua data Master untuk isi Dropdown (PENTING!)
    list_dosen = Dosen.query.all()
    list_kelas = Kelas.query.all()
    list_ruangan = Ruangan.query.all()

    if request.method == 'POST':
        try:
            # 3. Update data dari form
            jadwal.hari = request.form.get('hari')
            jadwal.jam_mulai = request.form.get('jam_mulai')
            jadwal.jam_selesai = request.form.get('jam_selesai')
            
            # Update Foreign Keys
            jadwal.dosen_id = request.form.get('dosen_id')
            jadwal.kelas_id = request.form.get('kelas_id')
            jadwal.ruangan_id = request.form.get('ruangan_id')

            db.session.commit()
            flash('Jadwal berhasil diperbarui!', 'success')
            return redirect(url_for('web.jadwal_index'))
            
        except Exception as e:
            db.session.rollback()
            return f"Gagal update: {str(e)}"

    # 4. Kirim semua data ke HTML
    return render_template('jadwal/edit.html', data=jadwal, semua_dosen=list_dosen, semua_kelas=list_kelas, semua_ruang=list_ruangan)

def delete(id):
    try:
        jadwal = Jadwal.query.get(id)
        if jadwal:
            db.session.delete(jadwal)
            db.session.commit()
            flash('Jadwal berhasil dihapus', 'success')
        return redirect(url_for('web.jadwal_index'))
    except Exception as e:
        return f"Error: {str(e)}"