"""
Author: Roufiel Hadi
NIM: 241524028
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import json
import re
from PyQt5.QtWidgets import QMainWindow, QMessageBox  # Import QMessageBox juga
from ui.register import Ui_Register  # Pastikan path ini benar
from databases.databases import hash_password, USER_DATABASE, PAYMENT_DATABASE    # Jika ada di databases.py

class RegisterScreen(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_Register()
        self.ui.setupUi(self)

        # Hubungkan tombol dengan fungsinya
        self.ui.submit_data.clicked.connect(self.register_user)
        self.ui.login.clicked.connect(self.goto_login)

    def register_user(self):
        """Menyimpan data user baru ke database JSON dengan validasi format."""
        email = self.ui.email_input.text().strip()
        password = self.ui.password_input.text().strip()
        nama = self.ui.nama_input.text().strip().title()  # Nama diawali huruf kapital
        alamat = self.ui.alamat_input.text().strip()
        nomor_telepon = self.ui.nomor_telepon_input.text().strip()
        nomor_rekening = self.ui.nomor_rekening_input.text().strip()
        saldo_text = self.ui.saldo_input.text().strip()
        pin = self.ui.pin_input.text().strip()

        # Validasi input
        if not all([email, password, nama, alamat, nomor_telepon, nomor_rekening, saldo_text, pin]):
            return self.show_warning("Semua kolom harus diisi!")

        if not self.is_valid_email(email):
            return self.show_warning("Format email tidak valid!")
        if not self.is_valid_password(password):
            return self.show_warning("Password harus minimal 8 karakter, mengandung 1 huruf besar, 1 angka, dan 1 simbol!")
        if not self.is_valid_phone(nomor_telepon):
            return self.show_warning("Nomor telepon harus terdiri dari 11-13 digit dan diawali dengan '08'!")
        if not self.is_valid_account_number(nomor_rekening):
            return self.show_warning("Nomor rekening harus terdiri dari 10-16 digit angka!")
        if not self.is_valid_pin(pin):
            return self.show_warning("PIN harus terdiri dari 6 angka!")
        try:
            saldo = float(saldo_text)
            if saldo <= 0:
                raise ValueError
        except ValueError:
            return self.show_warning("Saldo harus berupa angka positif!")

        if self.is_email_registered(email):
            return self.show_warning("Email sudah digunakan! Silakan gunakan email lain.")

        # Simpan data pengguna
        user_data = {
            "email": email,
            "password": hash_password(password),
            "nama_lengkap": nama,
            "alamat": alamat,
            "nomor_telepon": nomor_telepon,
            "is_admin": False
        }
        self.save_to_json(USER_DATABASE, user_data)

        payment_data = {
            "email": email,
            "nomor_rekening": nomor_rekening,
            "saldo": saldo,
            "pin": hash_password(pin)
        }
        self.save_to_json(PAYMENT_DATABASE, payment_data)

        QMessageBox.information(self, "Sukses", "Registrasi berhasil! Silakan login.")
        self.goto_login()

    def show_warning(self, message):
        """Menampilkan pesan peringatan."""
        QMessageBox.warning(self, "Peringatan", message)

    def is_valid_email(self, email):
        """Memeriksa apakah format email valid."""
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

    def is_valid_password(self, password):
        """Memeriksa apakah password memenuhi syarat keamanan."""
        return re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password)

    def is_valid_phone(self, phone):
        """Memeriksa apakah nomor telepon sesuai format."""
        return re.fullmatch(r"08\d{9,11}", phone)

    def is_valid_account_number(self, account):
        """Memeriksa apakah nomor rekening sesuai format."""
        return account.isdigit() and 10 <= len(account) <= 16

    def is_valid_pin(self, pin):
        """Memeriksa apakah PIN terdiri dari 6 angka."""
        return re.fullmatch(r"\d{6}", pin)

    def is_email_registered(self, email):
        """Memeriksa apakah email sudah terdaftar."""
        return any(user["email"] == email for user in self.load_users())

    def load_users(self):
        """Memuat data pengguna dari file JSON."""
        return self.load_json(USER_DATABASE)

    def save_to_json(self, filename, data):
        """Menyimpan data ke dalam file JSON."""
        existing_data = self.load_json(filename)
        existing_data.append(data)
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)

    def load_json(self, filename):
        """Memuat data dari file JSON."""
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def goto_login(self):
        """Kembali ke menu login."""
        self.main_app.setCurrentWidget(self.main_app.login_screen)