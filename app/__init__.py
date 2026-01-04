from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'sipkr-secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.model import user
from app.model import dosen
from app.model import kelas
from app.model import ruangan
from app.model import jadwal

from app import routes
