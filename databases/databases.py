import json
import os
import hashlib

USER_DATABASE = "databases/user_database.json"
PAYMENT_DATABASE = "databases/payment_database.json"
INFOUMUM_DATABASE = "databases/informasi_umum.json"
JADWALKERETA_DATABASE = "databases/jadwal_kereta.json"
KURSIKERETA_DATABASE = "databases/kursi_kereta.json"
FORMATGERBONG = "databases/formatGerbong.json"

def hash_password(password):
    """Menggunakan SHA-256 untuk mengenkripsi password."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(filename):
    """Memuat data dari file JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(filename, data):
    """Menyimpan data ke dalam file JSON tanpa menghapus data sebelumnya."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def find_user_by_email(email):
    """Mencari user berdasarkan email."""
    users = load_json(USER_DATABASE)
    return next((user for user in users if user["email"] == email), None)

def update_user_data(email, key, value):
    """Memperbarui data user dalam database."""
    users = load_json(USER_DATABASE)
    for user in users:
        if user["email"] == email:
            user[key] = value
            save_json(USER_DATABASE, users)
            return True
    return False
