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
                flash("Ruangan sudah terpakai di jam tersebut!", "error")
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
    
# --- FITUR CETAK LAPORAN ---
@jadwal_bp.route('/cetak-laporan', methods=['GET'])
@staticmethod
def cetak_laporan():
        try:
            # 1. Ambil Data
            data_jadwal = Jadwal.query.all()
            data_ruangan = Ruangan.query.all()

            # 2. UPDATE: Slot Waktu dibuat PER JAM (07.00 s/d 22.00)
            # Format: (Jam Mulai, Jam Selesai)
            time_slots_data = [
                ("07.00", "08.00"), ("08.00", "09.00"), ("09.00", "10.00"),
                ("10.00", "11.00"), ("11.00", "12.00"), ("12.00", "13.00"),
                ("13.00", "14.00"), ("14.00", "15.00"), ("15.00", "16.00"),
                ("16.00", "17.00"), ("17.00", "18.00"), ("18.00", "19.00"),
                ("19.00", "20.00"), ("20.00", "21.00"), ("21.00", "22.00")
            ]
            
            # Buat list string untuk header HTML (07.00-08.00, dst)
            time_slots_view = [f"{s}-{e}" for s, e in time_slots_data]
            
            days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]

            # 3. Buat Matrix Kosong
            matrix = {}
            for day in days:
                matrix[day] = {}
                for s, e in time_slots_data:
                    key = f"{s}-{e}"
                    matrix[day][key] = {}
                    for ruang in data_ruangan:
                        matrix[day][key][ruang.nama_ruang] = None 

            # 4. Logic Mapping Data (Tetap Pakai Logic Overlap Pintar)
            for j in data_jadwal:
                if not j.ruangan or not j.kelas: continue
                
                hari_db = j.hari.capitalize() 
                if hari_db not in days: continue

                # Helper konversi jam
                def to_float(t):
                    try:
                        return float(t.strftime("%H.%M"))
                    except:
                        return float(str(t)[:5].replace(':', '.'))

                j_start = to_float(j.jam_mulai)
                j_end = to_float(j.jam_selesai)
                
                # Cek overlap
                for s_str, e_str in time_slots_data:
                    slot_start = float(s_str)
                    slot_end = float(e_str)
                    
                    # LOGIKA: Jika jadwal overlap dengan jam ini
                    if j_start < slot_end and j_end > slot_start:
                        
                        key = f"{s_str}-{e_str}"
                        nama_ruang = j.ruangan.nama_ruang
                        
                        # TAMPILAN: Kode MK (Atas) & Dosen (Bawah)
                        # Contoh: SI201 (RUD)
                        
                        # Ambil Kode MK (misal 6 huruf)
                        kode_mk = j.kelas.nama_mk[:15] # Sesuaikan panjangnya
                        
                        # Ambil Inisial Dosen (3 huruf kapital)
                        dosen = "".join([x[0] for x in j.dosen.nama.split()]).upper()[:3]

                        if hari_db in matrix and key in matrix[hari_db]:
                            # Gunakan <br> agar turun baris
                            matrix[hari_db][key][nama_ruang] = f"{kode_mk}<br>({dosen})"

            # 5. Render
            return render_template('print_laporan.html', 
                                   matrix=matrix, 
                                   ruangan_list=data_ruangan, 
                                   days=days, 
                                   time_slots=time_slots_view)
                                   
        except Exception as e:
            print(f"ERROR: {e}")
            return f"Error: {str(e)}"