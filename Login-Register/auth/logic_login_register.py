import json
import os

from auth.validators import (
    validate_username,
    validate_email,
    validate_password
)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "users_db.json"
)


def load_users():
    if not os.path.exists(DB_PATH):
        return {}

    with open(DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def register_user(username, email, password):
    users = load_users()

    if not validate_username(username):
        return False, "Username harus 3-20 karakter"

    if not validate_email(email):
        return False, "Format email tidak valid"

    if not validate_password(password):
        return False, "Password minimal 6 karakter"

    if username in users:
        return False, "Username sudah terdaftar"

    for user in users.values():
        if user["email"] == email:
            return False, "Email sudah digunakan"

    users[username] = {
        "email": email,
        "password": password
    }

    save_users(users)

    return True, "Registrasi berhasil"


def login_user(identifier, password):
    users = load_users()

    for username, user in users.items():
        if (
            identifier == username
            or identifier == user["email"]
        ):
            if user["password"] == password:
                return True, "Login berhasil"

            return False, "Password salah"

    return False, "Username atau email tidak ditemukan"