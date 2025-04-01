"""
Author: Devi Maulani
NIM: 241524007
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung

"""


import json,os
from PyQt5.QtWidgets import QWidget, QMessageBox
from ui.pembayaran import Ui_pembayaran
from datetime import datetime  

# ================================== DATABASE ================================
PAYMENT_DATABASE_FILE = "databases/payment_database.json"
KURSI_KERETA_FILE = "databases/kursi_kereta.json"
RIWAYAT_PEMBELIAN_FILE = "databases/riwayat_pemesanan.json"

# ========================== KELAS UTAMA PEMBAYRAAN ==========================
class Pembayaran(QWidget):
    def __init__(self, main_app, tiket_terpilih):
        super().__init__()
        self.main_app = main_app
        self.tiket_terpilih = tiket_terpilih
        self.ui = Ui_pembayaran()
        self.ui.setupUi(self)

        # ========================== NAVIGASI ==========================
        self.tampilkan_detail_tiket()
        self.ui.checkBox.stateChanged.connect(self.cek_checkbox)
        self.ui.button_bayar.clicked.connect(self.process_payment)
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
        self.ui.label_kursi.setText(self.tiket_terpilih.get("id_kursi", "Belum Dipilih"))

    def cek_checkbox(self, state):
        print(f"Checkbox diubah: {state}")  # Debugging CHECKBOX 

    def process_payment(self):
        """Memproses pembayaran setelah user memilih kursi dan memastikan database terupdate sebelum berpindah halaman."""

        if not self.ui.checkBox.isChecked():
            QMessageBox.warning(self, "Peringatan", "Anda harus menyetujui syarat dan ketentuan sebelum melakukan pembayaran!")
            return 

        user_data = self.main_app.current_user
        if not user_data:
            QMessageBox.warning(self, "Gagal", "Data user tidak ditemukan.")
            return

        email_user = user_data.get("email")
        harga_tiket = self.tiket_terpilih.get("harga", 0)

        try:
            with open(PAYMENT_DATABASE_FILE, "r") as file:
                users = json.load(file)

            for user in users:
                if user["email"] == email_user:
                    if user["saldo"] >= harga_tiket:
                        user["saldo"] -= harga_tiket
                        kursi_terupdate = self.update_kursi_database()
                        riwayat_terupdate = self.simpan_ke_riwayat()

                        with open(PAYMENT_DATABASE_FILE, "w") as file:
                            json.dump(users, file, indent=4)

                        if kursi_terupdate and riwayat_terupdate:
                            QMessageBox.information(self, "Sukses", "Pembayaran berhasil! Tiket telah dipesan.")
                            self.main_app.kembali_ke_ticket_search() 
                        else:
                            QMessageBox.warning(self, "Gagal", "Terjadi kesalahan dalam memperbarui database. Coba lagi.")
                        return
                    else:
                        QMessageBox.warning(self, "Gagal", "Saldo tidak mencukupi.")
                        return
            QMessageBox.warning(self, "Gagal", "Akun tidak ditemukan.")
        except Exception as e:
            print(f"Error saat memproses pembayaran: {e}")

    def update_kursi_database(self):
        """Menandai kursi sebagai 'dipesan' setelah pembayaran sukses."""
        try:
            with open(KURSI_KERETA_FILE, "r") as file:
                data = json.load(file)

            kursi_ditemukan = False

            for kereta in data:
                if kereta.get('id_kereta') == self.tiket_terpilih.get('id_kereta') and \
                kereta.get('tanggal') == self.tiket_terpilih.get('tanggal'):
                    for gerbong in kereta.get('gerbong', []):
                        if gerbong.get('gerbong_id') == self.tiket_terpilih.get('gerbong_id'):
                            if self.tiket_terpilih['id_kursi'] in gerbong['kursi']:
                                gerbong['kursi'][self.tiket_terpilih['id_kursi']] = False
                                gerbong['kapasitas'] -= 1
                                kursi_ditemukan = True
            if kursi_ditemukan:
                with open(KURSI_KERETA_FILE, "w") as file:
                    json.dump(data, file, indent=4)
                return True  
            else:
                return False  
        except Exception as e:
            return False

    def simpan_ke_riwayat(self):
        """Menyimpan tiket yang telah dibeli ke riwayat pembelian dengan waktu pemesanan."""
        try:
            if os.path.exists(RIWAYAT_PEMBELIAN_FILE) and os.path.getsize(RIWAYAT_PEMBELIAN_FILE) > 0:
                with open(RIWAYAT_PEMBELIAN_FILE, "r") as file:
                    try:
                        riwayat = json.load(file)
                        if not isinstance(riwayat, list):  
                            riwayat = []
                    except json.JSONDecodeError:
                        riwayat = []
            else:
                riwayat = []

            # Tambahkan detail penumpang dan waktu pemesanan
            tiket_dengan_penumpang = self.tiket_terpilih.copy()
            tiket_dengan_penumpang["nama_penumpang"] = self.tiket_terpilih.get("nama_penumpang", "Tidak Diketahui")
            tiket_dengan_penumpang["email_penumpang"] = self.tiket_terpilih.get("email_penumpang", "Tidak Diketahui")
            tiket_dengan_penumpang["nomor_telepon"] = self.tiket_terpilih.get("nomor_telepon", "Tidak Diketahui")

            # menambahkan waktu pemesanan secara realtime
            waktu_pemesanan = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            tiket_dengan_penumpang["waktu_pemesanan"] = waktu_pemesanan

            # menambahkan tiket ke riwayat
            riwayat.append(tiket_dengan_penumpang)

            # Simpan kembali ke file JSON
            with open(RIWAYAT_PEMBELIAN_FILE, "w") as file:
                json.dump(riwayat, file, indent=4)
            return True  
        except Exception as e:
            return False  

    def kembali_ke_booking_kursi(self):
        """Kembali ke halaman Booking Kursi."""
        self.main_app.setCurrentWidget(self.main_app.booking_kursi_screen)

    def reset_input(self):

       # ============== reset input pada halaman pembayaran (mengubahnya menjadi default kembali) ==============
        self.ui.label_nama_kereta.clear()
        self.ui.label_namakereta.clear()
        self.ui.label_asal.clear()
        self.ui.label_tujuan.clear()
        self.ui.label_layanan.clear()
        self.ui.label_jenislayanan.clear()
        self.ui.label_waktu_ticket.clear()
        self.ui.label_harga.clear()
        self.ui.label_harga_2.clear()
        self.ui.label_kursi.clear()

        
        self.ui.checkBox.setChecked(False)

