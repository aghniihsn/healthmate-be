from flask import request, jsonify  
from datetime import datetime, timedelta 
# from threading import Thread  
from sqlalchemy import and_   
import time  

from api import response
from api.index import db, scheduler
from api.model.reminder import Reminder  
from api.model.notification import Notification  
from api.model.medicine import Medicine  
from api.model.user import User  
from api.model.schedule import Schedule  
from api.controller.NotifController import send_message

# def run_schedule():  
#     while True:  
#         schedule.run_pending()  
#         time.sleep(1)  

def runJobs():
    now = datetime.now()
    today_date = now.date()  # Ambil tanggal hari ini (YYYY-MM-DD)
    current_time = now.time()  # Ambil waktu sekarang (HH:MM:SS)

    # Query: Ambil jadwal dengan tanggal lebih besar dari hari ini
    # dan waktu yang lebih kecil atau sama dengan waktu sekarang
    print(f"today_date: {today_date}")
    print(f"current_time: {current_time}")
    results = db.session.query(Schedule).all()
    # .filter(
    #     and_(
    #         Schedule.schedule_end_date >= today_date,  # Hanya ambil tanggal lebih besar dari hari ini
    #         Schedule.schedule_time <= current_time  # Waktu lebih kecil atau sama dengan saat ini
    #     )
    # )
    token = "v4.public.eyJhbGlhcyI6ImFnaG5paSIsImV4cCI6IjIwMjUtMDMtMTNUMTA6NDY6MDBaIiwiaWF0IjoiMjAyNS0wMi0xMVQxMDo0NjowMFoiLCJpZCI6IjYyODE1NjQ2MDIxNzEiLCJuYmYiOiIyMDI1LTAyLTExVDEwOjQ2OjAwWiJ971RP8tu70Ztr8uSaeX5FRORzq60LkGghgmNkFBi5EyEs2zmLFhiYf5x3Cah1xKKyjaaUK2ggiCDbFHKy6MIZAg"  
      
    print(f"results: {results}")
    for schedule in results:
        try:
            user = User.query.filter_by(user_id=schedule.user_id).first()
            target = schedule.target
            message = schedule.message
            send_message(token, target, message)  # Fungsi ini harus dibuat sendiri

        except Exception as e:
            print(f"Error executing job: {e}")

    return {"status": "success", "message": f"Executed jobs at {now}"}
  
def show():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return response.error([], 'User ID diperlukan')
        
        results = (
            db.session.query(Reminder, Medicine)
            .join(Medicine, Reminder.id_medicine == Medicine.id_medicine)
            .filter(Reminder.user_id == user_id) 
            .all()
        )

        data = []
        for reminder, medicine in results:
            data.append({
                'id_reminder': reminder.id_reminder,
                'reminder_time': reminder.reminder_time.strftime('%H:%M:%S') if reminder.reminder_time else None,
                'description': reminder.description,
                'medicine_name': medicine.medicine_name,
                'dosage': medicine.dosage,
                'frequency': medicine.frequency,
                'start_date': reminder.start_date.strftime('%Y-%m-%d') if reminder.start_date else None,
                'end_date': reminder.end_date.strftime('%Y-%m-%d') if reminder.end_date else None,
            })

        return response.success(data, 'Sukses Mengambil Data')
    except Exception as e:
        print(e)
        return response.error('', 'Gagal Mengambil Data')

def detail(id):  
    try:  
        # Ambil data dari database dengan join antara Reminder dan Medicine
        result = db.session.query(Reminder, Medicine).join(Medicine, Reminder.id_medicine == Medicine.id_medicine).filter(Reminder.user_id == id).all()
        
        # Debugging: Cetak hasil ke terminal
        print(f"result: {result}")

        if not result:  
            return response.error('', 'Data tidak ditemukan')  

        # Proses data hasil query dan ubah menjadi format yang diinginkan
        data = []
        for reminder, medicine in result:
            reminder_data = {  
                'id_reminder': reminder.id_reminder,  
                'reminder_time': reminder.reminder_time.strftime('%H:%M:%S') if reminder.reminder_time else None,
                'description': reminder.description,  
                'medicine_name': medicine.medicine_name,  
                'dosage': medicine.dosage,  
                'frequency': medicine.frequency,  
                'start_date': reminder.start_date.strftime('%Y-%m-%d') if reminder.start_date else None,
                'end_date': reminder.end_date.strftime('%Y-%m-%d') if reminder.end_date else None,
            }
            data.append(reminder_data)

        # Debugging: Cetak data yang sudah diproses
        print(f"Processed data: {data}")
  
        return response.success(data, 'Sukses Mengambil Detail Data')  
  
    except Exception as e:  
        print(e)  
        return response.error('', 'Gagal Mengambil Detail Data')


