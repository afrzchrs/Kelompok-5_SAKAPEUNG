"""
Author: Devi Maulani
NIM: 241524007
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung

"""

import json, os
from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from ui.transasksi_pembayaran import Ui_transaksi_pembayaran
from datetime import datetime
import hashlib

# ================================== DATABASE ================================
PAYMENT_DATABASE_FILE = "databases/payment_database.json"
KURSI_KERETA_FILE = "databases/kursi_kereta.json"
RIWAYAT_PEMBELIAN_FILE = "databases/riwayat_pemesanan.json"

# ========================== KELAS UTAMA TRANSAKSI PEMBAYARAN ==========================
class TransaksiPembayaran(QWidget):
    def __init__(self, main_app, tiket_terpilih):
        super().__init__()
        self.main_app = main_app
        self.tiket_terpilih = tiket_terpilih
        self.ui = Ui_transaksi_pembayaran()
        self.ui.setupUi(self)


        # ========================== NAVIGASI ==========================
        self.reset_input() 
        self.tampilkan_detail_tiket()
        self.ui.button_bayar.clicked.connect(self.proses_pembayaran)
        self.ui.button_keluar.clicked.connect(self.kembali_ke_pembayaran)

    def tampilkan_detail_tiket(self):
        self.ui.label_nama_kereta.setText(self.tiket_terpilih.get("nama_kereta", ""))
        self.ui.label_asal.setText(self.tiket_terpilih.get("asal", ""))
        self.ui.label_tujuan.setText(self.tiket_terpilih.get("tujuan", ""))
        self.ui.label_layanan.setText(self.tiket_terpilih.get("jenis_layanan", ""))
        self.ui.label_waktu_ticket.setText(f"{self.tiket_terpilih.get('tanggal', '')} | {self.tiket_terpilih.get('waktu_berangkat', '')} - {self.tiket_terpilih.get('waktu_tiba', '')}")
        self.ui.label_harga_2.setText(f"Rp {self.tiket_terpilih.get('harga', 0)}")
        self.ui.label_kursi.setText(f"{self.tiket_terpilih.get('id_kursi', 'Belum Dipilih')} | {self.tiket_terpilih.get('gerbong_id', '')}")
        self.update_saldo()
    
    def update_saldo(self):
        """akan menampilkan saldo terbaru """
        try:
            with open(PAYMENT_DATABASE_FILE, "r") as file:
                users = json.load(file)
            for user in users:
                if user["email"] == self.main_app.current_user.get("email"):
                    self.ui.label_saldo.setText(f"Rp {user.get('saldo', 0)}")
                    return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil saldo: {e}")

    def proses_pembayaran(self):
        """akan memproses pembayaran dengan verifikasi PIN dari line_pinNorek."""
        user_data = self.main_app.current_user
        if not user_data:
            QMessageBox.warning(self, "Gagal", "Data user tidak ditemukan.")
            return

        email_user = user_data.get("email")
        harga_tiket = self.tiket_terpilih.get("harga", 0)
        pin_input = self.ui.line_pinNorek.text()

        if not pin_input:
            QMessageBox.warning(self, "Gagal", "PIN harus diisi.")
            return

        try:
            with open(PAYMENT_DATABASE_FILE, "r") as file:
                users = json.load(file)

            for user in users:
                if user["email"] == email_user:
                    if self.verifikasi_pin(user["pin"], pin_input):
                        if user["saldo"] >= harga_tiket:
                            user["saldo"] -= harga_tiket
                            
                            if self.update_kursi_database() and self.simpan_ke_riwayat():
                                with open(PAYMENT_DATABASE_FILE, "w") as file:
                                    json.dump(users, file, indent=4)
                                
                                QMessageBox.information(self, "Sukses", "Pembayaran berhasil! Tiket telah dipesan.")
                                self.reset_input() 
                                self.update_saldo()
                                self.main_app.kembali_ke_ticket_search()
                            else:
                                QMessageBox.warning(self, "Gagal", "Terjadi kesalahan dalam memperbarui database.")
                            return
                        else:
                            QMessageBox.warning(self, "Gagal", "Saldo tidak mencukupi.")
                            return
                    else:
                        QMessageBox.warning(self, "Gagal", "PIN yang anda masukan salah.")
                        return
            QMessageBox.warning(self, "Gagal", "Akun tidak ditemukan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Kesalahan saat pembayaran: {e}")

    def verifikasi_pin(self, hashed_pin, input_pin):
        """melaukan verifikasi PIN dengan hashing pada databse payment"""
        return hashlib.sha256(input_pin.encode()).hexdigest() == hashed_pin

    def update_kursi_database(self):
        """Menandai kursi sebagai 'false' dalam database"""
        try:
            with open(KURSI_KERETA_FILE, "r") as file:
                data = json.load(file)

            kursi_ditemukan = False
            for kereta in data:
                if kereta.get('id_kereta') == self.tiket_terpilih.get('id_kereta') and kereta.get('tanggal') == self.tiket_terpilih.get('tanggal'):
                    for gerbong in kereta.get('gerbong', []):
                        if gerbong.get('gerbong_id') == self.tiket_terpilih.get('gerbong_id'):
                            if gerbong['kursi'].get(self.tiket_terpilih['id_kursi']) == True:
                                gerbong['kursi'][self.tiket_terpilih['id_kursi']] = False
                                gerbong['kapasitas'] -= 1
                                kursi_ditemukan = True
            
            if kursi_ditemukan:
                with open(KURSI_KERETA_FILE, "w") as file:
                    json.dump(data, file, indent=4)
                return True
            return False
        except Exception:
            return False

    def simpan_ke_riwayat(self):
        """akan menyimpan tiket yang telah dibeli ke riwayat pembelian dengan waktu pemesanan."""
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

            tiket_dengan_penumpang = self.tiket_terpilih.copy()
            tiket_dengan_penumpang["nama_penumpang"] = self.tiket_terpilih.get("nama_penumpang", "Tidak Diketahui")
            tiket_dengan_penumpang["email_penumpang"] = self.tiket_terpilih.get("email_penumpang", "Tidak Diketahui")
            tiket_dengan_penumpang["nomor_telepon"] = self.tiket_terpilih.get("nomor_telepon", "Tidak Diketahui")
            waktu_pemesanan = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            tiket_dengan_penumpang["waktu_pemesanan"] = waktu_pemesanan
            riwayat.append(tiket_dengan_penumpang)

            with open(RIWAYAT_PEMBELIAN_FILE, "w") as file:
                json.dump(riwayat, file, indent=4)
            return True  
        except Exception as e:
            return False
    
    def reset_input(self):
         # ============== reset input pada halaman transaksi pembayaran (mengubahnya menjadi default kembali) ==============
        self.ui.line_pinNorek.clear() 
        self.ui.label_nama_kereta.clear()
        self.ui.label_asal.clear()
        self.ui.label_tujuan.clear()
        self.ui.label_layanan.clear()
        self.ui.label_waktu_ticket.clear()
        self.ui.label_harga_2.setText("Rp 0")  
        self.ui.label_kursi.setText("Belum Dipilih") 
        self.update_saldo() 
    
    def kembali_ke_pembayaran(self):
        """Kembali ke halaman pembayaran tanpa menutup aplikasi."""
        self.ui.line_pinNorek.clear()  
        self.main_app.setCurrentWidget(self.main_app.pembayaran_screen)



    



