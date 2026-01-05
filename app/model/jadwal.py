from app import db
from datetime import datetime

class Jadwal(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    hari = db.Column(db.String(20), nullable=False) # Senin, Selasa, dst.
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)

    # Foreign Keys (Menghubungkan ke tabel lain)
    dosen_id = db.Column(db.BigInteger, db.ForeignKey('dosen.id'), nullable=False)
    kelas_id = db.Column(db.BigInteger, db.ForeignKey('kelas.id'), nullable=False)
    ruangan_id = db.Column(db.BigInteger, db.ForeignKey('ruangan.id'), nullable=False)

    # Relasi agar mudah dipanggil di template
    dosen = db.relationship('Dosen', backref='jadwal_dosen')
    kelas = db.relationship('Kelas', backref='jadwal_kelas')
    ruangan = db.relationship('Ruangan', backref='jadwal_ruangan')

    def __repr__(self):
        return '<Jadwal {} - {}>'.format(self.hari, self.jam_mulai)