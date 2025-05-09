"""
Author: Devi Maulani
NIM: 241524007
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung

"""

import sys, json, os
from PyQt5.QtWidgets import  QDialog, QCalendarWidget, QPushButton, QVBoxLayout,QMessageBox
from PyQt5.QtCore import QDate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.ticket_search import Ui_TICKETBOOKING 
from PyQt5.QtCore import QDate

# ================================ PATH DATABASE =================================
JADWAL_KERETA_FILE = "databases/jadwal_kereta.json"
INFORMASI_UMUM_FILE = "databases/informasi_umum.json"
KURSI_KERETA_FILE = "databases/kursi_kereta.json"

# ========================== KELAS UTAMA PENCARIAN TIKET ==========================
class TicketSearch(QDialog):
    def __init__(self, main_app,ticket_show):
        super().__init__()

        # Memuat UI dari Qt Designer
        self.ui = Ui_TICKETBOOKING()
        self.ui.setupUi(self)  # akan Menghubungkan UI ke class
        self.main_app = main_app  # meimpan referensi ke MainApp
        self.ticket_show = ticket_show  # menymimpan referensi ke TicketShow

        # ========================== NAVIGASI ==========================
        self.ui.pushButton_Swap.clicked.connect(self.swap_stations)
        self.ui.button_cari.clicked.connect(self.cari_tiket)
        self.ui.button_tanggal.clicked.connect(self.show_calendar)
        self.ui.button_keluar.clicked.connect(self.kembali_ke_dashboard)

        # Mengisi dropdown stasiun asal & tujuan serta jenis layanan dengan data dari JSON
        self.populate_stations()
        self.populate_layanan()

    # Fungsi untuk membaca file JSON
    @staticmethod
    def load_json(file_path):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print(f"Error membaca file {file_path}")
                    return []
        return []
    
    def populate_stations(self):
        """Mengisi dropdown stasiun asal dan tujuan dengan daftar unik stasiun transit dari data JSON."""

        data = self.load_json(JADWAL_KERETA_FILE)
        # menggunakan array sementara untuk menyimpan daftar stasiun transit
        stasiun_transit_list = []

        for kereta in data:
            transit = kereta.get("stasiun_transit", [])
            stasiun_transit_list.extend(transit) #tergantung dari bagaimana cara penulisannya dalam database

        stasiun_transit_list = sorted(set(stasiun_transit_list))
        
        self.ui.combo_asal.clear()
        self.ui.combo_tujuan.clear()

        # memasukkan data ke dalam dropdown
        self.ui.combo_asal.addItems(stasiun_transit_list)
        self.ui.combo_tujuan.addItems(stasiun_transit_list)


    def populate_layanan(self):
        """Mengisi dropdown jenis layanan dengan daftar unik dari informasi umum."""
        
        data = self.load_json(INFORMASI_UMUM_FILE)
        # array sementara untuk menyimpan daftar layanan unik
        layanan_list = []

        for kereta in data:
            layanan = kereta.get("jenis_layanan", "")
            if layanan:  
                layanan_list.append(layanan)

        # mengahapus duplikasi dan megurutkannya, serta memasukan kedalam dropdown 
        layanan_list = sorted(set(layanan_list))
        self.ui.combo_layanan.clear()
        self.ui.combo_layanan.addItems(layanan_list)

    def swap_stations(self):
        """Menukar nilai dropdown stasiun asal dan tujuan"""
        asal = self.ui.combo_asal.currentText()
        tujuan = self.ui.combo_tujuan.currentText()
        self.ui.combo_asal.setCurrentText(tujuan)
        self.ui.combo_tujuan.setCurrentText(asal)

    def show_calendar(self):
        """Menampilkan kalender untuk memilih tanggal keberangkatan"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Masukan Tanggal")

        # Widget kalender
        calendar = QCalendarWidget(dialog)
        calendar.setGridVisible(True)
        calendar.setSelectedDate(QDate.currentDate())

        calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: #ffffff;
                background-color: #f8f9fa;
                color: #000;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton {
                background-color: #0078D7;
                color: white;
                border-radius: 3px;
                margin: 2px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #0056b3;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #004494;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #0078D7;
                selection-color: white;
            }
            QCalendarWidget QTableView QHeaderView::section {
                background-color: #0078D7;
                color: white;
                border-radius: 2px;
                padding: 3px;
            }
            QCalendarWidget QSpinBox {
                background: white;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Fungsi untuk menetapkan tanggal yang dipilih
        def set_date():
            selected_date = calendar.selectedDate()
            current_date = QDate.currentDate()

            if selected_date < current_date:
                QMessageBox.warning(dialog, "Tanggal Tidak Valid", "Anda tidak dapat memilih tanggal yang telah lewat!")
            else:
                # Format tanggal menyesaikan database
                formatted_date = selected_date.toString("yyyy-MM-dd")
                self.ui.button_tanggal.setText(formatted_date)
                dialog.accept()

        button_ok = QPushButton("OK", dialog)
        button_ok.clicked.connect(set_date)

        layout = QVBoxLayout()
        layout.addWidget(calendar)
        layout.addWidget(button_ok)
        dialog.setLayout(layout)
        dialog.exec_()

    def cari_tiket(self):
        """Mencari tiket berdasarkan input pengguna dan menampilkan di TicketShow."""
        try:
            asal = self.ui.combo_asal.currentText()
            tujuan = self.ui.combo_tujuan.currentText()
            tanggal_str = self.ui.button_tanggal.text()
            pilihan_layanan = self.ui.combo_layanan.currentText()  
            
            """print("DEBUG: Mulai pencarian tiket...")
            print(f"Stasiun asal: {asal}, tujuan: {tujuan}, tanggal: {tanggal_str}")
            print(f"Pilihan layanan pengguna: {pilihan_layanan}")"""

            if asal == tujuan:
                QMessageBox.warning(self, "Error", "Stasiun asal dan tujuan tidak boleh sama!")
                return

            # mengechek rute valid (ada atau tidak pada database) 
            jadwal_data = self.load_json(JADWAL_KERETA_FILE)
            valid_trip = False
            for jadwal in jadwal_data:
                stasiun_transit = jadwal.get("stasiun_transit", [])
                if asal in stasiun_transit and tujuan in stasiun_transit:
                    if stasiun_transit.index(asal) < stasiun_transit.index(tujuan):
                        valid_trip = True
                        break
            if not valid_trip:
                QMessageBox.warning(self, "Error", "Rute perjalanan tidak ditemukan!")
                return
                
            # Validasi tanggal
            selected_date = QDate.fromString(tanggal_str, "yyyy-MM-dd")
            current_date = QDate.currentDate()
            if selected_date < current_date:
                QMessageBox.warning(self, "Tanggal Tidak Valid", "Anda tidak dapat memilih tanggal yang telah lewat!")
                return

            # Mulai mencari tiket yang tersedia
            hasil_pencarian = []
            for jadwal in jadwal_data:
                id_kereta = jadwal["id_kereta"]
                stasiun_transit = jadwal["stasiun_transit"]
                waktu_transit = jadwal["waktu_transit"]

                if asal in stasiun_transit and tujuan in stasiun_transit:
                    idx_asal = stasiun_transit.index(asal)
                    idx_tujuan = stasiun_transit.index(tujuan)

                    if idx_asal < idx_tujuan:
                        info_kereta = next((info for info in self.load_json(INFORMASI_UMUM_FILE) if info["id_kereta"] == id_kereta), None)
                        if not info_kereta:
                            continue  
                            
                        harga = info_kereta.get("harga_tiket", "Tidak diketahui")
                        layanan = info_kereta.get("jenis_layanan", "Tidak diketahui")

                        # mengechek ketersediaan kursi
                        kursi_tersedia = any(
                            kursi["id_kereta"] == id_kereta and kursi["tanggal"] == tanggal_str
                            for kursi in self.load_json(KURSI_KERETA_FILE)
                        )

                        # menyeleksi berdasarkan layanan yang dipilih
                        if layanan == pilihan_layanan and kursi_tersedia:
                            tiket = {
                                "nama_kereta": info_kereta["nama_kereta"],
                                "id_kereta": info_kereta["id_kereta"],
                                "asal": asal,
                                "tujuan": tujuan,
                                "waktu_berangkat": waktu_transit[idx_asal],
                                "waktu_tiba": waktu_transit[idx_tujuan],
                                "tanggal": tanggal_str,
                                "harga": harga,
                                "jenis_layanan": layanan
                            }
                            hasil_pencarian.append(tiket)
            
            # menampilkan hasil atau beri peringatan (MassageBox) jika tidak ada tiket
            if hasil_pencarian:
                self.main_app.ticket_show_screen.tampilkan_tiket(hasil_pencarian)
                self.main_app.setCurrentWidget(self.ticket_show)  
            else:
                QMessageBox.warning(self, "Tiket Tidak Tersedia", "Maaf, tidak ada tiket yang tersedia untuk pencarian ini.")
                self.main_app.ticket_show_screen.tampilkan_tiket([])
                self.main_app.setCurrentWidget(self.ticket_show)

        except Exception as e:
            print(f"ERROR: {e}") 

    def reset_input(self):

        # ============== reset input pada halaman pencarian tiket (mengubahnya menjadi default kembali) ==============
        if self.ui.combo_asal.count() > 0:
            self.ui.combo_asal.setCurrentIndex(0)
        if self.ui.combo_tujuan.count() > 0:
            self.ui.combo_tujuan.setCurrentIndex(0)

        self.ui.button_tanggal.setText("Masukan Tanggal")

        if self.ui.combo_layanan.count() > 0:
            self.ui.combo_layanan.setCurrentIndex(0)

    def kembali_ke_dashboard(self):
        """Kembali ke dashboard utama"""
        self.main_app.setCurrentWidget(self.main_app.dashboard_user)

        
        
    

     


    

            
  


    



        
        
    

     


    

            
  


    


