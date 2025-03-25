"""
Nama: Adi Rafi Chaerufarizki
NIM: 241524001
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import sys
import os
import json
from PyQt5 import QtWidgets, uic
from ui.tiket_saya import Ui_dashboard_tiket_saya  # Pastikan path ini benar
from screens.detail_tiket_screen import DetailTiket  # Pastikan ini benar

# Lokasi file database
RIWAYAT_PEMESANAN_DATABASE = "databases/riwayat_pemesanan.json"

class TiketSaya(QtWidgets.QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Referensi ke aplikasi utama
        self.email_pengguna = self.main_app.email_pengguna
        self.ui = Ui_dashboard_tiket_saya()
        self.ui.setupUi(self)

        # Menghubungkan tombol lihat detail ke fungsi pencarian tiket
        self.ui.button_detail.clicked.connect(self.cari_dan_tampilkan_detail)
        
        # Menghubungkan tombol kembali ke fungsi kembali ke dashboard
        self.ui.button_kembali.clicked.connect(self.kembali_ke_dashboard)
        
        # Muat semua tiket tanpa filter email
        self.load_tiket()

    def load_tiket(self):
        """Memuat semua tiket tanpa filter email"""
        if not os.path.exists(RIWAYAT_PEMESANAN_DATABASE):
            QtWidgets.QMessageBox.critical(self, "Error", "Database riwayat_pemesanan.json tidak ditemukan!")
            return
        
        try:
            with open(RIWAYAT_PEMESANAN_DATABASE, "r") as file:
                data_pemesanan = json.load(file)
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.critical(self, "Error", "Database riwayat_pemesanan.json rusak atau tidak valid!")
            return

          # Filter hanya tiket yang sesuai dengan email pengguna yang login
        self.tiket_user = [tiket for tiket in data_pemesanan if tiket.get("email_penumpang") == self.main_app.email_pengguna]

        # Pastikan tabel cukup besar
        self.ui.table_tiket_saya.setRowCount(len(self.tiket_user))
        self.ui.table_tiket_saya.setColumnCount(5)
        self.ui.table_tiket_saya.setHorizontalHeaderLabels([
            "ID Kereta", "Nama Kereta", "Stasiun Asal", "Stasiun Tujuan", "Tanggal"
        ])

        for row, tiket in enumerate(self.tiket_user):
            id_kereta = str(tiket.get("id_kereta", "-"))
            nama_kereta = tiket.get("nama_kereta", "-")
            stasiun_asal = tiket.get("asal", "-")
            stasiun_tujuan = tiket.get("tujuan", "-")
            tanggal = tiket.get("tanggal", "-")
            
            self.ui.table_tiket_saya.setItem(row, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.table_tiket_saya.setItem(row, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.table_tiket_saya.setItem(row, 2, QtWidgets.QTableWidgetItem(stasiun_asal))
            self.ui.table_tiket_saya.setItem(row, 3, QtWidgets.QTableWidgetItem(stasiun_tujuan))
            self.ui.table_tiket_saya.setItem(row, 4, QtWidgets.QTableWidgetItem(tanggal))

    def cari_dan_tampilkan_detail(self):
        """Mencari tiket berdasarkan ID Kereta dan menampilkan detailnya"""
        id_kereta_input = self.ui.lineEdit.text().strip()
        
        if not id_kereta_input:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Masukkan ID Kereta terlebih dahulu!")
            return

        tiket_ditemukan = next((tiket for tiket in self.tiket_user if str(tiket["id_kereta"]) == id_kereta_input), None)
        
        if tiket_ditemukan:
            self.lihat_detail(tiket_ditemukan)
        else:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tiket tidak ditemukan!")
    

    def lihat_detail(self, tiket):
        """Menampilkan halaman detail tiket"""
        self.detail_tiket_window = DetailTiket(tiket)
        self.detail_tiket_window.show()

    def kembali_ke_dashboard(self):
        """Kembali ke dashboard utama"""
        self.main_app.setCurrentWidget(self.main_app.dashboard_user)
