from app import db

class Kelas(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_mk = db.Column(db.String(100), nullable=False)
    kode_mk = db.Column(db.String(20), unique=True, nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Kelas {}>'.format(self.nama_mk)