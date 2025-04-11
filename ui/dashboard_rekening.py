# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboard_rekening.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dashboard_rekening_sakapeung(object):
    def setupUi(self, dashboard_rekening_sakapeung):
        dashboard_rekening_sakapeung.setObjectName("dashboard_rekening_sakapeung")
        dashboard_rekening_sakapeung.resize(1280, 766)
        dashboard_rekening_sakapeung.setMaximumSize(QtCore.QSize(1280, 766))
        dashboard_rekening_sakapeung.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6a11cb, stop:1 #2575fc);\n"
"")
        self.centralwidget = QtWidgets.QWidget(dashboard_rekening_sakapeung)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_utama = QtWidgets.QFrame(self.centralwidget)
        self.frame_utama.setGeometry(QtCore.QRect(-10, -5, 1301, 771))
        self.frame_utama.setStyleSheet("background-color: rgba(255, 255, 255, 180); /* Transparansi */\n"
"border-radius: 15px; /* Membuat sudut melengkung */")
        self.frame_utama.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_utama.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_utama.setObjectName("frame_utama")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_utama)
        self.stackedWidget.setGeometry(QtCore.QRect(300, 0, 991, 781))
        self.stackedWidget.setStyleSheet("background : white;")
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stackedWidget.setObjectName("stackedWidget")
        self.rekening = QtWidgets.QWidget()
        self.rekening.setObjectName("rekening")
        self.label_2 = QtWidgets.QLabel(self.rekening)
        self.label_2.setGeometry(QtCore.QRect(-294, 2, 1291, 781))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("ui/dashboard_rekening.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.rekening)
        self.lihat_informasi_rekening = QtWidgets.QWidget()
        self.lihat_informasi_rekening.setObjectName("lihat_informasi_rekening")
        self.lihat_informasi_rekening_rekening = QtWidgets.QTextEdit(self.lihat_informasi_rekening)
        self.lihat_informasi_rekening_rekening.setGeometry(QtCore.QRect(70, 390, 841, 281))
        self.lihat_informasi_rekening_rekening.setStyleSheet("background : white;\n"
"border-radius: 10px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;")
        self.lihat_informasi_rekening_rekening.setObjectName("lihat_informasi_rekening_rekening")
        self.pin_konfirmasi_LIR_input = QtWidgets.QLineEdit(self.lihat_informasi_rekening)
        self.pin_konfirmasi_LIR_input.setGeometry(QtCore.QRect(130, 210, 731, 51))
        self.pin_konfirmasi_LIR_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.pin_konfirmasi_LIR_input.setText("")
        self.pin_konfirmasi_LIR_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin_konfirmasi_LIR_input.setObjectName("pin_konfirmasi_LIR_input")
        self.submit_pin_LIR = QtWidgets.QPushButton(self.lihat_informasi_rekening)
        self.submit_pin_LIR.setGeometry(QtCore.QRect(640, 290, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.submit_pin_LIR.setFont(font)
        self.submit_pin_LIR.setStyleSheet("QPushButton {\n"
"    background-color: rgb(44, 181, 255);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 14pt; \n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"")
        self.submit_pin_LIR.setObjectName("submit_pin_LIR")
        self.label_3 = QtWidgets.QLabel(self.lihat_informasi_rekening)
        self.label_3.setGeometry(QtCore.QRect(-294, 2, 1291, 771))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("ui/dashboard_rekening_pin.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.lihat_informasi_rekening_rekening.raise_()
        self.pin_konfirmasi_LIR_input.raise_()
        self.submit_pin_LIR.raise_()
        self.stackedWidget.addWidget(self.lihat_informasi_rekening)
        self.edit_informasi_rekening = QtWidgets.QWidget()
        self.edit_informasi_rekening.setObjectName("edit_informasi_rekening")
        self.pin_konfirmasi_no_rekening_input = QtWidgets.QLineEdit(self.edit_informasi_rekening)
        self.pin_konfirmasi_no_rekening_input.setGeometry(QtCore.QRect(90, 120, 801, 51))
        self.pin_konfirmasi_no_rekening_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.pin_konfirmasi_no_rekening_input.setText("")
        self.pin_konfirmasi_no_rekening_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin_konfirmasi_no_rekening_input.setObjectName("pin_konfirmasi_no_rekening_input")
        self.submit_ganti_nomor_rekening = QtWidgets.QPushButton(self.edit_informasi_rekening)
        self.submit_ganti_nomor_rekening.setGeometry(QtCore.QRect(670, 270, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.submit_ganti_nomor_rekening.setFont(font)
        self.submit_ganti_nomor_rekening.setStyleSheet("QPushButton {\n"
"    background-color: rgb(44, 181, 255);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 12pt; \n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"")
        self.submit_ganti_nomor_rekening.setObjectName("submit_ganti_nomor_rekening")
        self.nomor_rekening_baru_input = QtWidgets.QLineEdit(self.edit_informasi_rekening)
        self.nomor_rekening_baru_input.setGeometry(QtCore.QRect(90, 200, 811, 51))
        self.nomor_rekening_baru_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.nomor_rekening_baru_input.setText("")
        self.nomor_rekening_baru_input.setObjectName("nomor_rekening_baru_input")
        self.pin_baru_input = QtWidgets.QLineEdit(self.edit_informasi_rekening)
        self.pin_baru_input.setGeometry(QtCore.QRect(90, 490, 801, 61))
        self.pin_baru_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.pin_baru_input.setText("")
        self.pin_baru_input.setObjectName("pin_baru_input")
        self.konfirmasi_pin_baru_input = QtWidgets.QLineEdit(self.edit_informasi_rekening)
        self.konfirmasi_pin_baru_input.setGeometry(QtCore.QRect(90, 580, 801, 51))
        self.konfirmasi_pin_baru_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.konfirmasi_pin_baru_input.setText("")
        self.konfirmasi_pin_baru_input.setObjectName("konfirmasi_pin_baru_input")
        self.pin_konfirmasi_pin_input = QtWidgets.QLineEdit(self.edit_informasi_rekening)
        self.pin_konfirmasi_pin_input.setGeometry(QtCore.QRect(90, 410, 801, 51))
        self.pin_konfirmasi_pin_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.pin_konfirmasi_pin_input.setText("")
        self.pin_konfirmasi_pin_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin_konfirmasi_pin_input.setObjectName("pin_konfirmasi_pin_input")
        self.submit_ganti_pin = QtWidgets.QPushButton(self.edit_informasi_rekening)
        self.submit_ganti_pin.setGeometry(QtCore.QRect(670, 650, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.submit_ganti_pin.setFont(font)
        self.submit_ganti_pin.setStyleSheet("QPushButton {\n"
"    background-color: rgb(44, 181, 255);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 14pt; \n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"")
        self.submit_ganti_pin.setObjectName("submit_ganti_pin")
        self.label_5 = QtWidgets.QLabel(self.edit_informasi_rekening)
        self.label_5.setGeometry(QtCore.QRect(-294, 2, 1291, 771))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("ui/dashboard_rekening_edit.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_5.raise_()
        self.pin_konfirmasi_no_rekening_input.raise_()
        self.submit_ganti_nomor_rekening.raise_()
        self.nomor_rekening_baru_input.raise_()
        self.pin_baru_input.raise_()
        self.konfirmasi_pin_baru_input.raise_()
        self.pin_konfirmasi_pin_input.raise_()
        self.submit_ganti_pin.raise_()
        self.stackedWidget.addWidget(self.edit_informasi_rekening)
        self.top_up = QtWidgets.QWidget()
        self.top_up.setObjectName("top_up")
        self.pin_konfirmasi_TU_input = QtWidgets.QLineEdit(self.top_up)
        self.pin_konfirmasi_TU_input.setGeometry(QtCore.QRect(90, 240, 731, 51))
        self.pin_konfirmasi_TU_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.pin_konfirmasi_TU_input.setText("")
        self.pin_konfirmasi_TU_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin_konfirmasi_TU_input.setObjectName("pin_konfirmasi_TU_input")
        self.submit_saldo_topup = QtWidgets.QPushButton(self.top_up)
        self.submit_saldo_topup.setGeometry(QtCore.QRect(720, 450, 201, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.submit_saldo_topup.setFont(font)
        self.submit_saldo_topup.setStyleSheet("QPushButton {\n"
"    background-color: rgb(44, 181, 255);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 14pt; \n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"")
        self.submit_saldo_topup.setObjectName("submit_saldo_topup")
        self.Saldo_topup_input = QtWidgets.QLineEdit(self.top_up)
        self.Saldo_topup_input.setGeometry(QtCore.QRect(90, 350, 801, 51))
        self.Saldo_topup_input.setStyleSheet("    border: none;\n"
"    border-radius: 0px;\n"
"    color: white;\n"
"    font-family: \'Montserrat\';\n"
"    font-weight: bold;\n"
"    font-size: 16pt; \n"
"    padding: 5px;\n"
"    background: transparent;")
        self.Saldo_topup_input.setText("")
        self.Saldo_topup_input.setObjectName("Saldo_topup_input")
        self.label_4 = QtWidgets.QLabel(self.top_up)
        self.label_4.setGeometry(QtCore.QRect(-294, 2, 1291, 771))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("ui/topup.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.pin_konfirmasi_TU_input.raise_()
        self.submit_saldo_topup.raise_()
        self.Saldo_topup_input.raise_()
        self.stackedWidget.addWidget(self.top_up)
        self.home_button = QtWidgets.QPushButton(self.frame_utama)
        self.home_button.setGeometry(QtCore.QRect(40, 180, 241, 61))
        self.home_button.setMouseTracking(True)
        self.home_button.setTabletTracking(True)
        self.home_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    text-align: left;\n"
"    border-radius: 20px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 30px;\n"
"    font-size: 14pt;    \n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 35px;\n"
"}\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QtCore.QSize(32, 32))
        self.home_button.setObjectName("home_button")
        self.lihat_informasi_rekening_button = QtWidgets.QPushButton(self.frame_utama)
        self.lihat_informasi_rekening_button.setGeometry(QtCore.QRect(40, 250, 241, 61))
        self.lihat_informasi_rekening_button.setMouseTracking(True)
        self.lihat_informasi_rekening_button.setTabletTracking(True)
        self.lihat_informasi_rekening_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    text-align: left;\n"
"    border-radius: 20px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 11pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 30px;\n"
"    font-size: 14pt;    \n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 35px;\n"
"}\n"
"\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/liatrek.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lihat_informasi_rekening_button.setIcon(icon1)
        self.lihat_informasi_rekening_button.setIconSize(QtCore.QSize(32, 32))
        self.lihat_informasi_rekening_button.setObjectName("lihat_informasi_rekening_button")
        self.edit_informasi_rekening_button = QtWidgets.QPushButton(self.frame_utama)
        self.edit_informasi_rekening_button.setGeometry(QtCore.QRect(40, 320, 241, 61))
        self.edit_informasi_rekening_button.setMouseTracking(True)
        self.edit_informasi_rekening_button.setTabletTracking(True)
        self.edit_informasi_rekening_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    text-align: left;\n"
"    border-radius: 20px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 30px;\n"
"    font-size: 14pt;    \n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 35px;\n"
"}\n"
"\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/editwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_informasi_rekening_button.setIcon(icon2)
        self.edit_informasi_rekening_button.setIconSize(QtCore.QSize(32, 32))
        self.edit_informasi_rekening_button.setObjectName("edit_informasi_rekening_button")
        self.top_up_button = QtWidgets.QPushButton(self.frame_utama)
        self.top_up_button.setGeometry(QtCore.QRect(40, 390, 241, 61))
        self.top_up_button.setMouseTracking(True)
        self.top_up_button.setTabletTracking(True)
        self.top_up_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    text-align: left;\n"
"    border-radius: 20px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 30px;\n"
"    font-size: 14pt;    \n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 35px;\n"
"}\n"
"\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/wallettopup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.top_up_button.setIcon(icon3)
        self.top_up_button.setIconSize(QtCore.QSize(36, 36))
        self.top_up_button.setObjectName("top_up_button")
        self.kembali_button = QtWidgets.QPushButton(self.frame_utama)
        self.kembali_button.setGeometry(QtCore.QRect(30, 640, 251, 101))
        self.kembali_button.setMouseTracking(True)
        self.kembali_button.setTabletTracking(True)
        self.kembali_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    text-align: left;\n"
"    border-radius: 20px;\n"
"    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 30px;\n"
"    font-size: 14pt;    \n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1A73E8;\n"
"    color: white; /* Warna biru Google */\n"
"    border-radius: 35px;\n"
"}\n"
"\n"
"")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/dashboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kembali_button.setIcon(icon4)
        self.kembali_button.setIconSize(QtCore.QSize(32, 32))
        self.kembali_button.setObjectName("kembali_button")
        self.label = QtWidgets.QLabel(self.frame_utama)
        self.label.setGeometry(QtCore.QRect(10, 0, 1281, 781))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("ui/0.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_utama)
        self.lineEdit.setGeometry(QtCore.QRect(40, 490, 241, 20))
        self.lineEdit.setStyleSheet("    font-family: \'Montserrat\';\n"
"    font-size: 12pt;\n"
"    font-weight: bold;")
        self.lineEdit.setObjectName("lineEdit")
        self.label.raise_()
        self.stackedWidget.raise_()
        self.home_button.raise_()
        self.lihat_informasi_rekening_button.raise_()
        self.edit_informasi_rekening_button.raise_()
        self.top_up_button.raise_()
        self.kembali_button.raise_()
        self.lineEdit.raise_()
        dashboard_rekening_sakapeung.setCentralWidget(self.centralwidget)

        self.retranslateUi(dashboard_rekening_sakapeung)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(dashboard_rekening_sakapeung)

    def retranslateUi(self, dashboard_rekening_sakapeung):
        _translate = QtCore.QCoreApplication.translate
        dashboard_rekening_sakapeung.setWindowTitle(_translate("dashboard_rekening_sakapeung", "Dashboard SAKAPEUNG"))
        self.lihat_informasi_rekening_rekening.setHtml(_translate("dashboard_rekening_sakapeung", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400;\"><br /></p></body></html>"))
        self.pin_konfirmasi_LIR_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan pin anda....."))
        self.submit_pin_LIR.setText(_translate("dashboard_rekening_sakapeung", "Submit"))
        self.pin_konfirmasi_no_rekening_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan pin anda....."))
        self.submit_ganti_nomor_rekening.setText(_translate("dashboard_rekening_sakapeung", "Ganti Nomor Rekening"))
        self.nomor_rekening_baru_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan nomor rekening anda....."))
        self.pin_baru_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan pin baru anda....."))
        self.konfirmasi_pin_baru_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan ulang pin baru anda....."))
        self.pin_konfirmasi_pin_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan pin anda....."))
        self.submit_ganti_pin.setText(_translate("dashboard_rekening_sakapeung", "Ganti Pin"))
        self.pin_konfirmasi_TU_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan pin anda....."))
        self.submit_saldo_topup.setText(_translate("dashboard_rekening_sakapeung", "SUBMIT"))
        self.Saldo_topup_input.setPlaceholderText(_translate("dashboard_rekening_sakapeung", "masukkan jumlah saldo yang akan di top up....."))
        self.home_button.setText(_translate("dashboard_rekening_sakapeung", " Home"))
        self.lihat_informasi_rekening_button.setText(_translate("dashboard_rekening_sakapeung", " Informasi Rekening"))
        self.edit_informasi_rekening_button.setText(_translate("dashboard_rekening_sakapeung", " Edit Rekening"))
        self.top_up_button.setText(_translate("dashboard_rekening_sakapeung", " Top Up Saldo"))
        self.kembali_button.setText(_translate("dashboard_rekening_sakapeung", " Dashboard Utama"))
        self.lineEdit.setText(_translate("dashboard_rekening_sakapeung", "-------------------------------------"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dashboard_rekening_sakapeung = QtWidgets.QMainWindow()
    ui = Ui_dashboard_rekening_sakapeung()
    ui.setupUi(dashboard_rekening_sakapeung)
    dashboard_rekening_sakapeung.show()
    sys.exit(app.exec_())
