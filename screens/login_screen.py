from PyQt5.QtWidgets import QMainWindow, QMessageBox  # Import QMessageBox juga
from ui.login import Ui_Login  # Pastikan path ini benar
import json
from databases.databases import hash_password, USER_DATABASE   # Jika ada di databases.py


class LoginScreen(QMainWindow):
    """
    Kelas untuk halaman login pengguna
    """
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        # Hubungkan tombol ke fungsi masing-masing
        self.ui.registrasi.clicked.connect(self.goto_register)
        self.ui.masuk_ke_aplikasi.clicked.connect(self.login_user)
    
    def showEvent(self, event):
        """
        Mengatur background saat tampilan muncul
        """
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6a11cb, stop:1 #2575fc);")
        event.accept()
    
    def goto_register(self):
        """
        Berpindah ke halaman registrasi
        """
        self.main_app.setCurrentWidget(self.main_app.register_screen)
    
    def login_user(self):
        """
        Proses autentikasi pengguna
        """
        email = self.ui.email_input.text()
        password = hash_password(self.ui.password_input.text())
        users = self.load_users()
        user = next((u for u in users if u["email"] == email and u["password"] == password), None)

        if user:
            QMessageBox.information(self, "Sukses", f"Selamat datang, {user['nama_lengkap']}!")
            self.main_app.current_user = user
            self.main_app.email_pengguna = email  # 🔥 Simpan email pengguna yang login
            
            # Cek apakah user adalah admin atau bukan
            if user["is_admin"]:
                self.main_app.dashboard_admin.set_user(user)
                self.main_app.setCurrentWidget(self.main_app.dashboard_admin)
            else:
                self.main_app.dashboard_user.set_user(user)
                self.main_app.setCurrentWidget(self.main_app.dashboard_user)
        else:
            QMessageBox.warning(self, "Error", "Email atau password salah!")
    
    def load_users(self):
        """
        Memuat daftar pengguna dari database JSON
        """
        try:
            with open(USER_DATABASE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []