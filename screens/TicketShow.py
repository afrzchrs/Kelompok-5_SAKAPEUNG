import sys, os
from PyQt5.QtWidgets import QWidget,QTableWidgetItem, QMessageBox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui')))
from ui.ticket_show import Ui_tiket_show_box

# ========================== KELAS UTAMA UNTUK MENAMPILKAN TIKET YANG TERSEDIA ==========================
class TicketShow(QWidget):
    def __init__(self, main_app):
        super().__init__()

        self.ui = Ui_tiket_show_box()
        self.ui.setupUi(self)
        self.setWindowTitle("Hasil Pencarian Tiket")
        self.main_app = main_app  # Menyimpan referensi ke aplikasi utama

        # =============================== NAVIGASI ================================
        self.ui.table_pesan_tiket.cellClicked.connect(self.pilih_tiket)
        self.ui.button_keluar.clicked.connect(self.kembali_ke_search)

    def tampilkan_tiket(self, tiket_list):
        """Menampilkan tiket dalam tabel atau menampilkan notifikasi jika tiket tidak tersedia."""
        
        self.ui.table_pesan_tiket.setRowCount(0)

        if not tiket_list:
            QMessageBox.warning(self, "Tiket Tidak Tersedia", "Maaf, tidak ada tiket yang tersedia untuk pencarian ini.")
            return  

        self.ui.table_pesan_tiket.setRowCount(len(tiket_list))
        self.tiket_list = tiket_list  # Simpan daftar tiket

        for row, tiket in enumerate(tiket_list):
            self.ui.table_pesan_tiket.setItem(row, 0, QTableWidgetItem(tiket['nama_kereta']))
            self.ui.table_pesan_tiket.setItem(row, 1, QTableWidgetItem(tiket['asal']))
            self.ui.table_pesan_tiket.setItem(row, 2, QTableWidgetItem(tiket['tujuan']))
            self.ui.table_pesan_tiket.setItem(row, 3, QTableWidgetItem(tiket['waktu_berangkat']))
            self.ui.table_pesan_tiket.setItem(row, 4, QTableWidgetItem(tiket['waktu_tiba']))
            self.ui.table_pesan_tiket.setItem(row, 5, QTableWidgetItem(f"Rp {tiket['harga']}"))

    def pilih_tiket(self, row):
        """Fungsi dipanggil ketika user memilih tiket dari tabel."""
        if row < 0 or row >= len(self.tiket_list):
            print("Baris tiket tidak valid!")
            return

        tiket_terpilih = self.tiket_list[row]
        print(f"Tiket yang dipilih: {tiket_terpilih}")   
        try:
            self.main_app.open_detail_pemesanan(tiket_terpilih)
            print(" Berhasil memanggil open_detail_pemesanan")  
        except Exception as e:
            print(f"Error saat memanggil open_detail_pemesanan: {e}")

    def kembali_ke_search(self):
        """Navigasi kembali ke halaman TicketSearch."""
        self.main_app.setCurrentWidget(self.main_app.ticket_search_screen)


