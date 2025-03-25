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
from datetime import datetime, timedelta
from ui.detail_RekapKeuntungan import Ui_detail_RekapKeuntungan as detail_RekapKeuntungan

RIWAYATPEMESANAN = "databases/riwayat_pemesanan.json"
USERDATABASE = "databases/user_database.json"

class DetailRekapKeuntungan(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.ui = detail_RekapKeuntungan()
        self.ui.setupUi(self)
        self.main_app = main_app

        # Load data pengguna (email → nama)
        self.email_to_nama = self.load_data_pengguna()

        # Pastikan combobox memiliki nilai default sebelum di-load
        self.ui.combo_filter_rekap.setCurrentIndex(0)

        # Load data sesuai filter saat combobox berubah
        self.ui.combo_filter_rekap.currentIndexChanged.connect(self.update_tabel_berdasarkan_filter)

        # Tombol kembali ke halaman utama rekap keuntungan
        self.ui.button_kembali.clicked.connect(self.kembali_ke_rekap)

        # Load data pertama kali (default: Harian)
        self.update_tabel_berdasarkan_filter()

    def load_data_pengguna(self):
        """Memuat data pengguna dari user_database.json (email → nama pengguna)."""
        try:
            with open(USERDATABASE, "r", encoding="utf-8") as file:
                users = json.load(file)
            return {user["email"]: user["nama_lengkap"] for user in users}
        except (FileNotFoundError, json.JSONDecodeError):
            print(" Database pengguna tidak ditemukan atau rusak!")
            return {}

    def update_tabel_berdasarkan_filter(self):
        """Memfilter data berdasarkan pilihan (Harian, Mingguan, Bulanan, Tahunan)"""
        try:
            with open(RIWAYATPEMESANAN, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Database riwayat pemesanan tidak ditemukan atau rusak!")
            return

        # Ambil filter yang dipilih oleh admin
        filter_terpilih = self.ui.combo_filter_rekap.currentText()
        data_terfilter = []
        total_keuntungan = 0

        # Tanggal saat ini
        tanggal_sekarang = datetime.today().date()

        for pemesanan in data:
            tanggal_pemesanan = datetime.strptime(pemesanan["tanggal"], "%Y-%m-%d").date()

            if filter_terpilih == "Harian":
                if tanggal_pemesanan == tanggal_sekarang:
                    data_terfilter.append(pemesanan)

            elif filter_terpilih == "Mingguan":
                minggu_lalu = tanggal_sekarang - timedelta(days=7)
                if minggu_lalu <= tanggal_pemesanan <= tanggal_sekarang:
                    data_terfilter.append(pemesanan)

            elif filter_terpilih == "Bulanan":
                if tanggal_pemesanan.year == tanggal_sekarang.year and tanggal_pemesanan.month == tanggal_sekarang.month:
                    data_terfilter.append(pemesanan)

            elif filter_terpilih == "Tahunan":
                if tanggal_pemesanan.year == tanggal_sekarang.year:
                    data_terfilter.append(pemesanan)

        # Menampilkan data ke dalam tabel
        self.ui.table_lihat_detail_rekap_keuntungan.setRowCount(len(data_terfilter))

        for row, pemesanan in enumerate(data_terfilter):
            total_keuntungan += pemesanan.get("harga", 0)
            email_pelanggan = pemesanan.get("email_penumpang", "-")

            nama_pengguna = self.email_to_nama.get(email_pelanggan, "Tidak ada nama")

            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 0, QTableWidgetItem(nama_pengguna))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 1, QTableWidgetItem(pemesanan.get("email_penumpang", "-")))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 2, QTableWidgetItem(pemesanan.get("nama_kereta", "-")))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 3, QTableWidgetItem(str(pemesanan.get("id_kereta", "-"))))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 4, QTableWidgetItem(str(pemesanan.get("id_kursi", "-"))))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 5, QTableWidgetItem(str(pemesanan.get("harga", "-"))))
            self.ui.table_lihat_detail_rekap_keuntungan.setItem(row, 6, QTableWidgetItem(pemesanan.get("tanggal", "-")))


        # Menampilkan total pemasukan sesuai filter di label
        self.ui.label_total_pemasukan.setText(f"Rp {total_keuntungan:,}")

    def kembali_ke_rekap(self):
        """Navigasi kembali ke halaman Lihat Rekap Keuntungan."""
        self.main_app.setCurrentWidget(self.main_app.lihat_RekapKeuntungan)
