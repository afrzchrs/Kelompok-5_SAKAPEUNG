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
from ui.dashboard_lihatJadwalKereta import Ui_dashboard_lihatJadwalKereta as dashboard_lihat_jadwal
from screens.tiket_saya_screen import TiketSaya

# Lokasi file database
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
        
        # Hubungkan tombol reset dengan fungsi reset table
        self.ui.tombo_search_3.clicked.connect(self.reset_table)
        
        self.setup_connections()
        # Load Data
        self.data = []
        self.load_data()
    
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
        self.ui.user.setCurrentWidget(self.ui.pembelian_tiket)

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
        
        
    def load_data(self):
        """Memuat data dari semua database JSON dengan perbaikan error handling"""
        combined_data = {}

        for db_path in [INFOUMUM_DATABASE, JADWALKERETA_DATABASE, KURSIKERETA_DATABASE]:
            if not os.path.exists(db_path):
                QtWidgets.QMessageBox.critical(self, "Error", f"Database {db_path} tidak ditemukan.")
                return
            
            try:
                with open(db_path, "r") as file:
                    data = json.load(file)
                    for kereta in data:
                        id_kereta = kereta.get("id_kereta")
                        if id_kereta:
                            if id_kereta not in combined_data:
                                combined_data[id_kereta] = {}
                            combined_data[id_kereta].update(kereta)
            except json.JSONDecodeError:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database {db_path} rusak atau tidak dapat dibaca.")
                return
        
        self.data = list(combined_data.values())
        self.populate_table(self.data)
    
    def reset_table(self):
        """Menghapus semua isi tabel dan memuat ulang data dari JSON."""
        self.ui.input_nama_kereta_2.clear()
        self.ui.input_stasiun_awal_2.clear()
        self.ui.input_stasiun_tujuan_2.clear()
        self.ui.tableWidget.clearContents()  
        self.ui.tableWidget.setRowCount(0)  
        self.load_data() 
        
    def populate_table(self, data):
        """Mengisi tabel dengan data kereta, menampilkan stasiun dan waktu transit dalam format vertikal."""
        
        # Hitung total baris yang diperlukan (setiap stasiun transit membutuhkan satu baris)
        total_rows = sum(len(kereta.get("stasiun_transit", [])) or 1 for kereta in data)

        self.ui.tableWidget.setRowCount(total_rows)
        self.ui.tableWidget.setColumnCount(6)  # 6 Kolom: ID, Nama, Tanggal, Jenis Layanan, Stasiun, Waktu

        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Jenis Layanan", "Stasiun Transit", "Waktu Transit"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget.verticalHeader().setVisible(False)

        row = 0
        for kereta in data:
            id_kereta = kereta.get("id_kereta", "-")
            nama_kereta = kereta.get("nama_kereta", "-")
            tanggal = kereta.get("tanggal", "-")
            jenis_layanan = kereta.get("jenis_layanan", "-")
            stasiun_transit = kereta.get("stasiun_transit", ["-"])  # Jika tidak ada stasiun, tetap buat satu baris
            waktu_transit = kereta.get("waktu_transit", ["-"])

            span_count = max(len(stasiun_transit), 1)  # Pastikan minimal satu baris

            # Mengisi kolom ID, Nama, Tanggal, dan Jenis Layanan hanya di baris pertama dari setiap kereta
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(tanggal))
            self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(jenis_layanan))

            # Menggabungkan sel untuk ID Kereta, Nama, Tanggal, dan Jenis Layanan
            self.ui.tableWidget.setSpan(row, 0, span_count, 1)
            self.ui.tableWidget.setSpan(row, 1, span_count, 1)
            self.ui.tableWidget.setSpan(row, 2, span_count, 1)
            self.ui.tableWidget.setSpan(row, 3, span_count, 1)

            # Mengisi Stasiun Transit dan Waktu Transit
            for i in range(span_count):
                self.ui.tableWidget.setItem(row + i, 4, QtWidgets.QTableWidgetItem(stasiun_transit[i] if i < len(stasiun_transit) else "-"))
                self.ui.tableWidget.setItem(row + i, 5, QtWidgets.QTableWidgetItem(waktu_transit[i] if i < len(waktu_transit) else "-"))

            row += span_count  # Update row index untuk data berikutnya

        # Atur tampilan tabel
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.resizeRowsToContents()

    def search_train(self):
        """Pencarian kereta berdasarkan input pengguna."""
        nama_kereta = self.ui.input_nama_kereta_2.text().strip().lower()
        stasiun_awal = self.ui.input_stasiun_awal_2.text().strip().lower()
        stasiun_akhir = self.ui.input_stasiun_tujuan_2.text().strip().lower()

        #print(f" Input Pencarian -> Nama: {nama_kereta}, Awal: {stasiun_awal}, Akhir: {stasiun_akhir}")

        filtered_data = []

        for kereta in self.data:
            nama_kereta_data = kereta.get("nama_kereta", "").strip().lower()
            stasiun_transit = kereta.get("stasiun_transit", [])

            # Pastikan stasiun_transit adalah list dan minimal 2 elemen
            if isinstance(stasiun_transit, list) and len(stasiun_transit) > 1:
                stasiun_awal_data = stasiun_transit[0].strip().lower()
                stasiun_akhir_data = stasiun_transit[-1].strip().lower()

                #print(f" Data: {nama_kereta_data}, Awal: {stasiun_awal_data}, Akhir: {stasiun_akhir_data}")

                # Cek harus sesuai urutan
                if (nama_kereta in nama_kereta_data and
                    stasiun_awal == stasiun_awal_data and
                    stasiun_akhir == stasiun_akhir_data):
                    print(" Ditemukan!")
                    filtered_data.append(kereta)

        # Jika tidak ada hasil
        if not filtered_data:
            QtWidgets.QMessageBox.information(self, "Hasil Pencarian", "Tidak ada kereta yang ditemukan.")
        else:
            self.populate_table(filtered_data)

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = QtWidgets.QStackedWidget()
    window = LihatJadwalKereta(main_app)
    main_app.addWidget(window)
    main_app.show()
    sys.exit(app.exec_())
