import json
import hashlib

USER_DATABASE = "databases/user_database.json"
PAYMENT_DATABASE = "databases/payment_database.json"

def hash_password(password):
    """Menggunakan SHA-256 untuk mengenkripsi password."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(filename):
    """Memuat data dari file JSON."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(filename, data):
    """Menyimpan data ke dalam file JSON tanpa menghapus data sebelumnya."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
