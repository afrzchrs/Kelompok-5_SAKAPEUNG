"""
Author: Devi Maulani
NIM: 241524007
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung

"""

import json, os
from PyQt5.QtWidgets import QWidget, QMessageBox
from ui.pembayaran import Ui_konfirmasi_pembayaran
from datetime import datetime  

# ================================== DATABASE ================================
PAYMENT_DATABASE_FILE = "databases/payment_database.json"
KURSI_KERETA_FILE = "databases/kursi_kereta.json"
RIWAYAT_PEMBELIAN_FILE = "databases/riwayat_pemesanan.json"

# ========================== KELAS UTAMA KONFRIMASI PEMBAYARAN ==========================
class Pembayaran(QWidget):
    def __init__(self, main_app, tiket_terpilih):
        super().__init__()
        self.main_app = main_app
        self.tiket_terpilih = tiket_terpilih
        self.ui = Ui_konfirmasi_pembayaran()
        self.ui.setupUi(self)

        # ========================== NAVIGASI ==========================
        self.tampilkan_detail_tiket()
        self.ui.checkBox.stateChanged.connect(self.cek_checkbox)
        self.ui.button_bayar.clicked.connect(self.buka_transaksi_pembayaran)
        self.ui.button_keluar.clicked.connect(self.kembali_ke_booking_kursi)

    def tampilkan_detail_tiket(self):
        """Menampilkan detail tiket yang dipilih di halaman pembayaran."""
        self.ui.label_nama_kereta.setText(self.tiket_terpilih.get("nama_kereta", ""))
        self.ui.label_namakereta.setText(self.tiket_terpilih.get("nama_kereta", ""))
        self.ui.label_asal.setText(self.tiket_terpilih.get("asal", ""))
        self.ui.label_tujuan.setText(self.tiket_terpilih.get("tujuan", ""))
        self.ui.label_layanan.setText(self.tiket_terpilih.get("jenis_layanan", ""))
        self.ui.label_jenislayanan.setText(self.tiket_terpilih.get("jenis_layanan", ""))
        self.ui.label_waktu_ticket.setText(f"{self.tiket_terpilih.get('tanggal', '')} | {self.tiket_terpilih.get('waktu_berangkat', '')} - {self.tiket_terpilih.get('waktu_tiba', '')}")
        self.ui.label_harga_2.setText(f"Rp {self.tiket_terpilih.get('harga', 0)}")
        self.ui.label_harga.setText(f"Rp {self.tiket_terpilih.get('harga', 0)}")
        self.ui.label_kursi.setText(f"{self.tiket_terpilih.get('id_kursi', 'Belum Dipilih')} | {self.tiket_terpilih.get('gerbong_id', '')}")

    def cek_checkbox(self, state):
        print(f"Checkbox diubah: {state}")  # Debugging CHECKBOX 

    def buka_transaksi_pembayaran(self):
        """Mengarahkan pengguna ke halaman transaksi pembayaran."""
        if not self.ui.checkBox.isChecked():
            QMessageBox.warning(self, "Peringatan", "Anda harus menyetujui syarat dan ketentuan sebelum melakukan pembayaran!")
            return 
        self.main_app.open_transaksi_pembayaran(self.tiket_terpilih)

    def kembali_ke_booking_kursi(self):
        """Kembali ke halaman Booking Kursi."""
        self.main_app.setCurrentWidget(self.main_app.booking_kursi_screen)

    def reset_input(self):
        """Reset input pada halaman pembayaran."""
        self.ui.label_nama_kereta.clear()
        self.ui.label_asal.clear()
        self.ui.label_tujuan.clear()
        self.ui.label_layanan.clear()
        self.ui.label_waktu_ticket.clear()
        self.ui.label_harga.clear()
        self.ui.label_kursi.clear()
        self.ui.checkBox.setChecked(False)


