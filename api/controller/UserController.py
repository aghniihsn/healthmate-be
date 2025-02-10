from flask import request
from api import response
from api.index import app, db
# from flask_socketio import SocketIO, emit  

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from datetime import datetime, timedelta
from api.model.user import User

def singleObject(data):
    return {
        "user_id": data.user_id,
        "name": data.name,
        "email": data.email,
        "phone_number": data.phone_number,
        "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return response.BadRequest([], "Email dan Password wajib diisi!")

        user = User.query.filter_by(email=email).first()

        if not user:
            return response.BadRequest([], "Email tidak terdaftar")

        if not user.checkPassword(password):
            return response.BadRequest([], "Kombinasi email dan password salah")

        data_user = singleObject(user)
        data_user['user_id'] = user.user_id

        access_token = create_access_token(identity=data_user, fresh=True, expires_delta=timedelta(days=7))
        refresh_token = create_refresh_token(identity=data_user, expires_delta=timedelta(days=7))
        return response.success({
            "data": data_user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, "Berhasil login!")
    except Exception as e:
        print(f"Error saat login: {e}")
        return response.error([], "Gagal login")

@jwt_required()
def getUserProfile():
    try:
        current_user = get_jwt_identity()
        return response.success(current_user, "User berhasil di-autentikasi")
    except Exception as e:
        print(f"Error: {e}")
        return response.error([], "Terjadi kesalahan saat mengambil profil user", 500)

def registerUser():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not all([name, email, phone_number, password]):
            return response.BadRequest([], "Semua field harus diisi!")

        if User.query.filter_by(email=email).first():
            return response.BadRequest([], "Email sudah digunakan!")

        if User.query.filter_by(phone_number=phone_number).first():
            return response.BadRequest([], "Nomor telepon sudah digunakan!")

        new_user = User(name=name, email=email, phone_number=phone_number)
        new_user.setPassword(password)

        db.session.add(new_user)
        db.session.commit()

        return response.success(singleObject(new_user), "User berhasil didaftarkan!")
    except Exception as e:
        print(f"Error saat mendaftarkan user: {e}")
        return response.error([], "Gagal mendaftarkan user")

    
def getAllUsers():
    try:
        # users = User.query.all()
        # if not users:
        #     return response.success([], "Tidak ada user yang ditemukan")

        # users_data = [singleObject(user) for user in users]
        # return response.success(users_data, "Berhasil mendapatkan semua user")
        results = (
            db.session.query(User)
            .all()
        )

        data = []
        for user in results:
            data.append({
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
            })

        return response.success(data, 'Sukses Mengambil Data')
    except Exception as e:
        print(f"Error saat mendapatkan semua user: {e}")
        return response.error([], "Gagal mendapatkan semua user", 500)

def updateProfile():
    print("update profile")

    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone_number = data.get("phone_number")

        user = User.query.filter_by(email=email).first()

        if not user:
            return response.BadRequest([], "User tidak ditemukan!")

        if not all([name, phone_number]):
            return response.BadRequest([], "Nama dan nomor telepon wajib diisi!")

        user.name = name
        user.phone_number = phone_number

        db.session.commit()
        return response.success(singleObject(user), "Profil berhasil diperbarui!")

    except Exception as e:
        print(f"Error saat memperbarui profil: {e}")
        return response.error([], "Gagal memperbarui profil", 500)