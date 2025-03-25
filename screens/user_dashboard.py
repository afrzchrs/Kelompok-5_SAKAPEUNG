"""
Author: Roufiel Hadi
NIM: 241524028
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import sys
from ui.dashboard_user import Ui_dashboard_user_sakapeung as Ui_dashboard_user # Pastikan path ini benar
from PyQt5.QtWidgets import QMainWindow  # Import QMessageBox juga

class UserDashboard(QMainWindow):
    """
    Kelas untuk tampilan dashboard pengguna setelah login.
    Menyediakan navigasi ke berbagai fitur pengguna seperti pembelian tiket,
    melihat jadwal kereta, melihat tiket yang dimiliki, dan pengelolaan akun.
    """
    
    def __init__(self, main_app):
        """Inisialisasi dashboard user dan menghubungkan tombol dengan fungsi navigasi."""
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_dashboard_user()
        self.ui.setupUi(self)
        
        self.setup_connections()

    def setup_connections(self):
        """Menghubungkan tombol dengan fungsi navigasi."""
        self.ui.home_button.clicked.connect(self.show_home)
        self.ui.pembelian_tiket_button.clicked.connect(self.show_pembelian_tiket)
        self.ui.lihat_jadwal_kereta_button.clicked.connect(self.show_lihat_jadwal)
        self.ui.tiket_saya_button.clicked.connect(self.show_tiket_saya)
        self.ui.dashboard_akun_button.clicked.connect(self.show_dashboard_akun)
        self.ui.dashboard_rekening_button.clicked.connect(self.show_dashboard_rekening)
        self.ui.keluar_button.clicked.connect(self.exit_application)

    def set_user(self, user):
        """Menyimpan informasi pengguna yang sedang login."""
        self.user = user

    def exit_application(self):
        """Menutup aplikasi."""
        sys.exit()

    # ======== Fungsi Navigasi ========
    def show_home(self):
        """Menampilkan halaman utama dashboard user."""
        self.ui.user.setCurrentWidget(self.ui.user_dashboard)

    def show_pembelian_tiket(self):
        """Menampilkan halaman pembelian tiket."""
        self.main_app.setCurrentWidget(self.main_app.ticket_search_screen)

    def show_lihat_jadwal(self):
        """Menampilkan halaman jadwal kereta."""
        self.ui.user.setCurrentWidget(self.ui.lihat_jadwal_kereta)

    def show_tiket_saya(self):
        """Menampilkan halaman tiket yang telah dibeli user."""
        self.ui.user.setCurrentWidget(self.ui.tiket_saya)

    def show_dashboard_akun(self):
        """Navigasi ke halaman Dashboard Akun dan menyetel user aktif."""
        self.main_app.dashboard_akun.set_user()  # Pastikan user aktif disimpan
        self.main_app.setCurrentWidget(self.main_app.dashboard_akun)

    def show_dashboard_rekening(self):
        """Navigasi ke halaman Dashboard Rekening."""
        self.main_app.setCurrentWidget(self.main_app.dashboard_rekening)