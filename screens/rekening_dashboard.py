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
from ui.dashboard_rekening import Ui_dashboard_rekening_sakapeung as Ui_dashboard_rekening  # Pastikan path ini benar
from databases.databases import hash_password, PAYMENT_DATABASE    # Jika ada di databases.py

class RekeningDashboard(QMainWindow):
    """
    Kelas untuk menangani tampilan dan fungsi Dashboard Rekening.
    User dapat melihat saldo, mengganti nomor rekening, mengganti PIN, dan melakukan top-up saldo.
    """

    def __init__(self, main_app):
        """Inisialisasi dashboard rekening dan menghubungkan tombol dengan fungsi masing-masing."""
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_dashboard_rekening()
        self.ui.setupUi(self)

        self.setup_connections()

    def setup_connections(self):
        """Menghubungkan tombol dengan fungsi navigasi dan aksi pengguna."""
        # Navigasi antar halaman
        self.ui.home_button.clicked.connect(self.show_home)
        self.ui.lihat_informasi_rekening_button.clicked.connect(self.show_lihat_saldo)
        self.ui.edit_informasi_rekening_button.clicked.connect(self.show_edit_rekening)
        self.ui.top_up_button.clicked.connect(self.show_top_up)
        self.ui.kembali_button.clicked.connect(self.goto_dashboard_user)

        # Aksi perubahan data rekening
        self.ui.submit_pin_LIR.clicked.connect(self.lihat_informasi_rekening)
        self.ui.submit_ganti_nomor_rekening.clicked.connect(self.ganti_nomor_rekening)
        self.ui.submit_ganti_pin.clicked.connect(self.ganti_pin)
        self.ui.submit_saldo_topup.clicked.connect(self.top_up_saldo)

    def set_user(self, user):
        """Menyimpan informasi user aktif."""
        self.user = user

    # ======================== Navigasi Dashboard Rekening ========================

    def show_home(self):
        """Menampilkan halaman utama Dashboard Rekening."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.rekening)

    def show_lihat_saldo(self):
        """Menampilkan halaman informasi saldo rekening."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.lihat_informasi_rekening)

    def show_edit_rekening(self):
        """Menampilkan halaman edit informasi rekening."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.edit_informasi_rekening)

    def show_top_up(self):
        """Menampilkan halaman top-up saldo."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.top_up)

    def goto_dashboard_user(self):
        """Kembali ke menu Dashboard User."""
        self.main_app.setCurrentWidget(self.main_app.dashboard_user)

    # ======================== Pengelolaan Data Rekening ========================

    def load_payments(self):
        """Memuat data rekening dari file JSON."""
        try:
            with open(PAYMENT_DATABASE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_payments(self, payments):
        """Menyimpan data rekening ke file JSON."""
        with open(PAYMENT_DATABASE, "w") as file:
            json.dump(payments, file, indent=4)

    def lihat_informasi_rekening(self):
        """Menampilkan informasi rekening setelah verifikasi PIN."""
        pin_input = self.ui.pin_konfirmasi_LIR_input.text().strip()
        payments = self.load_payments()

        for payment in payments:
            if payment["email"] == self.main_app.current_user["email"] and payment["pin"] == hash_password(pin_input):
                info = f"""
                Nomor Rekening : {payment["nomor_rekening"]}
                Saldo          : Rp{payment["saldo"]}
                """
                self.ui.lihat_informasi_rekening_rekening.setPlainText(info)
                return
        QMessageBox.warning(self, "Error", "PIN salah atau rekening tidak ditemukan!")

    def ganti_nomor_rekening(self):
        """Mengubah nomor rekening setelah verifikasi PIN dengan validasi."""
        pin_input = self.ui.pin_konfirmasi_no_rekening_input.text().strip()
        new_rekening = self.ui.nomor_rekening_baru_input.text().strip()
        payments = self.load_payments()

        if not re.fullmatch(r"\d{10,16}", new_rekening):
            QMessageBox.warning(self, "Error", "Nomor rekening harus terdiri dari 10-16 digit angka!")
            return

        for payment in payments:
            if payment["email"] == self.main_app.current_user["email"] and payment["pin"] == hash_password(pin_input):
                payment["nomor_rekening"] = new_rekening
                self.save_payments(payments)
                QMessageBox.information(self, "Sukses", "Nomor rekening berhasil diubah!")
                return
        QMessageBox.warning(self, "Error", "PIN salah atau data tidak valid!")

    def ganti_pin(self):
        """Mengganti PIN setelah verifikasi PIN lama dengan validasi."""
        pin_input = self.ui.pin_konfirmasi_pin_input.text().strip()
        new_pin = self.ui.pin_baru_input.text().strip()
        confirm_pin = self.ui.konfirmasi_pin_baru_input.text().strip()
        payments = self.load_payments()

        if not re.fullmatch(r"\d{6}", new_pin):
            QMessageBox.warning(self, "Error", "PIN harus terdiri dari 6 angka!")
            return

        for payment in payments:
            if payment["email"] == self.main_app.current_user["email"] and payment["pin"] == hash_password(pin_input):
                if new_pin == confirm_pin:
                    payment["pin"] = hash_password(new_pin)
                    self.save_payments(payments)
                    QMessageBox.information(self, "Sukses", "PIN berhasil diubah!")
                    return
                QMessageBox.warning(self, "Error", "PIN baru tidak cocok!")
                return
        QMessageBox.warning(self, "Error", "PIN lama salah atau data tidak valid!")

    def top_up_saldo(self):
        """Menambahkan saldo setelah verifikasi PIN dengan validasi."""
        pin_input = self.ui.pin_konfirmasi_TU_input.text().strip()
        top_up_amount = self.ui.Saldo_topup_input.text().strip()
        payments = self.load_payments()

        if not top_up_amount.isdigit() or int(top_up_amount) <= 0:
            QMessageBox.warning(self, "Error", "Jumlah top-up harus berupa angka positif!")
            return

        for payment in payments:
            if payment["email"] == self.main_app.current_user["email"] and payment["pin"] == hash_password(pin_input):
                payment["saldo"] += int(top_up_amount)
                self.save_payments(payments)
                QMessageBox.information(self, "Sukses", "Saldo berhasil ditambahkan!")
                return
        QMessageBox.warning(self, "Error", "PIN salah atau data tidak valid!")