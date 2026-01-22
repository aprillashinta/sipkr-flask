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
        print(f"Error Database Jadwal: {str(e)}")
        return f"Terjadi kesalahan pada database: {str(e)}"

@jadwal_bp.route('/jadwal/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            hari = request.form.get('hari')
            jam_mulai = request.form.get('jam_mulai')
            jam_selesai = request.form.get('jam_selesai')
            dosen_id = request.form.get('dosen_id')
            ruangan_id = request.form.get('ruangan_id')
            kelas_id = request.form.get('kelas_id')

            bentrok_ruangan = Jadwal.query.filter_by(hari=hari, ruangan_id=ruangan_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()

            if bentrok_ruangan:
                flash("Ruangan sudah terpakai di jam tersebut!", "error")
                return redirect(url_for('web.jadwal_create'))

            bentrok_dosen = Jadwal.query.filter_by(hari=hari, dosen_id=dosen_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()

            if bentrok_dosen:
                flash("Dosen sudah ada jadwal mengajar di jam tersebut!", "error")
                return redirect(url_for('web.jadwal_create'))

            bentrok_kelas = Jadwal.query.filter_by(hari=hari, kelas_id=kelas_id).filter(
                (Jadwal.jam_mulai < jam_selesai) & (Jadwal.jam_selesai > jam_mulai)
            ).first()

            if bentrok_kelas:
                flash("Kelas ini sudah ada jadwal kuliah di jam tersebut!", "error")
                return redirect(url_for('web.jadwal_create'))

            baru = Jadwal(
                hari=hari,
                jam_mulai=jam_mulai,
                jam_selesai=jam_selesai,
                dosen_id=dosen_id,
                ruangan_id=ruangan_id,
                kelas_id=kelas_id
            )
            db.session.add(baru)
            db.session.commit()

            flash("Jadwal berhasil disimpan!", "success")
            return redirect(url_for('web.jadwal_index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Gagal menyimpan jadwal: {str(e)}", "error")
            return redirect(url_for('web.jadwal_create'))

    dosen = Dosen.query.all()
    kelas = Kelas.query.all()
    ruangan = Ruangan.query.all()
    return render_template('jadwal/create.html', dosen=dosen, kelas=kelas, ruangan=ruangan)


@jadwal_bp.route('/jadwal/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    jadwal = Jadwal.query.get(id)
    list_dosen = Dosen.query.all()
    list_kelas = Kelas.query.all()
    list_ruangan = Ruangan.query.all()

    if request.method == 'POST':
        try:
            jadwal.hari = request.form.get('hari')
            jadwal.jam_mulai = request.form.get('jam_mulai')
            jadwal.jam_selesai = request.form.get('jam_selesai')
            jadwal.dosen_id = request.form.get('dosen_id')
            jadwal.kelas_id = request.form.get('kelas_id')
            jadwal.ruangan_id = request.form.get('ruangan_id')

            db.session.commit()
            flash('Jadwal berhasil diperbarui!', 'success')
            return redirect(url_for('web.jadwal_index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Gagal update: {str(e)}", "error")
            return redirect(url_for('web.jadwal_edit', id=id))

    return render_template(
        'jadwal/edit.html',
        data=jadwal,
        semua_dosen=list_dosen,
        semua_kelas=list_kelas,
        semua_ruang=list_ruangan
    )


@jadwal_bp.route('/jadwal/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        jadwal = Jadwal.query.get(id)
        if jadwal:
            db.session.delete(jadwal)
            db.session.commit()
            flash('Jadwal berhasil dihapus', 'success')
        return redirect(url_for('web.jadwal_index'))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('web.jadwal_index'))
