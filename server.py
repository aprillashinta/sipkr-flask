from app import app
from app.routes import web

app.register_blueprint(web)
