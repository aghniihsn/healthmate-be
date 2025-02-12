from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

import threading
import schedule
import time

from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config(object):
    isProd = os.environ.get("FLASK_ENV") != "development"
    
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))
    DB_PORT = str(os.environ.get("DB_PORT"))
    
    if isProd:
        HOST = "sql12.freesqldatabase.com"
        DATABASE = "sql12761945"
        USERNAME = "sql12761945"
        PASSWORD = "eJfUGjrSIR"
        DB_PORT = "3306"
        
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    print(f'prod', isProd)
    print(f'HOST', HOST)

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{DB_PORT}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERY = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')



app = Flask(__name__)

# Jalankan job_runner di thread terpisah
scheduler = BackgroundScheduler()
scheduler.start()
print(f'run scheduler..')

# scheduler.init_app(app)
app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
print(f'prepare flask, config, jwt, db, migrate')

from api.model import user, medicine, reminder, notification
from api import routes

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

if __name__ == '__main__':
    
    app.run(debug=True)
    print(f'Server running...')
    
