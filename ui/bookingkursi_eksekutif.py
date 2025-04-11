# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bookingkursi_eksekutif.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_kereta_eksekutif(object):
    def setupUi(self, kereta_eksekutif):
        kereta_eksekutif.setObjectName("kereta_eksekutif")
        kereta_eksekutif.resize(1280, 766)
        kereta_eksekutif.setMaximumSize(QtCore.QSize(1280, 766))
        kereta_eksekutif.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6a11cb, stop:1 #2575fc);\n"
"")
        self.kereta_box = QtWidgets.QFrame(kereta_eksekutif)
        self.kereta_box.setGeometry(QtCore.QRect(50, 30, 1181, 711))
        self.kereta_box.setStyleSheet("background-color: rgba(255, 255, 255, 150); /* Transparansi */\n"
"border-radius: 15px; /* Membuat sudut melengkung */\n"
"")
        self.kereta_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.kereta_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.kereta_box.setObjectName("kereta_box")
        self.kursi_kereta_box = QtWidgets.QWidget(self.kereta_box)
        self.kursi_kereta_box.setGeometry(QtCore.QRect(60, 80, 1051, 611))
        self.kursi_kereta_box.setStyleSheet("background : white;")
        self.kursi_kereta_box.setObjectName("kursi_kereta_box")
        self.scrollArea_kursi = QtWidgets.QScrollArea(self.kursi_kereta_box)
        self.scrollArea_kursi.setGeometry(QtCore.QRect(120, 70, 781, 421))
        self.scrollArea_kursi.setWidgetResizable(True)
        self.scrollArea_kursi.setObjectName("scrollArea_kursi")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 781, 421))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.widget_container_kursi = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.widget_container_kursi.setGeometry(QtCore.QRect(110, 10, 111, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_container_kursi.sizePolicy().hasHeightForWidth())
        self.widget_container_kursi.setSizePolicy(sizePolicy)
        self.widget_container_kursi.setObjectName("widget_container_kursi")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_container_kursi)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.scrollArea_kursi.setWidget(self.scrollAreaWidgetContents_2)
        self.frame_data_kereta = QtWidgets.QFrame(self.kursi_kereta_box)
        self.frame_data_kereta.setGeometry(QtCore.QRect(120, 10, 781, 51))
        self.frame_data_kereta.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_data_kereta.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_data_kereta.setObjectName("frame_data_kereta")
        self.pilih_gerbong = QtWidgets.QPushButton(self.frame_data_kereta)
        self.pilih_gerbong.setGeometry(QtCore.QRect(450, 10, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.pilih_gerbong.setFont(font)
        self.pilih_gerbong.setObjectName("pilih_gerbong")
        self.comboBox = QtWidgets.QComboBox(self.frame_data_kereta)
        self.comboBox.setGeometry(QtCore.QRect(675, 9, 91, 41))
        self.comboBox.setObjectName("comboBox")
        self.nama_kereta = QtWidgets.QLabel(self.frame_data_kereta)
        self.nama_kereta.setGeometry(QtCore.QRect(20, 5, 261, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nama_kereta.setFont(font)
        self.nama_kereta.setAlignment(QtCore.Qt.AlignCenter)
        self.nama_kereta.setObjectName("nama_kereta")
        self.button_pilihkursi = QtWidgets.QPushButton(self.kursi_kereta_box)
        self.button_pilihkursi.setGeometry(QtCore.QRect(30, 510, 991, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.button_pilihkursi.setFont(font)
        self.button_pilihkursi.setStyleSheet("QPushButton {\n"
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
        self.button_pilihkursi.setObjectName("button_pilihkursi")
        self.button_keluar = QtWidgets.QPushButton(self.kursi_kereta_box)
        self.button_keluar.setGeometry(QtCore.QRect(30, 560, 991, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.button_keluar.setFont(font)
        self.button_keluar.setStyleSheet("QPushButton {\n"
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
        self.button_keluar.setObjectName("button_keluar")
        self.label_pilih_kursi = QtWidgets.QLabel(self.kereta_box)
        self.label_pilih_kursi.setGeometry(QtCore.QRect(60, 10, 1041, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_pilih_kursi.setFont(font)
        self.label_pilih_kursi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pilih_kursi.setObjectName("label_pilih_kursi")
        self.label_5 = QtWidgets.QLabel(kereta_eksekutif)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 1611, 771))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("ui/3.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_5.raise_()
        self.kereta_box.raise_()

        self.retranslateUi(kereta_eksekutif)
        QtCore.QMetaObject.connectSlotsByName(kereta_eksekutif)

    def retranslateUi(self, kereta_eksekutif):
        _translate = QtCore.QCoreApplication.translate
        kereta_eksekutif.setWindowTitle(_translate("kereta_eksekutif", "Dialog"))
        self.pilih_gerbong.setText(_translate("kereta_eksekutif", "PILIH GERBONG KERETA "))
        self.nama_kereta.setText(_translate("kereta_eksekutif", "NAMA KERETA"))
        self.button_pilihkursi.setText(_translate("kereta_eksekutif", "PILIH"))
        self.button_keluar.setText(_translate("kereta_eksekutif", "KELUAR"))
        self.label_pilih_kursi.setText(_translate("kereta_eksekutif", "PILIH KURSI ANDA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    kereta_eksekutif = QtWidgets.QDialog()
    ui = Ui_kereta_eksekutif()
    ui.setupUi(kereta_eksekutif)
    kereta_eksekutif.show()
    sys.exit(app.exec_())
