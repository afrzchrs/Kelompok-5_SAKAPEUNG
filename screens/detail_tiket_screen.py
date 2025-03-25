"""
Nama: Adi Rafi Chaerufarizki
NIM: 241524001
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import sys
import json
from PyQt5 import QtWidgets
from ui.detail_tiket import Ui_dashboard_detail_tiket  # Pastikan path ini benar

USERDATABASE = "databases/user_database.json"

class DetailTiket(QtWidgets.QMainWindow):
    def __init__(self, tiket):
        super().__init__()
        self.ui = Ui_dashboard_detail_tiket()
        self.ui.setupUi(self)

        # Pastikan atribut `self.email_to_nama` dibuat lebih awal
        self.email_to_nama = self.load_user_data()

        # Load data pengguna (email → nama)
        self.email_to_nama = self.load_data_pengguna()

        # Ambil email dari data pemesanan
        email_pelanggan = tiket.get("email_penumpang", "-")

        # Ambil nama pengguna berdasarkan email (jika tidak ditemukan, tampilkan "-")
        nama_pengguna = self.email_to_nama.get(email_pelanggan, "-")

        # Mengisi label dengan data tiket
        self.ui.label_namapenumpang.setText(nama_pengguna)
        self.ui.label_idkereta.setText(str(tiket.get("id_kereta", "-")))
        self.ui.label_namakereta.setText(tiket.get("nama_kereta", "-"))
        self.ui.label_stasiunawal.setText(tiket.get("asal", "-"))
        self.ui.label_stasiunakhir.setText(tiket.get("tujuan", "-"))
        self.ui.label_tanggal.setText(tiket.get("tanggal", "-"))
        self.ui.label_waktu.setText(tiket.get("waktu_berangkat", "-"))
        self.ui.label_jenislayanan.setText(tiket.get("jenis_layanan", "-"))
        self.ui.label_idkursi.setText(str(tiket.get("id_kursi", "-")))
        self.ui.label_tarif.setText(f"Rp {tiket.get('harga', 0):,}")
        self.ui.label_waktupemesanan.setText(tiket.get("waktu_pemesanan", "-"))

        # Tombol kembali ke menu sebelumnya
        self.ui.button_kembali.clicked.connect(self.close)

    def load_user_data(self):
        """Membaca user_database.json dan membuat mapping email -> nama_lengkap."""
        try:
            with open(USERDATABASE, "r", encoding="utf-8") as file:
                users = json.load(file)
            return {user["email"]: user["nama_lengkap"] for user in users}
        except (FileNotFoundError, json.JSONDecodeError):
            print("Database user tidak ditemukan atau rusak!")
            return {}

    def load_data_pengguna(self):
        """Memuat data pengguna dari user_database.json (email → nama pengguna)."""
        try:
            with open(USERDATABASE, "r", encoding="utf-8") as file:
                users = json.load(file)
            return {user["email"]: user["nama_lengkap"] for user in users}
        except (FileNotFoundError, json.JSONDecodeError):
            print(" Database pengguna tidak ditemukan atau rusak!")
            return {}
