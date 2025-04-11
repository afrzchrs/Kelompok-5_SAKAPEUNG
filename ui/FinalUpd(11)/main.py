import sys
from PyQt5.QtWidgets import QStackedWidget, QApplication
from screens.welcome_screen import WelcomeScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.user_dashboard import UserDashboard
from screens.admin_dashboard import AdminDashboard
from screens.akun_dashboard import AkunDashboard
from screens.rekening_dashboard import RekeningDashboard
from screens.TicketSearch import TicketSearch  
from screens.TicketShow import TicketShow  
from screens.DetailPemesanan import DetailPemesanan
from screens.BookingKursi import BookingKursi
from screens.Pembayaran import Pembayaran
from screens.lihatJadwalKereta_dashboard import LihatJadwalKereta
from screens.EditDataKereta_dashboard import DashboardEditData 
from screens.tiket_saya_screen import TiketSaya
from screens.lihatRekapKeuntungan_dasboard import LihatRekapKeuntungan
from screens.detailRekapKeuntungan_dasboard import DetailRekapKeuntungan  

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        self.current_user = None  # Menyimpan data user yang sedang login
        self.booking_kursi_screen = None  
        self.pembayaran_screen = None 
        self.email_pengguna = None  # Simpan email pengguna yang login
   
        # Inisialisasi semua halaman aplikasi
        self.welcome_screen = WelcomeScreen(self)
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.dashboard_admin = AdminDashboard(self)
        self.dashboard_user = UserDashboard(self) 
        self.dashboard_akun = AkunDashboard(self)
        self.dashboard_rekening = RekeningDashboard(self)
        self.ticket_show_screen = TicketShow(self)
        self.ticket_search_screen = TicketSearch(self,self.ticket_show_screen)  
        self.detail_pemesanan_screen = DetailPemesanan(self)
        self.lihat_jadwal_kereta = LihatJadwalKereta(self)
        self.admin_edit_data_kereta = DashboardEditData(self)
        self.tiket_saya_screen = TiketSaya(self)  # Tambahkan email pengguna 
        self.lihat_RekapKeuntungan = LihatRekapKeuntungan(self)
        self.detail_RekapKeuntungan = DetailRekapKeuntungan(self)     
        
        # Menambahkan halaman ke dalam stack
        self.addWidget(self.welcome_screen)
        self.addWidget(self.login_screen)
        self.addWidget(self.register_screen)
        self.addWidget(self.dashboard_admin)
        self.addWidget(self.dashboard_user)
        self.addWidget(self.dashboard_akun)
        self.addWidget(self.dashboard_rekening)
        self.addWidget(self.ticket_search_screen)  
        self.addWidget(self.ticket_show_screen)  
        self.addWidget(self.detail_pemesanan_screen)
        self.addWidget(self.lihat_jadwal_kereta)
        self.addWidget(self.admin_edit_data_kereta)  
        self.addWidget(self.tiket_saya_screen)
        self.addWidget(self.lihat_RekapKeuntungan)
        self.addWidget(self.detail_RekapKeuntungan)


        # Menampilkan halaman awal (Welcome Screen)
        self.setCurrentWidget(self.welcome_screen)
        self.setMinimumSize(800, 600)
        
        # Fokuskan ke welcome screen agar bisa menangkap event keyboard
        self.welcome_screen.setFocus()

        # Integrasi lihat jadwal ke dashboard user
        self.dashboard_user.ui.lihat_jadwal_kereta_button.clicked.connect(self.open_lihat_jadwal)
        
        # Integrasi tiket saya ke dashboard user
        self.dashboard_user.ui.tiket_saya_button.clicked.connect(self.open_tiket_saya)
        
        """ Integrasi Dashboard Admin """

        # Integrasi Edit Data Kereta ke dashboard admin
        self.dashboard_admin.ui.edit_jadwal_kereta_button.clicked.connect(self.open_edit_data_kereta)
        
        # Integrasi lihat rekap keuntungan dashboard admin
        self.dashboard_admin.ui.lihat_rekap_keuntungan_button.clicked.connect(self.open_lihat_rekap_keuntungan)
        
        # Jalankan update kursi langsung saat aplikasi dimulai
        print("Memperbarui data kursi...")
        self.admin_edit_data_kereta.update_kursi_kereta()
        print("Data kursi berhasil diperbarui!")

    """ INTEGRASI USER DASH """
    def open_lihat_jadwal(self):
        """Menampilkan halaman Lihat Jadwal Kereta dengan update kursi terbaru."""
        print("Memperbarui data kursi sebelum melihat jadwal...")
        self.admin_edit_data_kereta.update_kursi_kereta()  
        print("Data kursi diperbarui sebelum melihat jadwal.")
        self.setCurrentWidget(self.lihat_jadwal_kereta)
    
    def open_tiket_saya(self):
        """Menampilkan halaman Tiket Saya tanpa perlu login."""   
        # Langsung pindah ke halaman "Tiket Saya" tanpa cek login
        self.tiket_saya_screen.email_pengguna = self.email_pengguna  # Perbarui email pengguna
        self.tiket_saya_screen.load_tiket()  # Muat ulang tiket dengan email pengguna yang login
        self.setCurrentWidget(self.tiket_saya_screen)

    def open_ticket_search(self):
        """Pindah kembali ke halaman TicketSearch saat tombol 'Kembali' ditekan"""
        self.setCurrentWidget(self.ticket_search_screen)

    def open_ticket_show(self):
        """Pindah ke halaman TicketShow setelah hasil pencarian ditemukan""" 
        self.setCurrentWidget(self.ticket_show_screen)
        
    def open_detail_pemesanan(self, tiket_terpilih):
        """Navigasi ke halaman DetailPemesanan"""
       
        try:
            self.detail_pemesanan_screen.tampilkan_detail(tiket_terpilih)
            self.setCurrentWidget(self.detail_pemesanan_screen)
        except Exception as e:
            print(f"Error di open_detail_pemesanan: {e}")

    def open_booking_kursi(self, tiket_terpilih):
        """Navigasi ke halaman pemilihan kursi."""
        if not self.booking_kursi_screen:
            self.booking_kursi_screen = BookingKursi(self, tiket_terpilih)
            self.addWidget(self.booking_kursi_screen)
        else:
            self.booking_kursi_screen.tiket_terpilih = tiket_terpilih
            self.booking_kursi_screen.selected_seat = None 

        self.setCurrentWidget(self.booking_kursi_screen)

    def open_pembayaran(self, tiket_terpilih):
        """Navigasi ke halaman pembayaran setelah kursi dipilih."""
        if not self.pembayaran_screen:
            self.pembayaran_screen = Pembayaran(self, tiket_terpilih)
            self.addWidget(self.pembayaran_screen)
        else:
            self.pembayaran_screen.tiket_terpilih = tiket_terpilih
            self.pembayaran_screen.tampilkan_detail_tiket()

        self.setCurrentWidget(self.pembayaran_screen)

    def kembali_ke_ticket_search(self):
        """Navigasi kembali ke halaman utama (TicketSearch) setelah pembayaran selesai, dan reset input di semua halaman."""
        
        # Reset input di semua halaman
        self.ticket_search_screen.reset_input()
        self.detail_pemesanan_screen.reset_input()
        if self.booking_kursi_screen:
            self.booking_kursi_screen.reset_input()
        if self.pembayaran_screen:
            self.pembayaran_screen.reset_input()

        # Pindah ke halaman Ticket Search
        self.setCurrentWidget(self.ticket_search_screen)
    

    """ INTEGRASI ADMIN DASH """
    def open_edit_data_kereta(self):
        """Menampilkan halaman Edit Data Kereta dengan update kursi terbaru."""
        print("Memperbarui data kursi sebelum edit data kereta...")
        self.admin_edit_data_kereta.update_kursi_kereta() 
        print("Data kursi diperbarui sebelum edit data kereta.")
        self.setCurrentWidget(self.admin_edit_data_kereta) 
        
    def open_lihat_rekap_keuntungan(self):
        """Navigasi ke halaman Lihat Rekap Keuntungan."""
        self.setCurrentWidget(self.lihat_RekapKeuntungan)

    def open_detail_rekap_keuntungan(self):
        """Navigasi ke halaman Detail Rekap Keuntungan."""
        self.setCurrentWidget(self.detail_RekapKeuntungan)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
