import os

class config(object):
    HOST = os.environ.get("DB_HOST")
    DATABASE = os.environ.get("DB_DATABASE")
    USERNAME = os.environ.get("DB_USERNAME")
    PASSWORD = os.environ.get("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        + USERNAME
        + ":"
        + PASSWORD
        + "@"
        + HOST
        + "/"
        + DATABASE
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