def combine_date_time(date_str, time_str):
    try:
        combined = f"{date_str} {time_str}"
        result = datetime.strptime(combined, "%Y-%m-%d %H:%M:%S")
        return result
    except ValueError as e:
        print(f"Error combining date and time: {e}")
        return None

def history(user_id):  
    try:  
        results = (
            db.session.query(Reminder, Medicine)
            .join(Medicine, Reminder.id_medicine == Medicine.id_medicine)
            .filter(Reminder.user_id == user_id)
            .all()
        )        
        print(f"result: {results}")

        if not results:  
            return response.error('', 'Data tidak ditemukan')  

        current_datetime = datetime.now()

        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        today = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")

        data = []
        for reminder, medicine in results:
            threshold_datetime = combine_date_time(reminder.end_date, reminder.reminder_time)
            
            if not threshold_datetime:
                continue

            print(f"threshold_datetime: {threshold_datetime}")
            print(f"threshold_datetime: {today}")

            if threshold_datetime > today:
                continue

            reminder_data = {  
                'id_reminder': reminder.id_reminder,  
                'reminder_time': reminder.reminder_time.strftime('%H:%M:%S') if reminder.reminder_time else None,
                'description': reminder.description,  
                'medicine_name': medicine.medicine_name,  
                'dosage': medicine.dosage,  
                'frequency': medicine.frequency,  
                'start_date': reminder.start_date.strftime('%Y-%m-%d') if reminder.start_date else None,
                'end_date': reminder.end_date.strftime('%Y-%m-%d') if reminder.end_date else None,
            }
            data.append(reminder_data)

        print(f"Processed data: {data}")
  
        return response.success(data, 'Sukses Mengambil Detail Data')  
  
    except Exception as e:  
        print(e)  
        return response.error('', 'Gagal Mengambil Detail Data')

def schedule_reminders(end_date, reminder_time, frequency, token, target, message, id_reminder, user_id):  
    # interval = 24 * 60 // frequency  
    # for i in range(frequency):  
    #     reminder_datetime = reminder_time + timedelta(minutes=i * interval)  
    #     print(f"Scheduling message for {reminder_datetime}")  
    user = User.query.filter_by(user_id=user_id).first()
    schedule_time_mysql = datetime.strptime(reminder_time, '%H:%M:%S')  
    schedule_time = reminder_time[:5]
    print(f"Scheduling message for {schedule_time}")  
    try:
        medicine = Notification(  
            message=message, 
            id_reminder=id_reminder, 
            user_id=user_id  
        )  
        db.session.add(medicine)  
        db.session.commit()
        schedule = Schedule(  
            message=message,
            token=token,
            target=target, 
            schedule_time=schedule_time_mysql,
            schedule_end_date=end_date,
            user_id=user_id  
        )  
        db.session.add(schedule)  
        db.session.commit()

        scheduler.add_job(
            lambda:send_message(token, target, message), 
            "cron", 
            hour=schedule_time.split(':')[0], 
            minute=schedule_time.split(':')[1],
            id=str(id_reminder), 
        )  
        
    except Exception as e:  
        print(e)  
        db.session.rollback()  

def save():  
    try:  
        data = request.json  
        reminder_time_str = data.get('reminder_time')  
        description = data.get('description')      
        frequency = int(data.get('frequency'))    
        user_id = data.get('user_id')  
  
        if user_id is None:  
            return jsonify({"status": "error", "message": "User Id is missing"}), 404  
  
        user = User.query.get(user_id)  
        if user is None:  
            return jsonify({"status": "error", "message": "User not found"}), 404  
  
        reminder_time = datetime.strptime(reminder_time_str, '%H:%M:%S')  
        message = "Ini adalah pesan dari Health Mate -- Waktunya Minum Obat Jangan Sampai Terlambat!"    
        token = "v4.public.eyJhbGlhcyI6ImFnaG5paSIsImV4cCI6IjIwMjUtMDMtMTNUMTA6NDY6MDBaIiwiaWF0IjoiMjAyNS0wMi0xMVQxMDo0NjowMFoiLCJpZCI6IjYyODE1NjQ2MDIxNzEiLCJuYmYiOiIyMDI1LTAyLTExVDEwOjQ2OjAwWiJ971RP8tu70Ztr8uSaeX5FRORzq60LkGghgmNkFBi5EyEs2zmLFhiYf5x3Cah1xKKyjaaUK2ggiCDbFHKy6MIZAg"  
        target = user.phone_number
  
        medicine = Medicine(  
            medicine_name=data.get('medicine_name'),  
            dosage=data.get('dosage'),  
            frequency=frequency,  
            user_id=user_id  
        )  
        db.session.add(medicine)  
        db.session.commit()    
  
        reminder = Reminder(  
            reminder_time=reminder_time,  
            start_date=data.get('start_date'),  
            end_date=data.get('end_date'),  
            description=description,  
            id_medicine=medicine.id_medicine,
            user_id=user_id  
        )  
        db.session.add(reminder)


        db.session.commit()  
  
        print(f"result message for {reminder.id_reminder}")  
        schedule_reminders(data.get('end_date'), reminder_time_str, frequency, token, target, message, reminder.id_reminder, user_id)  
  
        return jsonify({"status": "success", "message": "Sukses Menambahkan Data Reminder dan Medicine"})  
    except Exception as e:  
        print(e)  
        db.session.rollback()  
        return jsonify({"status": "error", "message": "Gagal Menambahkan Data Reminder dan Medicine"})  

