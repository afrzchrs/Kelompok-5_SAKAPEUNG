"""
Author: Roufiel Hadi
NIM: 241524028
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Import UI_Welcome dari file yang sesuai
from ui.welcome import Ui_Welcome

class WelcomeScreen(QMainWindow):
    """
    Kelas untuk halaman selamat datang
    """
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_Welcome()
        self.ui.setupUi(self)

        # Membuat QLabel untuk menampilkan logo
        self.label_logo = QLabel(self)
        self.label_logo.setGeometry(QtCore.QRect(290, 50, 491, 461))  # Sesuaikan posisi dan ukuran
        self.label_logo.setStyleSheet("background:transparent;")

        # Memuat gambar dari folder icons
        pixmap = QPixmap("icons/sakapeung.png")

        self.label_logo.setPixmap(pixmap)
        self.label_logo.setScaledContents(True)  # Supaya gambar menyesuaikan ukuran label

        # Menghubungkan tombol enter dengan fungsi goto_login
        self.ui.tombol_enter_untuk_lanjut.clicked.connect(self.goto_login)

        # Atur fokus agar bisa menangkap input keyboard
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        """
        Menangani event keyboard, jika tombol Enter ditekan maka akan masuk ke halaman login
        """
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.goto_login()

    def goto_login(self):
        """
        Fungsi untuk berpindah ke halaman login
        """
        self.main_app.setCurrentWidget(self.main_app.login_screen)
        self.main_app.login_screen.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6a11cb, stop:1 #2575fc);"
        )
