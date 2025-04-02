
import json, os
from PyQt5.QtWidgets import QWidget, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy
from ui.bookingkursi_bisnis import Ui_kereta_bisnis
from ui.bookingkursi_ekonomi import Ui_kereta_ekonomi
from ui.bookingkursi_eksekutif import Ui_kereta_eksekutif

# ====================================== PATH DATABASE ===========================================
KURSI_KERETA_FILE = "databases/kursi_kereta.json"

# ============================= KELAS UTAMA DALAM BOOKING KURSI ==================================
class BookingKursi(QWidget):
    def __init__(self, main_app, tiket_terpilih):
        super().__init__()
        self.main_app = main_app
        self.tiket_terpilih = tiket_terpilih
        self.selected_seat = None
        self.ui = None 

        self.setup_ui_for_ticket()

    def setup_ui_for_ticket(self):
        self.selected_seat = None 
        self.load_ui_based_on_service()
        
        if self.ui:
            self.ui.setupUi(self)
            self.ui.nama_kereta.setText(self.tiket_terpilih.get('nama_kereta', ''))
            
            # ============================= NAVIGASI ================================
            self.ui.comboBox.currentIndexChanged.connect(self.update_kursi_display)
            self.ui.button_pilihkursi.clicked.connect(self.confirm_booking)
            self.ui.button_keluar.clicked.connect(self.kembali_ke_detail_pemesanan)
            
            self.load_gerbong()

    def load_ui_based_on_service(self):
        layanan = self.tiket_terpilih.get('jenis_layanan', '').lower()
        if layanan == 'eksekutif':
            self.ui = Ui_kereta_eksekutif()
        elif layanan == 'bisnis':
            self.ui = Ui_kereta_bisnis()
        elif layanan == 'ekonomi':
            self.ui = Ui_kereta_ekonomi()
        else:
            print(f"Jenis layanan tidak dikenal: {layanan}")
        
    def load_gerbong(self):
        gerbong_list = []
        try:
            with open(KURSI_KERETA_FILE, 'r') as file:
                data = json.load(file)

            for kereta in data:
                if kereta.get('id_kereta') == self.tiket_terpilih.get('id_kereta') and \
                kereta.get('tanggal') == self.tiket_terpilih.get('tanggal'):
                    for gerbong in kereta.get('gerbong', []):
                        gerbong_list.append(gerbong.get('gerbong_id'))

            if gerbong_list:
                self.ui.comboBox.clear()
                self.ui.comboBox.addItems(gerbong_list)
                self.update_kursi_display() 
            else:
                print(f"Tidak ada gerbong yang tersedia untuk kereta: {self.tiket_terpilih.get('nama_kereta')}")
        except Exception as e:
            print(f"Error saat memuat gerbong: {e}")

    def update_kursi_display(self):
        self.clear_kursi()
        gerbong_id = self.ui.comboBox.currentText()
        if not gerbong_id:
            return

        try:
            with open(KURSI_KERETA_FILE, 'r') as file:
                data = json.load(file)

            for kereta in data:
                if kereta.get('id_kereta') == self.tiket_terpilih.get('id_kereta') and \
                kereta.get('tanggal') == self.tiket_terpilih.get('tanggal'):
                    for gerbong in kereta.get('gerbong', []):
                        if gerbong.get('gerbong_id') == gerbong_id:
                            self.display_kursi(gerbong.get('kursi', {}))
                            return
            
            print(f"Tidak ditemukan kereta/gerbong yang sesuai untuk ID: {self.tiket_terpilih.get('id_kereta')}, gerbong: {gerbong_id}")
        except Exception as e:
            print(f"Error saat memperbarui kursi: {e}")

    def clear_kursi(self):
        if not hasattr(self, 'ui') or not self.ui:
            return
            
        layout = self.ui.gridLayout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def display_kursi(self, kursi_data):
        # ========================== space kursi ========================
        self.ui.gridLayout.setSpacing(15)  
        row = 0
        for seat_index in range(1, 14):
            # Kursi A
            seat_A = f"A{seat_index}"
            checkbox_A = QCheckBox(seat_A)
            checkbox_A.setEnabled(kursi_data.get(seat_A, True))
            checkbox_A.stateChanged.connect(lambda state, s=seat_A: self.handle_seat_selection(state, s))
            self.ui.gridLayout.addWidget(checkbox_A, row, 0)

            # Spacer antar Kursi A dan B
            spacer_ab = QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
            self.ui.gridLayout.addItem(spacer_ab, row, 1)

            # Kursi B
            seat_B = f"B{seat_index}"
            checkbox_B = QCheckBox(seat_B)
            checkbox_B.setEnabled(kursi_data.get(seat_B, True))
            checkbox_B.stateChanged.connect(lambda state, s=seat_B: self.handle_seat_selection(state, s))
            self.ui.gridLayout.addWidget(checkbox_B, row, 2)

            # Spacer Tengah
            spacer_tengah = QSpacerItem(200, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.ui.gridLayout.addItem(spacer_tengah, row, 3)

            # Kursi C
            seat_C = f"C{seat_index}"
            checkbox_C = QCheckBox(seat_C)
            checkbox_C.setEnabled(kursi_data.get(seat_C, True))
            checkbox_C.stateChanged.connect(lambda state, s=seat_C: self.handle_seat_selection(state, s))
            self.ui.gridLayout.addWidget(checkbox_C, row, 4)

            # Spacer antar Kursi C dan D
            spacer_cd = QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
            self.ui.gridLayout.addItem(spacer_cd, row, 5)

            # Kursi D
            seat_D = f"D{seat_index}"
            checkbox_D = QCheckBox(seat_D)
            checkbox_D.setEnabled(kursi_data.get(seat_D, True))
            checkbox_D.stateChanged.connect(lambda state, s=seat_D: self.handle_seat_selection(state, s))
            self.ui.gridLayout.addWidget(checkbox_D, row, 6)

            row += 1
                
        # Memastikan tampilan diperbarui
        self.ui.gridLayout.update()
        self.ui.widget_container_kursi.adjustSize()
        self.ui.scrollArea_kursi.ensureVisible(0, 0)

    def handle_seat_selection(self, state, seat):
        if state == 2:  # Checked
            if self.selected_seat:
                QMessageBox.warning(self, "Peringatan", "Anda hanya dapat memilih satu kursi untuk 1 penumpang!")
                self.sender().setChecked(False)
            else:
                self.selected_seat = seat
        else:
            if self.selected_seat == seat:
                self.selected_seat = None

    def confirm_booking(self):
        if not self.selected_seat:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih kursi terlebih dahulu!")
            return
        
        # menyimpan ID kursi yang dipilih ke dalam tiket_terpilih (TAPI BELUM UPDATE DATABASE)
        self.tiket_terpilih['id_kursi'] = self.selected_seat
        self.tiket_terpilih['gerbong_id'] = self.ui.comboBox.currentText()  

        QMessageBox.information(self, "Kursi Dipilih", f"Kursi {self.selected_seat} telah dipilih. Lanjutkan ke pembayaran.")

        self.main_app.open_pembayaran(self.tiket_terpilih)

    def kembali_ke_detail_pemesanan(self):
        self.main_app.setCurrentWidget(self.main_app.detail_pemesanan_screen)
    
    def update_ticket(self, tiket_terpilih):
        """Memperbarui tiket saat ini dan memperbarui semua elemen UI"""
        print("update_ticket() dipanggil!")
        if not tiket_terpilih:
            print("Error: tiket_terpilih kosong!")
            return

        self.tiket_terpilih = tiket_terpilih
        self.reset_input()
        self.setup_ui_for_ticket()

        if hasattr(self.ui, 'nama_kereta'):
            self.ui.nama_kereta.setText(self.tiket_terpilih.get('nama_kereta', ''))
            
    def reset_input(self):
        """Reset semua input dan elemen UI ke keadaan default"""
        self.selected_seat = None  # Hapus kursi yang dipilih
        
        if hasattr(self, 'ui') and self.ui:
            # Bersihkan combobox dan tampilan kursi
            if hasattr(self.ui, 'comboBox'):
                self.ui.comboBox.clear()
            
            self.clear_kursi()
            
            # Perbarui nama kereta jika diperlukan
            if hasattr(self.ui, 'nama_kereta'):
                self.ui.nama_kereta.setText(self.tiket_terpilih.get('nama_kereta', ''))
