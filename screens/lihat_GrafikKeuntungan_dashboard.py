"""
Nama: Adi Rafi Chaerufarizki
NIM: 241524001
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from ui.lihat_grafik_keuntungan import Ui_lihat_grafik_keuntungan as LihatGrafikUi
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

RIWAYAT_PEMESANAN = "databases/riwayat_pemesanan.json"

class LihatGrafikKeuntungan(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.ui = LihatGrafikUi()
        self.ui.setupUi(self)
        self.main_app = main_app

        # Pastikan widget_grafik ada sebelum menambahkan grafik
        if not self.ui.widget_grafik:
            print("Error: widget_grafik tidak ditemukan!")
            return

        # Pastikan widget_grafik memiliki layout sebelum menambahkan canvas
        if not self.ui.widget_grafik.layout():
            self.ui.widget_grafik.setLayout(QVBoxLayout())

        # Inisialisasi canvas matplotlib (hanya sekali)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.ui.widget_grafik.layout().addWidget(self.canvas)

        # Event ketika combobox diubah
        self.ui.combo_filter_rekap.currentIndexChanged.connect(self.tampilkan_grafik)

        # Tombol kembali ke halaman Detail Rekap Keuntungan
        self.ui.button_kembali.clicked.connect(self.kembali_ke_detail_rekap)

        # Tampilkan grafik pertama kali
        self.tampilkan_grafik()

    def kembali_ke_detail_rekap(self):
        """Navigasi kembali ke halaman Detail Rekap Keuntungan."""
        self.main_app.setCurrentWidget(self.main_app.detail_RekapKeuntungan)

    def tampilkan_grafik(self):
        """Menampilkan diagram batang berdasarkan filter (Harian, Mingguan, Bulanan, Tahunan)."""
        try:
            with open(RIWAYAT_PEMESANAN, "r", encoding="utf-8") as file:
                data_pemesanan = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Database riwayat pemesanan tidak ditemukan atau rusak!")
            return

        filter_terpilih = self.ui.combo_filter_rekap.currentText()
        tanggal_sekarang = datetime.today().date()
        keuntungan_per_tanggal = {}

       for pemesanan in data_pemesanan:
            try:
                tanggal_pemesanan = datetime.strptime(pemesanan["tanggal"], "%Y-%m-%d").date()
            except ValueError:
                continue
            harga = pemesanan.get("harga", 0)

            if filter_terpilih == "Harian":
                if tanggal_pemesanan == tanggal_sekarang:
                    keuntungan_per_tanggal[tanggal_pemesanan] = keuntungan_per_tanggal.get(tanggal_pemesanan, 0) + harga

            elif filter_terpilih == "Mingguan":
                if tanggal_pemesanan.year == tanggal_sekarang.year and tanggal_pemesanan.month == tanggal_sekarang.month:
                    label = tanggal_sekarang.strftime("%B %Y")  # Misalnya "April 2025"
                    keuntungan_per_tanggal[label] = keuntungan_per_tanggal.get(label, 0) + harga


            elif filter_terpilih == "Bulanan":
                if tanggal_pemesanan.year == tanggal_sekarang.year and tanggal_pemesanan.month <= tanggal_sekarang.month:
                    nama_bulan = tanggal_pemesanan.strftime("%B")
                keuntungan_per_tanggal[nama_bulan] = keuntungan_per_tanggal.get(nama_bulan, 0) + harga

            elif filter_terpilih == "Tahunan":
                # Ambil data dari tahun sekarang ke tahun-tahun sebelumnya
                tahun = tanggal_pemesanan.year
                if tahun <= tanggal_sekarang.year:
                    keuntungan_per_tanggal[str(tahun)] = keuntungan_per_tanggal.get(str(tahun), 0) + harga

        # Jika tidak ada data, tampilkan pesan
        if not keuntungan_per_tanggal:
            self.ax.clear()
            self.ax.set_title(f"Tidak ada data keuntungan ({filter_terpilih})")
            self.canvas.draw()
            return

        # Menghitung persentase perubahan keuntungan
        keuntungan_list = list(keuntungan_per_tanggal.values())
        if len(keuntungan_list) >= 2:
            keuntungan_terbaru = keuntungan_list[-1]
            keuntungan_sebelumnya = keuntungan_list[-2]
            persentase_perubahan = ((keuntungan_terbaru - keuntungan_sebelumnya) / keuntungan_sebelumnya) * 100
        else:
            persentase_perubahan = 0

        # Update label total pemasukan
        total_keuntungan = sum(keuntungan_per_tanggal.values())
        self.ui.label_total_pemasukan.setText(f"Rp {total_keuntungan:,}")

        # Update label persentase perubahan
        self.ui.label_persentase_perubahan.setText(f"{persentase_perubahan:.2f}%")

        # Update diagram batang
        self.ax.clear()
        dates = list(keuntungan_per_tanggal.keys())
        values = list(keuntungan_per_tanggal.values())

        self.ax.bar(dates, values, color=["#6a11cb", "#2575fc"])
        self.ax.set_title(f"Grafik Keuntungan ({filter_terpilih})")
        self.ax.set_xlabel("Tanggal")
        self.ax.set_ylabel("Total Keuntungan (Rp)")

        if dates:  # Format tanggal hanya jika ada data
            self.figure.autofmt_xdate()

        self.canvas.draw()
