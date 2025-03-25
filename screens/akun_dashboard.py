"""
Author: Roufiel Hadi
NIM: 241524028
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import json
import re
from PyQt5.QtWidgets import QMainWindow, QMessageBox  # Import QMessageBox juga
from ui.dashboard_akun import Ui_dashboard_admin_sakapeung as Ui_dashboard_akun  # Pastikan path ini benar
from databases.databases import hash_password, USER_DATABASE    # Jika ada di databases.py

class AkunDashboard(QMainWindow):
    """
    Kelas untuk menangani tampilan dan fungsi Dashboard Akun.
    User dapat melihat, mengedit informasi akun, mengganti password, dan mengakses pusat bantuan.
    """

    def __init__(self, main_app):
        """Inisialisasi dashboard akun dan menghubungkan tombol dengan fungsi masing-masing."""
        super().__init__()
        self.main_app = main_app
        self.ui = Ui_dashboard_akun()
        self.ui.setupUi(self)

        self.setup_connections()

    def setup_connections(self):
        """Menghubungkan tombol dengan fungsi navigasi dan aksi pengguna."""
        # Navigasi antar halaman dalam dashboard akun
        self.ui.home_button.clicked.connect(self.show_home)
        self.ui.lihat_informasi_akun_button.clicked.connect(self.show_lihat_informasi_akun)
        self.ui.edit_informasi_akun_button.clicked.connect(self.show_edit_informasi_akun)
        self.ui.ganti_password_button.clicked.connect(self.show_ganti_password)
        self.ui.informasi_aplikasi_button.clicked.connect(self.show_informasi_aplikasi)
        self.ui.pusat_bantuan_button.clicked.connect(self.show_pusat_bantuan)
        self.ui.logout_button.clicked.connect(self.logout)
        self.ui.kembali_button.clicked.connect(self.goto_dashboard_user)
        
        # Aksi perubahan data akun
        self.ui.submit_nama_baru.clicked.connect(self.edit_nama)
        self.ui.submit_alamat_baru.clicked.connect(self.edit_alamat)
        self.ui.submit_nomor_telepon_baru.clicked.connect(self.edit_nomor_telepon)
        self.ui.submit_password_baru.clicked.connect(self.ganti_password)
        
    def set_user(self):
        """Menyetel user aktif berdasarkan sesi login."""
        self.user = self.main_app.current_user  

    # ======================== Navigasi Dashboard Akun ========================

    def show_home(self):
        """Menampilkan halaman utama Dashboard Akun."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.akun)

    def show_lihat_informasi_akun(self):
        """Menampilkan informasi akun user yang sedang login."""
        self.set_user()  # Memastikan data user selalu terbaru
        self.ui.stackedWidget.setCurrentWidget(self.ui.lihat_informasi_akun)

        if not self.user:
            self.ui.lihat_informasi_akun_akun.setPlainText("User tidak ditemukan.")
            return

        info = (
            f"Nama: {self.user['nama_lengkap']}\n"
            f"Email: {self.user['email']}\n"
            f"Alamat: {self.user['alamat']}\n"
            f"Nomor Telepon: {self.user['nomor_telepon']}"
        )
        self.ui.lihat_informasi_akun_akun.setPlainText(info)

    def show_edit_informasi_akun(self):
        """Menampilkan halaman edit informasi akun."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.edit_informasi_akun)

    def show_ganti_password(self):
        """Menampilkan halaman ganti password."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.ganti_password)

    def show_informasi_aplikasi(self):
        """Menampilkan informasi tentang aplikasi."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.informasi_aplikasi)
        self.ui.informasi_aplikasi_akun.setText(
            """
            Nama Aplikasi: SAKAPEUNG!
            Deskripsi: Platform beli tiket kereta api terbaik!
            Versi: 1.0
            """
        )

    def show_pusat_bantuan(self):
        """Menampilkan informasi kontak pusat bantuan."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.pusat_bantuan)
        self.ui.pusat_bantuan_akun.setText(
            """
            Email: cs@sakapeung.com
            Nomor Telepon: 021-120
            SMS: 021120
            Website: www.sakapeung.com/help
            """
        )

    # ======================== Pengelolaan Data User ========================

    def load_users(self):
        """Memuat data pengguna dari file JSON."""
        try:
            with open(USER_DATABASE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_users(self, users):
        """Menyimpan data pengguna ke file JSON."""
        with open(USER_DATABASE, "w") as file:
            json.dump(users, file, indent=4)

    def edit_nama(self):
        """Mengubah nama pengguna dan memperbaruinya di database."""
        new_name = self.ui.nama_baru_input.text().strip().title()
        if new_name:
            users = self.load_users()
            for user in users:
                if user["email"] == self.main_app.current_user["email"]:
                    user["nama_lengkap"] = new_name
                    self.save_users(users)
                    self.main_app.current_user["nama_lengkap"] = new_name
                    QMessageBox.information(self, "Sukses", "Nama berhasil diperbarui!")
                    return
        QMessageBox.warning(self, "Error", "Nama tidak boleh kosong!")

    def edit_alamat(self):
        """Mengubah alamat pengguna dan memperbaruinya di database."""
        new_address = self.ui.alamat_baru_input.text().strip()
        if new_address:
            users = self.load_users()
            for user in users:
                if user["email"] == self.main_app.current_user["email"]:
                    user["alamat"] = new_address
                    self.save_users(users)
                    self.main_app.current_user["alamat"] = new_address
                    QMessageBox.information(self, "Sukses", "Alamat berhasil diperbarui!")
                    return
        QMessageBox.warning(self, "Error", "Alamat tidak boleh kosong!")

    def edit_nomor_telepon(self):
        """Mengubah nomor telepon pengguna dengan validasi pola nomor yang benar."""
        new_phone = self.ui.no_telepon_baru_input.text().strip()
        if re.fullmatch(r"08\d{9,11}", new_phone):
            users = self.load_users()
            for user in users:
                if user["email"] == self.main_app.current_user["email"]:
                    user["nomor_telepon"] = new_phone
                    self.save_users(users)
                    self.main_app.current_user["nomor_telepon"] = new_phone
                    QMessageBox.information(self, "Sukses", "Nomor telepon berhasil diperbarui!")
                    return
        QMessageBox.warning(self, "Error", "Nomor telepon harus terdiri dari 11-13 digit dan diawali dengan '08'!")

    def ganti_password(self):
        """Mengganti password pengguna dengan validasi password lama dan format keamanan."""
        current_password = hash_password(self.ui.password_lama_input.text().strip())
        new_password = self.ui.password_baru_input.text().strip()
        confirm_password = self.ui.konfirmasi_password_baru_input.text().strip()

        password_pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(password_pattern, new_password):
            QMessageBox.warning(self, "Error", "Password harus minimal 8 karakter, mengandung 1 huruf besar, 1 angka, dan 1 simbol!")
            return

        users = self.load_users()
        for user in users:
            if user["email"] == self.main_app.current_user["email"]:
                if user["password"] != current_password:
                    QMessageBox.warning(self, "Error", "Password lama salah!")
                    return
                if new_password != confirm_password:
                    QMessageBox.warning(self, "Error", "Password baru tidak cocok!")
                    return
                user["password"] = hash_password(new_password)
                self.save_users(users)
                self.main_app.current_user["password"] = user["password"]
                QMessageBox.information(self, "Sukses", "Password berhasil diubah!")
                return
        QMessageBox.warning(self, "Error", "Terjadi kesalahan saat mengganti password!")

    # ======================== Logout dan Navigasi ========================

    def logout(self):
        """Menghapus sesi user dan kembali ke halaman login."""
        self.main_app.current_user = None
        self.main_app.setCurrentWidget(self.main_app.login_screen)

    def goto_dashboard_user(self):
        """Kembali ke dashboard utama pengguna."""
        self.main_app.setCurrentWidget(self.main_app.dashboard_user)