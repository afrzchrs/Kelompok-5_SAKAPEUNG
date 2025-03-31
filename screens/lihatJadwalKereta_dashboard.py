"""
Author: Afriza Choirie Saputra
NIM: 241524002
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import sys
import json
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from datetime import datetime
from ui.dashboard_lihatJadwalKereta import Ui_dashboard_lihatJadwalKereta as dashboard_lihat_jadwal

INFOUMUM_DATABASE = "databases/informasi_umum.json"
JADWALKERETA_DATABASE = "databases/jadwal_kereta.json"
KURSIKERETA_DATABASE = "databases/kursi_kereta.json"

class LihatJadwalKereta(QtWidgets.QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.ui = dashboard_lihat_jadwal()
        self.ui.setupUi(self)
        self.main_app = main_app
        self.setWindowTitle("Lihat Jadwal Kereta")

        # Hubungkan tombol pencarian dengan fungsi search_train
        self.ui.tombo_search_2.clicked.connect(self.search_train)
        self.ui.tombo_search_3.clicked.connect(self.reset_table)
        
        self.setup_connections()
        self.data = []
        self.load_data()
        self.setup_table()
    
    def setup_connections(self):
        """Menghubungkan tombol dengan fungsi navigasi."""
        self.ui.home_button.clicked.connect(self.reset_and_show_home)
        self.ui.pembelian_tiket_button.clicked.connect(self.reset_and_show_pembelian_tiket)
        self.ui.lihat_jadwal_kereta_button.clicked.connect(self.reset_and_show_lihat_jadwal)
        self.ui.tiket_saya_button.clicked.connect(self.reset_and_show_tiket_saya)
        self.ui.dashboard_akun_button.clicked.connect(self.show_dashboard_akun)
        self.ui.dashboard_rekening_button.clicked.connect(self.show_dashboard_rekening)
        self.ui.keluar_button.clicked.connect(self.exit_application)
        self.ui.tombol_kembali.clicked.connect(self.goto_dashboard_user)
    
    def exit_application(self):
        """Menutup aplikasi."""
        QtWidgets.QApplication.quit()

    def reset_and_show_home(self):
        self.load_data()
        self.ui.user.setCurrentWidget(self.ui.user_dashboard)

    def reset_and_show_pembelian_tiket(self):
        self.load_data()
        self.main_app.setCurrentWidget(self.main_app.ticket_search_screen)

    def reset_and_show_lihat_jadwal(self):
        self.load_data()
        self.ui.user.setCurrentWidget(self.ui.lihat_jadwal_kereta)

    def reset_and_show_tiket_saya(self):
        self.load_data()
        self.main_app.setCurrentWidget(self.main_app.tiket_saya_screen)

    def show_dashboard_akun(self):
        self.main_app.dashboard_akun.set_user()
        self.main_app.setCurrentWidget(self.main_app.dashboard_akun)

    def show_dashboard_rekening(self):
        self.main_app.setCurrentWidget(self.main_app.dashboard_rekening)
    
    def goto_dashboard_user(self):
        """Kembali ke menu Dashboard User."""
        self.main_app.setCurrentWidget(self.main_app.dashboard_user)
    
    def reset_table(self):
        """Menghapus semua isi tabel dan memuat ulang data dari JSON."""
        self.ui.input_nama_kereta_2.clear()
        self.ui.input_stasiun_awal_2.clear()
        self.ui.input_stasiun_tujuan_2.clear()
        self.ui.tableWidget.clearContents()  
        self.ui.tableWidget.setRowCount(0)  
        self.load_data() 

    def setup_table(self):
        """Mengatur tampilan tabel dengan kolom dan ukuran yang sesuai."""
        self.ui.tableWidget.setColumnCount(6)
        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Jenis Layanan", "Stasiun Transit", "Waktu Transit"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        # Menyembunyikan header vertikal
        self.ui.tableWidget.verticalHeader().setVisible(False)

        # Menyesuaikan lebar kolom
        self.ui.tableWidget.setColumnWidth(0, 100)  # ID Kereta
        self.ui.tableWidget.setColumnWidth(1, 200)  # Nama Kereta
        self.ui.tableWidget.setColumnWidth(2, 120)  # Tanggal
        self.ui.tableWidget.setColumnWidth(3, 150)  # Jenis Layanan
        self.ui.tableWidget.setColumnWidth(4, 250)  # Stasiun Transit
        self.ui.tableWidget.setColumnWidth(5, 200)  # Waktu Transit

        # Set header agar rata tengah
        for col in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.horizontalHeaderItem(col).setTextAlignment(QtCore.Qt.AlignCenter)

        # Atur agar kolom menyesuaikan ukuran otomatis
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.resizeRowsToContents()


    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def search_kereta_by_date(self, target_date):
        kursi_data = self.load_json(KURSIKERETA_DATABASE)
        informasi_kereta = self.load_json(INFOUMUM_DATABASE)
        jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)
        
        hasil_pencarian = []
        
        for entry in kursi_data:
            if entry["tanggal"] == target_date:
                id_kereta = entry["id_kereta"]
                
                info_kereta = next((kereta for kereta in informasi_kereta if kereta["id_kereta"] == id_kereta), None)
                jadwal = next((jadwal for jadwal in jadwal_kereta if jadwal["id_kereta"] == id_kereta), None)
                gerbong = next((gerbong for gerbong in kursi_data if gerbong["id_kereta"] == id_kereta), None)
                
                if info_kereta and jadwal and gerbong:
                    hasil_pencarian.append({
                        "id_kereta": id_kereta,
                        "nama_kereta": info_kereta["nama_kereta"],
                        "jenis_layanan": info_kereta["jenis_layanan"],
                        "tanggal":gerbong["tanggal"],
                        "harga_tiket": info_kereta["harga_tiket"],
                        "stasiun_transit": jadwal["stasiun_transit"],
                        "waktu_transit": jadwal["waktu_transit"]
                    })
        if not hasil_pencarian:
            QtWidgets.QMessageBox.information(self, "Hasil Pencarian", f"Tidak ada data untuk tanggal {target_date}.")
        else:
            self.populate_table(hasil_pencarian)

    def search_kereta_by_user(self, target_date, target_nama, target_stasiun_awal, target_stasiun_akhir):
        # Pastikan minimal tanggal diisi
        if not target_date:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Harap pilih tanggal pencarian.")
            return

        # Muat data dari file JSON
        kursi_data = self.load_json(KURSIKERETA_DATABASE)
        informasi_kereta = self.load_json(INFOUMUM_DATABASE)
        jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)

        hasil_pencarian = []

        for entry in kursi_data:
            if entry["tanggal"] != target_date:
                continue  # Lewati jika tanggal tidak cocok

            id_kereta = entry["id_kereta"]
            
            info_kereta = next((kereta for kereta in informasi_kereta if kereta["id_kereta"] == id_kereta), None)
            jadwal = next((jadwal for jadwal in jadwal_kereta if jadwal["id_kereta"] == id_kereta), None)

            if not info_kereta or not jadwal:
                continue  # Lewati jika tidak ada data

            stasiun_transit = jadwal.get("stasiun_transit", [])
            if len(stasiun_transit) < 2:
                continue  # Lewati jika tidak cukup stasiun

            stasiun_awal_db = stasiun_transit[0].lower()
            stasiun_akhir_db = stasiun_transit[-1].lower()

            # **Pencarian fleksibel** (hanya filter yang diisi user)
            if (not target_nama or target_nama.lower() == info_kereta["nama_kereta"].lower()) and \
            (not target_stasiun_awal or target_stasiun_awal.lower() == stasiun_awal_db) and \
            (not target_stasiun_akhir or target_stasiun_akhir.lower() == stasiun_akhir_db):

                hasil_pencarian.append({
                    "id_kereta": id_kereta,
                    "nama_kereta": info_kereta["nama_kereta"],
                    "jenis_layanan": info_kereta["jenis_layanan"],
                    "tanggal": entry["tanggal"],
                    "harga_tiket": info_kereta["harga_tiket"],
                    "stasiun_transit": stasiun_transit,
                    "waktu_transit": jadwal.get("waktu_transit", "-")
                })

        if hasil_pencarian:
            self.populate_table(hasil_pencarian)
        else:
            QtWidgets.QMessageBox.information(self, "Hasil Pencarian", "Tidak ada data yang sesuai dengan kriteria pencarian.")

    def populate_table(self, result):
        """Mengisi tabel dengan hasil pencarian kereta berdasarkan kriteria yang diberikan."""
        self.ui.tableWidget.setRowCount(0)  

        total_rows = sum(len(kereta.get("stasiun_transit", [])) or 1 for kereta in result)
        self.ui.tableWidget.setRowCount(total_rows)

        row = 0
        for kereta in result:
            id_kereta = kereta.get("id_kereta", "-")
            nama_kereta = kereta.get("nama_kereta", "-")
            tanggal = kereta.get("tanggal", "-")
            jenis_layanan = kereta.get("jenis_layanan", "-")
            stasiun_transit = kereta.get("stasiun_transit", ["-"])
            waktu_transit = kereta.get("waktu_transit", ["-"])

            span_count = max(len(stasiun_transit), 1)  # Minimal satu baris

            # Mengisi kolom utama hanya pada baris pertama
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(tanggal))
            self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(jenis_layanan))

            # Menggabungkan sel untuk ID Kereta, Nama Kereta, Tanggal, dan Jenis Layanan
            self.ui.tableWidget.setSpan(row, 0, span_count, 1)
            self.ui.tableWidget.setSpan(row, 1, span_count, 1)
            self.ui.tableWidget.setSpan(row, 2, span_count, 1)
            self.ui.tableWidget.setSpan(row, 3, span_count, 1)

            # Mengisi kolom Stasiun Transit dan Waktu Transit
            for i in range(span_count):
                self.ui.tableWidget.setItem(row + i, 4, QtWidgets.QTableWidgetItem(stasiun_transit[i] if i < len(stasiun_transit) else "-"))
                self.ui.tableWidget.setItem(row + i, 5, QtWidgets.QTableWidgetItem(waktu_transit[i] if i < len(waktu_transit) else "-"))

            row += span_count  # Pindah ke baris berikutnya

        # Atur tampilan agar lebih rapi
        self.ui.tableWidget.resizeRowsToContents()

    def search_train(self):
        tanggal = self.ui.dateEdit_lihat_jadwal_kereta.date().toString('yyyy-MM-dd')
        nama_kereta = self.ui.input_nama_kereta_2.text().strip().lower()
        stasiun_awal = self.ui.input_stasiun_awal_2.text().strip().lower()
        stasiun_akhir = self.ui.input_stasiun_tujuan_2.text().strip().lower()
        self.search_kereta_by_user(tanggal, nama_kereta, stasiun_awal, stasiun_akhir)
    
    def load_data(self):
        today = datetime.today().strftime("%Y-%m-%d")
        self.search_kereta_by_date(today)
