from flask import request
from api.index import app, socketio
from api.controller import UserController
from api.controller.UserController import registerUser
from api.controller import ReminderController 
from api.controller import NotifController
from flask import jsonify

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/register', methods=['POST'])
def register():
    return registerUser()

@app.route('/login', methods = ['POST'])
def logins():
    return UserController.login(socketio)

@app.route("/notification/<id>", methods=['GET'])
def getAllNotification(id):
    return NotifController.getAll(id)

@app.route('/allUser', methods=['GET'])
def getAllUser():
    return UserController.getAllUsers()

@app.route('/user-by-token', methods = ['POST'])
def userByToken():
    return UserController.getUserbyToken()

@app.route('/reminder', methods=['GET', 'POST'])
def reminder(): 
    if request.method == 'GET':
        return ReminderController.show()
    else:
        return ReminderController.save()

@app.route('/history/<id>', methods=['GET'])
def history(id):
    return ReminderController.history(id)
    
@app.route('/reminder/<id>', methods=['GET', 'PUT', 'DELETE'])
def reminderDetail(id):
    if request.method == 'GET':
        return ReminderController.detail(id)
    elif request.method == 'PUT':
        return ReminderController.ubah(id)
    elif request.method == 'DELETE' :
        return ReminderController.hapus(id)
    
@app.route('/send_message', methods=['POST'])
def send_message():
    return NotifController.send_message()

@app.route('/send_notification', methods=['POST'])  
def send_notification():  
    data = request.json  
    message = data.get('message')  
    NotifController.send_notification_via_websocket(message)  
    return jsonify({"status": "success", "message": "Notification sent via WebSocket"})   

@app.route('/update-profile', methods=['PUT'])
def update_profile():
    return UserController.updateProfile()