from api import response
from api.index import db
from api.model.notification import Notification  
from api.model.medicine import Medicine  

import requests

def getAll(user_id):  
    try:  
        # Ambil data dari database dengan join antara Reminder dan Medicine
        result = db.session.query(Notification).filter(Notification.user_id == user_id).all()
        
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


def send_notif(target, message):
    print(f"Sending notif...")  # Debugging
    
    try:
       
        url = "https://api.onesignal.com/notifications?c=push"
        payload = {
            "app_id": "25850dc0-06ac-45c7-bbfb-3681b2a4450b",
            "contents": { "en": message },
            "included_segments": []
        }
        headers = {
            "accept": "application/json",
            "Authorization": "os_v2_app_ewcq3qagvrc4po73g2a3fjcfbns5gemf2eretgmoyysttjc4ntbygsg47cqh6jmij4fnlzn5y5pglqta2hbtes7ekpdd4e32xbdamma",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print('Successfully sent notif:', response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending notif: {str(e)}")
        return {"error": str(e)}

def send_message(token, target, message):
    print(f"Sending message to {target}: {message}")  # Debugging
    # url = "https://dash.pushwa.com/api/kirimPesan"
    # payload = {
    #     "token": token,
    #     "target": target,
    #     "type": "text",
    #     "delay": "1",
    #     "message": message,
    # }
    url = "https://api.wa.my.id/api/v2/send/message/text"
    payload = {
        "to": target,
        "isgroup": False,
        "messages": message
    }
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        resultStatus = response.raise_for_status()
        print(f"result status: {response.json()}")
        # send_notif(target, message)
        return response.json()  # Mengembalikan respons dari API
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {str(e)}")
        return {"error": str(e)}
    
def send_notification_via_websocket(message):  
    print(f"Sending WebSocket notification: {message}")  # Debugging  
    socketio.emit('notification', {'message': message}, broadcast=True)
    

def getMessage(message):  
    print(f"Message from wa.my.id: {message}")  # Debugging  
    # socketio.emit('notification', {'message': message}, broadcast=True)