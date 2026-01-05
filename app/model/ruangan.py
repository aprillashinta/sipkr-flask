from app import db

class Ruangan(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_ruang = db.Column(db.String(50), nullable=False) # Contoh: Lab Komputer 1
    kapasitas = db.Column(db.Integer, nullable=False)
    lokasi = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Ruangan {}>'.format(self.nama_ruang)