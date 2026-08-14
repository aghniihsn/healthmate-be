import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST", "127.0.0.1"))
    DB_PORT = str(os.environ.get("DB_PORT", "5432"))
    DATABASE = str(os.environ.get("DB_DATABASE", "med_app"))
    USERNAME = str(os.environ.get("DB_USERNAME", "root"))
    PASSWORD = str(os.environ.get("DB_PASSWORD", ""))
    DB_SCHEME = str(os.environ.get("DB_SCHEME", "postgresql+psycopg2"))

    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))

    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = f"{DB_SCHEME}://{USERNAME}:{PASSWORD}@{HOST}:{DB_PORT}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERY = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')