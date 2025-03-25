"""
Nama: Adi Rafi Chaerufarizki
NIM: 241524001
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import json
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from ui.lihat_RekapKeuntungan import Ui_lihat_RekapKeuntungan as lihat_RekapKeuntungan

RIWAYATPEMESANAN = "databases/riwayat_pemesanan.json"
USERDATABASE = "databases/user_database.json"

class LihatRekapKeuntungan(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.ui = lihat_RekapKeuntungan()
        self.ui.setupUi(self)
        self.main_app = main_app

        # Pastikan atribut `self.email_to_nama` dibuat lebih awal
        self.email_to_nama = self.load_user_data()

        # Load data user dari user_database.json
        self.load_user_data()

        # Load data ke tabel saat halaman dibuka
        self.load_data_rekap()

        # Tombol kembali ke dashboard admin
        self.ui.button_kembali.clicked.connect(self.kembali_ke_dashboard)

        # Navigasi ke halaman detail rekap keuntungan
        self.ui.button_lihat_detail_rekap.clicked.connect(self.buka_detail_rekap)

    def load_user_data(self):
        """Membaca user_database.json dan membuat mapping email -> nama_lengkap."""
        try:
            with open(USERDATABASE, "r", encoding="utf-8") as file:
                users = json.load(file)
            return {user["email"]: user["nama_lengkap"] for user in users}
        except (FileNotFoundError, json.JSONDecodeError):
            print("Database user tidak ditemukan atau rusak!")
            return {}


    def load_data_rekap(self):
        """Menampilkan semua data tiket dari riwayat pemesanan ke tabel."""
        try:
            with open(RIWAYATPEMESANAN, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Database riwayat pemesanan tidak ditemukan atau rusak!")
            return

        total_tiket = 0
        total_pemasukan = 0

        self.ui.table_lihat_rekap_keuntungan.setRowCount(len(data))

        for row, pemesanan in enumerate(data):
            total_tiket += 1
            total_pemasukan += pemesanan.get("harga", 0)

            # Ambil email dari data pemesanan
            email_penumpang = pemesanan.get("email_penumpang", "-")

            # Ambil nama pengguna berdasarkan email (jika tidak ditemukan, tampilkan "-")
            nama_pengguna = self.email_to_nama.get(email_penumpang, "-")
            
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 0, QTableWidgetItem(nama_pengguna))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 1, QTableWidgetItem(pemesanan.get("email_penumpang", "-")))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 2, QTableWidgetItem(pemesanan.get("nama_kereta", "-")))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 3, QTableWidgetItem(str(pemesanan.get("id_kereta", "-"))))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 4, QTableWidgetItem(str(pemesanan.get("id_kursi", "-"))))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 5, QTableWidgetItem(str(pemesanan.get("harga", "-"))))
            self.ui.table_lihat_rekap_keuntungan.setItem(row, 6, QTableWidgetItem(pemesanan.get("tanggal", "-")))


        # Tampilkan total tiket dan pemasukan di label
        self.ui.label_total_pemasukan.setText(f"Rp {total_pemasukan:,}")
        self.ui.label_tiket_terjual.setText(str(total_tiket))

    def kembali_ke_dashboard(self):
        """Kembali ke dashboard admin."""
        self.main_app.setCurrentWidget(self.main_app.dashboard_admin)

    def buka_detail_rekap(self):
        """Navigasi ke halaman Detail Rekap Keuntungan."""
        self.main_app.setCurrentWidget(self.main_app.detail_RekapKeuntungan)
