from flask import request, jsonify
import datetime
from api.index import app
from api.controller import UserController
from api.controller import ReminderController 
from api.controller import NotifController

@app.route('/')
def index():
    return 'Hello Flask'

@app.route("/notif/webhook/nomor/6281564602171", methods=['GET'])
def getMessage():
    return NotifController.getMessage()

@app.route("/notif/<user_id>", methods=['GET'])
def getAllNotification(user_id):
    return NotifController.getAll(user_id)

@app.route('/notif/send_message', methods=['POST'])
def send_message():
    return NotifController.send_message()

@app.route('/notif/send_notification', methods=['POST'])  
def send_notification():  
    data = request.json  
    message = data.get('message')  
    NotifController.send_notification_via_websocket(message)  
    return jsonify({"status": "success", "message": "Notification sent via WebSocket"})   

# User
@app.route('/register', methods=['POST'])
def register():
    return UserController.signUpUser()

@app.route('/login', methods = ['POST'])
def logins():
    return UserController.loginUser()

@app.route('/allUser', methods=['GET'])
def getAllUser():
    return UserController.getAllUsers()

@app.route('/update-profile', methods=['PUT'])
def update_profile():
    return UserController.updateProfile()

# @app.route('/user-by-token', methods = ['POST'])
# def userByToken():
#     return UserController.getUserbyToken()
# End User

# Reminder
@app.route('/reminder', methods=['GET', 'POST'])
def reminder(): 
    if request.method == 'GET':
        return ReminderController.show()
    else:
        return ReminderController.save()

@app.route('/reminder/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def reminderDetail(user_id):
    if request.method == 'GET':
        return ReminderController.detail(user_id)
    elif request.method == 'PUT':
        return ReminderController.ubah(user_id)
    elif request.method == 'DELETE' :
        return ReminderController.hapus(user_id)
    
@app.route('/reminder/history/<user_id>', methods=['GET'])
def history(user_id):
    return ReminderController.history(user_id)

@app.route("/reminder/run-jobs", methods=["POST"])
def run_jobs():
    return ReminderController.runJobs()
    

# End Reminder