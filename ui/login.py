"""
Author: Mario Julius Christianto
NIM: 241524014
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(1280, 720)
        Login.setMaximumSize(QtCore.QSize(1280, 720))
        Login.setStyleSheet("background : #92b8cf;")
        self.login = QtWidgets.QWidget(Login)
        self.login.setObjectName("login")

        self.label = QtWidgets.QLabel(self.login)
        self.label.setGeometry(QtCore.QRect(-4, -10, 1281, 691))
        self.label.setPixmap(QtGui.QPixmap("ui\login_page.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.email_input = QtWidgets.QLineEdit(self.login)
        self.email_input.setGeometry(QtCore.QRect(730, 220, 501, 71))
        self.email_input.setStyleSheet("border: 2px solid #B0C4DE; border-radius: 15px; padding: 5px; background: white; font-family: 'Montserrat'; font-size: 20px; color: #333;")
        self.email_input.setObjectName("email_input")

        self.password_input = QtWidgets.QLineEdit(self.login)
        self.password_input.setGeometry(QtCore.QRect(730, 330, 501, 71))
        self.password_input.setStyleSheet("border: 2px solid #B0C4DE; border-radius: 15px; padding-right: 50px; background: white; font-family: 'Montserrat'; font-size: 20px; color: #333;")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Default: sembunyikan password
        self.password_input.setObjectName("password_input")

        # Tombol Show/Hide Password di dalam input
        self.toggle_password_btn = QtWidgets.QPushButton(self.password_input)
        self.toggle_password_btn.setGeometry(QtCore.QRect(460, 15, 40, 40))  # Letakkan di dalam input, di ujung kanan
        self.toggle_password_btn.setStyleSheet("background: transparent; border: none;")
        self.toggle_password_btn.setIcon(QtGui.QIcon("FinalUpd(11)/ui/eye_open.png"))  # Gunakan ikon gambar
        self.toggle_password_btn.setIconSize(QtCore.QSize(30, 30))  # Perbesar ikon
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.setObjectName("toggle_password_btn")

        self.masuk_ke_aplikasi = QtWidgets.QPushButton(self.login)
        self.masuk_ke_aplikasi.setGeometry(QtCore.QRect(730, 480, 501, 71))
        self.masuk_ke_aplikasi.setStyleSheet("background-color: transparent; color: white; border-radius: 20px; font-size: 16px; font-weight: bold; padding: 10px 40px; font-family: 'Montserrat';")
        self.masuk_ke_aplikasi.setObjectName("masuk_ke_aplikasi")

        self.registrasi = QtWidgets.QPushButton(self.login)
        self.registrasi.setGeometry(QtCore.QRect(880, 560, 91, 21))
        self.registrasi.setStyleSheet("background-color: transparent; color: white; border-radius: 20px; font-size: 16px; font-weight: bold; padding: 10px 40px; font-family: 'Montserrat';")
        self.registrasi.setObjectName("registrasi")

        self.widget = QtWidgets.QWidget(self.login)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1281, 701))
        self.widget.setObjectName("widget")
        self.widget.raise_()
        self.label.raise_()
        self.email_input.raise_()
        self.password_input.raise_()
        self.masuk_ke_aplikasi.raise_()
        self.registrasi.raise_()
        self.toggle_password_btn.raise_()
        Login.setCentralWidget(self.login)

        self.menubar = QtWidgets.QMenuBar(Login)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        Login.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Login)
        self.statusbar.setObjectName("statusbar")
        Login.setStatusBar(self.statusbar)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

        # Hubungkan tombol dengan fungsi toggle
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self):
        """Mengubah mode tampilan password (show/hide)."""
        if self.toggle_password_btn.isChecked():
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)  # Tampilkan password
            self.toggle_password_btn.setIcon(QtGui.QIcon("ui\eye_close.png"))  # Ubah ikon mata tertutup
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Sembunyikan password
            self.toggle_password_btn.setIcon(QtGui.QIcon("ui\eye_open.png"))  # Ubah ikon mata terbuka

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "MainWindow"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
