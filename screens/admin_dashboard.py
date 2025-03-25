"""
Author: Roufiel Hadi
NIM: 241524028
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import sys
from ui.dashboard_admin import Ui_dashboard_admin_sakapeung as Ui_dashboard_admin  # Pastikan path ini benar
from PyQt5.QtWidgets import QMainWindow  # Import QMessageBox juga

class AdminDashboard(QMainWindow):
    """
    Kelas ini mengelola tampilan dashboard admin, termasuk navigasi antara halaman 
    utama, pengeditan jadwal kereta, dan rekap keuntungan.
    """
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_dashboard_admin()
        self.ui.setupUi(self)
        
        # Menghubungkan tombol dengan fungsi yang sesuai
        self.setup_connections()
    
    def setup_connections(self):
        """Menghubungkan tombol dengan fungsi navigasi dan aksi logout."""
        self.ui.home_button.clicked.connect(self.show_home)
        self.ui.edit_jadwal_kereta_button.clicked.connect(self.show_edit_jadwal)
        self.ui.lihat_rekap_keuntungan_button.clicked.connect(self.show_rekap_keuntungan)
        self.ui.logout_button.clicked.connect(self.logout)
        self.ui.keluar_button.clicked.connect(self.exit_application)
    
    def set_user(self, user):
        """Menyimpan informasi user yang sedang login."""
        self.user = user
    
    def logout(self):
        """Menghapus sesi pengguna dan kembali ke layar login."""
        self.main_app.current_user = None
        self.main_app.setCurrentWidget(self.main_app.login_screen)
    
    def exit_application(self):
        """Keluar dari aplikasi sepenuhnya."""
        sys.exit()

    # Fungsi navigasi berdasarkan tombol yang ditekan
    def show_home(self):
        """Menampilkan halaman utama admin."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.admin)
    
    def show_edit_jadwal(self):
        """Menampilkan halaman untuk mengedit jadwal kereta."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.edit_jadwal_kereta)
    
    def show_rekap_keuntungan(self):
        """Menampilkan halaman rekap keuntungan."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.lihat_rekap_keuntungan)
