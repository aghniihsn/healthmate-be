import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST", "127.0.0.1:3306"))
    DATABASE = str(os.environ.get("DB_DATABASE", "med_app"))
    USERNAME = str(os.environ.get("DB_USERNAME", "root"))
    PASSWORD = str(os.environ.get("DB_PASSWORD", ""))

    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERY = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')