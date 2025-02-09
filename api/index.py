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

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode) 

print(f'run2')

# from api.model import user, medicine, reminder, notification

from api import routes

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
print(f'run3')

print(f'run4')

logging.basicConfig(filename="error.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# socketio.init_app(app)
wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
if __name__ == '__main__':

    
    print("Server is running...")
    socketio.run(app, host="0.0.0.0", port=5000)
    
    # socketio.run(app, debug=True, host="0.0.0.0", port=5000) 
    # print(f'run')

# from flask import Flask
# from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# import schedule
# import threading
# import time
# from flask_socketio import SocketIO
# import logging
# import eventlet
# from eventlet import wsgi

# # Inisialisasi
# db = SQLAlchemy()
# migrate = Migrate()
# import sys

# if sys.platform == "win32":
#     from gevent import monkey
#     monkey.patch_all()
#     async_mode = "gevent"
# else:
#     import eventlet
#     async_mode = "eventlet"

# socketio = SocketIO(cors_allowed_origins="*", async_mode=async_mode)

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Setup Flask Extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     CORS(app)
#     JWTManager(app)
#     socketio.init_app(app)

#     # Import routes setelah inisialisasi
#     from api import routes

#     return app

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.start()

# # Logging untuk production
# logging.basicConfig(filename="error.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# app = create_app()

# # Jika dijalankan langsung (untuk development)
# if __name__ == '__main__':
#     print("Server is running...")

#     # if async_mode == "eventlet":
#     # Jalankan dengan eventlet WSGI server
#     wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
#     socketio.run(app, host="0.0.0.0", port=5000)


