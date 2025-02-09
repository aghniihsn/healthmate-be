from flask import Flask
from config import Config
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
from eventlet import wsgi
import sys



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

# socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode) 

print(f'run2')

# from api.model import user, medicine, reminder, notification

from api import routes

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.start()
# print(f'run3')

# print(f'run4')

logging.basicConfig(filename="error.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
