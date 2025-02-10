from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import threading
import schedule
import time
from flask_socketio import SocketIO
import logging

import eventlet
import sys

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # HOST = str(os.environ.get("DB_HOST", "127.0.0.1:3306"))
    # DATABASE = str(os.environ.get("DB_DATABASE", "med_app"))
    # USERNAME = str(os.environ.get("DB_USERNAME", "root"))
    # PASSWORD = str(os.environ.get("DB_PASSWORD", ""))
    HOST = str(os.environ.get("DB_HOST", "sql12.freesqldatabase.com"))
    
    DATABASE = str(os.environ.get("DB_DATABASE", "sql12761945"))
    USERNAME = str(os.environ.get("DB_USERNAME", "sql12761945"))
    PASSWORD = str(os.environ.get("DB_PASSWORD", "eJfUGjrSIR"))
    DB_PORT = str(os.environ.get("DB_PORT", "3306"))
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{DB_PORT}/{DATABASE}"

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERY = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')



load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
print(Config.__class__)
print(type(Config))

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
print(f'run1')

if sys.platform == "win32":
    from gevent import monkey
    monkey.patch_all()
    async_mode = "gevent"
else:
    import eventlet
    async_mode = "eventlet"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode) 

print(f'run2')

from api.model import user, medicine, reminder, notification

from api import routes

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
print(f'run3')
logging.basicConfig(filename="error.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=True) 
