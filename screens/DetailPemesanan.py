import sys, os, json
from PyQt5.QtWidgets import QWidget, QMessageBox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui')))
from ui.detail_pemesanan import Ui_detail_pemesanan

# ====================================== PATH DATABASE ==========================================
USER_DATABASE_FILE = "databases/user_database.json"

# ================================ KELAS UTAMA DETAIL PEMESANAN =================================
class DetailPemesanan(QWidget):
    def __init__(self, main_app):
        super().__init__()

        self.ui =Ui_detail_pemesanan()
        self.ui.setupUi(self)
        self.setWindowTitle("Detail Pemesanan")
        self.main_app = main_app  # Menyimpan referensi ke aplikasi utama

        # ============================= NAVIGASI ================================
        self.ui.button_keluar.clicked.connect(self.kembali_ke_show)
        self.ui.checkBox.stateChanged.connect(self.isi_data_akun)
        self.ui.button_lanjutkan.clicked.connect(self.lanjut_ke_booking_kursi)

    def tampilkan_detail(self, tiket):
        """Menampilkan data tiket yang dipilih di UI"""
        self.tiket_terpilih = tiket  
       
        if not tiket:
            return
        try:
            self.ui.label_nama_kereta.setText(tiket.get("nama_kereta", ""))
            self.ui.label_asal.setText(tiket.get("asal", ""))
            self.ui.label_tujuan.setText(tiket.get("tujuan", ""))
            self.ui.label_waktu_ticket.setText(f"Tanggal: {tiket.get('tanggal', 'Tidak Ada Tanggal')} | {tiket.get('waktu_berangkat', '')} - {tiket.get('waktu_tiba', '')}")
            self.ui.label_layanan.setText(tiket.get("jenis_layanan", ""))
            self.ui.label_harga.setText(f"Rp {tiket.get('harga', 0)}")  
        except Exception as e:
            print(f"Error saat menampilkan detail: {e}")
  
    def isi_data_akun(self, state):
        """Mengisi data otomatis jika checkbox dicentang."""
        if state == 2: 
            user_data = self.main_app.current_user
            if user_data:
                self.ui.line_nama.setText(user_data.get("nama_lengkap", ""))
                self.ui.line_email.setText(user_data.get("email", ""))
                self.ui.line_nomor.setText(user_data.get("nomor_telepon", ""))
            else:
                QMessageBox.warning(self, "Gagal", "Tidak dapat menemukan data user.")
        else:
            self.ui.line_nama.clear()
            self.ui.line_email.clear()
            self.ui.line_nomor.clear()

    def lanjut_ke_booking_kursi(self):
        """Memeriksa apakah data akun sudah diisi sebelum melanjutkan ke pemilihan kursi."""
        try:
            if not self.tiket_terpilih:
                QMessageBox.warning(self, "Peringatan", "Data tiket tidak valid.")
                return
            # akan memastikan semua data akun telah diisi
            nama = self.ui.line_nama.text().strip()
            email = self.ui.line_email.text().strip()
            nomor = self.ui.line_nomor.text().strip()

            self.tiket_terpilih["nama_penumpang"] = self.ui.line_nama.text().strip()
            self.tiket_terpilih["email_penumpang"] = self.ui.line_email.text().strip()
            self.tiket_terpilih["nomor_telepon"] = self.ui.line_nomor.text().strip()

            if not nama or not email or not nomor:
                QMessageBox.warning(self, "Peringatan", "Harap isi data akun terlebih dahulu sebelum melanjutkan!")
                return  
            self.main_app.open_booking_kursi(self.tiket_terpilih)
        except Exception as e:
            print(f"Error saat membuka halaman Booking Kursi: {e}")

    def kembali_ke_show(self):
            """Navigasi kembali ke TicketShow."""
            self.main_app.setCurrentWidget(self.main_app.ticket_show_screen)
            self.reset_input()

    def reset_input(self):
        # ============== reset input pada halaman detail pemesanan (mengubahnya menjadi default kembali) ==============
        
        self.ui.line_nama.clear()
        self.ui.line_email.clear()
        self.ui.line_nomor.clear()

        self.ui.checkBox.setChecked(False)
        
        self.ui.label_nama_kereta.clear()
        self.ui.label_asal.clear()
        self.ui.label_tujuan.clear()
        self.ui.label_waktu_ticket.clear()
        self.ui.label_layanan.clear()
        self.ui.label_harga.clear()

        self.tiket_terpilih = None  # menghapus data tiket sebelumnya







