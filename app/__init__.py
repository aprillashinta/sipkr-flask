from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'sipkr-secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.model import user, dosen, kelas, ruangan, jadwal

from app.controller.WebController import web
from app.controller.DosenController import dosen_bp
from app.controller.DosenController import dosen_bp
from app.controller.KelasController import kelas_bp
from app.controller.RuanganController import ruangan_bp
from app.controller.JadwalController import jadwal_bp

# Registrasi blueprint ke aplikasi
app.register_blueprint(dosen_bp)
app.register_blueprint(kelas_bp)
app.register_blueprint(ruangan_bp)
app.register_blueprint(jadwal_bp)
app.register_blueprint(web)