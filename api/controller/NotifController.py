from api.index import db, socketio
from api import response
from api.model.notification import Notification  

from api.model.medicine import Medicine  
import requests

def getAll(id):  
    try:  
        # Ambil data dari database dengan join antara Reminder dan Medicine
        result = db.session.query(Notification).filter(Notification.user_id == id).all()
        
        # Debugging: Cetak hasil ke terminal
        print(f"result: {result}")

        if not result:  
            return response.error('', 'Data tidak ditemukan')  

        # Proses data hasil query dan ubah menjadi format yang diinginkan
        data = []
        for notification in result:
            new_notif = {  
                    "id_notification": notification.id_notification,
                    "message": notification.message,
                    "created_at": notification.created_at.strftime('%Y-%m-%d %H:%M:%S') if notification.created_at else None
            }
            data.append(new_notif)

        print(f"Notification data: {data}")

        return response.success(data, 'Sukses Mengambil Detail Data')  

    except Exception as e:  
        print(e)  
        return response.error('', 'Gagal Mengambil Detail Data')


def send_notif(token, target, message):
    try:
       socketio.emit("notification", message)
    except requests.exceptions.RequestException as e:
        print(f"Error sending notif: {str(e)}")
        return {"error": str(e)}

def send_message(token, target, message):
    print(f"Sending message to {target}: {message}")  # Debugging
    url = "https://dash.pushwa.com/api/kirimPesan"
    payload = {
        "token": token,
        "target": target,
        "type": "text",
        "delay": "1",
        "message": message,
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        send_notif(token, target, message)
        return response.json()  # Mengembalikan respons dari API
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {str(e)}")
        return {"error": str(e)}
    
def send_notification_via_websocket(message):  
    print(f"Sending WebSocket notification: {message}")  # Debugging  
    socketio.emit('notification', {'message': message}, broadcast=True)