def ubah(id_reminder):    
    try:    
        data = request.json    
        reminder = Reminder.query.filter_by(id_reminder=id_reminder).first()    
        if not reminder:    
            return jsonify({"status": "error", "message": "Data Reminder tidak ditemukan"}), 404    

        medicine = Medicine.query.filter_by(id_medicine=reminder.id_medicine).first()    
        if not medicine:    
            return jsonify({"status": "error", "message": "Data Medicine tidak ditemukan"}), 404    

        reminder_time_str = data.get('reminder_time')    
        description = data.get('description')    
        medicine_name = data.get('medicine_name')    
        dosage = data.get('dosage')    
        frequency = int(data.get('frequency')) if data.get('frequency') else medicine.frequency    
        start_date = data.get('start_date')    
        end_date = data.get('end_date')    

        if reminder_time_str:    
            reminder.reminder_time = datetime.strptime(reminder_time_str, '%H:%M:%S')    
        if description:    
            reminder.description = description    
        if start_date:    
            reminder.start_date = start_date 
        if end_date:    
            reminder.end_date = end_date   

        if medicine_name:    
            medicine.medicine_name = medicine_name    
        if dosage:    
            medicine.dosage = dosage    
        if frequency:    
            medicine.frequency = frequency    

        # Update the reminder and medicine in the database  
        db.session.commit()

        # Reschedule reminders if necessary  
        if reminder_time_str or frequency:    
            token = "v4.public.eyJhbGlhcyI6IkFyaSIsImV4cCI6IjIwMjUtMDMtMTJUMTA6NTI6MzlaIiwiaWF0IjoiMjAyNS0wMi0xMFQxMDo1MjozOVoiLCJpZCI6IjYyODU4NTIzMTU1OTAiLCJuYmYiOiIyMDI1LTAyLTEwVDEwOjUyOjM5WiJ9w8vKTFN-VsjDlojf2iq2M3Nu5mb-7M6FiJAdpSZ6gec2dDmF7g8zoi7zpU0TV8aBxgiMgb7pTZNbaegBLdBCDw"    
            target = User.query.get(reminder.user_id).phone_number    
            message = "Ini adalah pesan dari Health Mate -- Waktunya Minum Obat Jangan Sampai Terlambat!"  

            schedule.clear(id_reminder)  # Clear the existing schedule  
            schedule_reminders(end_date, reminder_time_str, frequency, token, target, message, id_reminder, reminder.user_id)    

        return jsonify({"status": "success", "message": "Sukses Mengupdate Data Reminder dan Medicine"})    

    except Exception as e:    
        print(f"Error saat mengupdate data: {e}")    
        db.session.rollback()    
        return jsonify({"status": "error", "message": "Gagal Mengupdate Data Reminder dan Medicine"})
    
def hapus(id_reminder):  
    try:  
        reminder = Reminder.query.filter_by(id_reminder=id_reminder).first()  
        if not reminder:  
            return response.error('', 'Data Reminder tidak ditemukan')  
  
        medicine = Medicine.query.filter_by(id_medicine=reminder.id_medicine).first()  
        if not medicine:  
            return response.error('', 'Data Medicine tidak ditemukan')  
  
        db.session.delete(reminder)  
        db.session.delete(medicine)  
        db.session.commit()  
  
        return response.success('', 'Sukses Menghapus Data Reminder dan Medicine')  
    except Exception as e:  
        print(e)  
        db.session.rollback()  
        return response.error('', 'Gagal Menghapus Data Reminder dan Medicine')  
