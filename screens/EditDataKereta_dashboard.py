"""
Author: Afriza Choirie Saputra
NIM: 241524002
Kelas: 1A
Prodi: Sarjana Terapan Teknik Informatika
Jurusan: Teknik Komputer dan Informatika
Politeknik Negeri Bandung
"""

import json
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from ui.dashboard_editDataKereta import Ui_dashboard_admin_Edit_Data as DashboardAdminEditData

INFOUMUM_DATABASE = "databases/informasi_umum.json"
JADWALKERETA_DATABASE = "databases/jadwal_kereta.json"
KURSIKERETA_DATABASE = "databases/kursi_kereta.json"
FORMATGERBONG = "databases/formatGerbong.json"

class DashboardEditData(QtWidgets.QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.ui = DashboardAdminEditData()
        self.ui.setupUi(self)
        self.main_app = main_app
        self.setWindowTitle("Admin Jadwal Kereta")
        self.setup_connections()
        
        # Load Data
        self.data = []
        self.load_data()
        
    # ======================== Navigasi Dashboard Edit Data Kereta ========================
    
    def setup_connections(self):
        self.ui.Lihat_Data_Kereta.clicked.connect(self.Lihat_Jadwal_kereta)
        self.ui.Tambah_Data_kereta.clicked.connect(self.Tambah_Jadwal_kereta)
        self.ui.Edit_Data_kereta.clicked.connect(self.Edit_Jadwal_kereta)
        self.ui.Hapus_Data_Kereta.clicked.connect(self.Hapus_Jadwal_kereta)
        self.ui.Dashboard_Utama.clicked.connect(self.Go_to_Main)
        
        self.ui.tombol_tambah_data.clicked.connect(self.tambah_data_kereta)
        self.ui.tombol_edit_data.clicked.connect(self.edit_data_kereta)
        self.ui.Cari_KeretaYangDihapus.clicked.connect(self.search_train_by_id)
        self.ui.tombol_hapus_data.clicked.connect(self.hapus_data_kereta)
        self.ui.tombol_batal.clicked.connect(self.reset_table)
        self.ui.tombol_seacrh_id_Lihat_Jadwal.clicked.connect(self.search_train_by_jenis_layanan)
        self.ui.tombol_reset_form_lihaJadwal_2.clicked.connect(self.reset_table)
        self.ui.tombol_reset_form_lihaJadwal.clicked.connect(self.reset_form_tambah_data)
        self.ui.tombol_reset_form.clicked.connect(self.reset_form_edit_data)
    
    def Lihat_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Lihat_jadwal_kereta)
    def Tambah_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Tambah_jadwal_kereta)
    def Edit_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Edit_jadwal_kereta)
    def Hapus_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Hapus_jadwal_kereta)
    def Go_to_Main(self):
        self.main_app.setCurrentWidget(self.main_app.dashboard_admin)
        
    # ============================== Pengelolaan Data Kereta ==============================
    
    def load_data(self):
        combined_data = {}

        for db_path in [INFOUMUM_DATABASE, JADWALKERETA_DATABASE, KURSIKERETA_DATABASE, FORMATGERBONG]:
            if not os.path.exists(db_path):
                QtWidgets.QMessageBox.critical(self, "Error", f"Database {db_path} tidak ditemukan.")
                return
            
            try:
                with open(db_path, "r") as file:
                    data = json.load(file)
                    for kereta in data:
                        id_kereta = kereta.get("id_kereta")
                        if id_kereta:
                            if id_kereta not in combined_data:
                                combined_data[id_kereta] = {}
                            combined_data[id_kereta].update(kereta)
            except json.JSONDecodeError:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database {db_path} rusak atau tidak dapat dibaca.")
                return
        
        self.data = list(combined_data.values())
        self.populate_table(self.data)
    
    def save_data(self, data):
        
        # MEMISAHKA DATA
        informasi_umum_data = []
        jadwal_kereta_data = []
        kursi_kereta_data = []

        for kereta in data:
            id_kereta = kereta.get("id_kereta")

            # Cek dan tambahkan ke informasi umum
            if "nama_kereta" in kereta and "jenis_layanan" in kereta and "harga_tiket" in kereta:
                informasi_umum_data.append({
                    "id_kereta": id_kereta,
                    "nama_kereta": kereta["nama_kereta"],
                    "jenis_layanan": kereta["jenis_layanan"],
                    "harga_tiket": kereta["harga_tiket"] 
                })

            # Cek dan tambahkan ke jadwal kereta
            if "stasiun_transit" in kereta and "waktu_transit" in kereta:
                jadwal_kereta_data.append({
                    "id_kereta": id_kereta,
                    "stasiun_transit": kereta["stasiun_transit"],
                    "waktu_transit": kereta["waktu_transit"]
                })

            # Cek dan tambahkan ke kursi kereta
            if "tanggal" in kereta and "gerbong" in kereta:
                kursi_kereta_data.append({
                    "id_kereta": id_kereta,
                    "tanggal": kereta["tanggal"],
                    "gerbong": kereta["gerbong"]
                })

        # Simpan data kembali ke file masing-masing
        file_mapping = {
            INFOUMUM_DATABASE: informasi_umum_data,
            JADWALKERETA_DATABASE: jadwal_kereta_data,
            KURSIKERETA_DATABASE: kursi_kereta_data,
        }

        for db_path, content in file_mapping.items():
            try:
                with open(db_path, "w", encoding="utf-8") as file:
                    json.dump(content, file, indent=4)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menyimpan ke {db_path}: {str(e)}")
                return
            
    def reset_table(self):
        self.ui.input_id_Hapus_kereta.clear()
        self.ui.input_JenisLayananLihat_Jadwal.clear()
        self.ui.tableWidget_Li.clearContents()  
        self.ui.tableWidget_Li.setRowCount(0) 
        self.ui.tableWidget_Hapus_Data.clearContents() 
        self.ui.tableWidget_Hapus_Data.setRowCount(0)
        self.load_data() 
        
    def reset_form_tambah_data(self):
        self.ui.input_nama_kereta_TambahData.clear()    
        self.ui.input_Jenis_layanan_TambahData.clear()
        self.ui.input_Stasiun_Transit_TambahData.clear()
        self.ui.input_Waktu_Operasional_TambahData.clear()
        self.ui.input_Tarif_Tiket_TambahData.clear()
        self.ui.dateEdit_TambahData.setDate(QDate.currentDate()) 
        self.ui.input_Jumla_Gerbong_TambahData.clear()

    def reset_form_edit_data(self):
        self.ui.input_id_kereta_EditData.clear()
        self.ui.input_nama_kereta_EditData.clear()
        self.ui.input_nama_kereta_JenisLayanan.clear()
        self.ui.input_staisun_transit_EditData.clear()
        self.ui.input_waktu_transit_EditData.clear()
        self.ui.input_tarif_tiket_EditData.clear()
        self.ui.dateEdit_TambahData_2.setDate(QDate.currentDate()) 
        self.ui.input_jumlah_gerbong_EdiData.clear()

        
    def populate_table(self, data):
        #Mengisi tabel dengan data kereta, menampilkan stasiun dan waktu transit dalam format vertikal.
        current_rows = self.ui.tableWidget_Li.rowCount()  # Ambil jumlah baris saat ini
        new_rows = sum(len(kereta.get("stasiun_transit", [])) for kereta in data)  # Hitung total baris tambahan
        total_rows = current_rows + new_rows  # Total baris setelah penambahan data

        self.ui.tableWidget_Li.setRowCount(total_rows)
        self.ui.tableWidget_Li.setColumnCount(6)  # 6 Kolom: ID, Nama, Tanggal, Jenis Layanan, Stasiun, Waktu

        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Jenis Layanan", "Stasiun Transit", "Waktu Transit"]
        self.ui.tableWidget_Li.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_Li.verticalHeader().setVisible(False)

        row = current_rows  # Mulai dari baris terakhir yang ada
        for kereta in data:
            id_kereta = kereta.get("id_kereta", "-")
            nama_kereta = kereta.get("nama_kereta", "-")
            tanggal = kereta.get("tanggal", "-")
            jenis_layanan = kereta.get("jenis_layanan", "-")
            stasiun_transit = kereta.get("stasiun_transit", [])
            waktu_transit = kereta.get("waktu_transit", [])

            span_count = len(stasiun_transit)  # Hitung jumlah baris yang harus digabung

            for i in range(len(stasiun_transit)):
                self.ui.tableWidget_Li.setItem(row, 4, QtWidgets.QTableWidgetItem(stasiun_transit[i]))
                self.ui.tableWidget_Li.setItem(row, 5, QtWidgets.QTableWidgetItem(waktu_transit[i] if i < len(waktu_transit) else "-"))
                row += 1
                
            first_row = row - span_count
            self.ui.tableWidget_Li.setItem(first_row, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.tableWidget_Li.setItem(first_row, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.tableWidget_Li.setItem(first_row, 2, QtWidgets.QTableWidgetItem(tanggal))
            self.ui.tableWidget_Li.setItem(first_row, 3, QtWidgets.QTableWidgetItem(jenis_layanan))

            self.ui.tableWidget_Li.setSpan(first_row, 0, span_count, 1)  # ID Kereta
            self.ui.tableWidget_Li.setSpan(first_row, 1, span_count, 1)  # Nama Kereta
            self.ui.tableWidget_Li.setSpan(first_row, 2, span_count, 1)  # Tanggal
            self.ui.tableWidget_Li.setSpan(first_row, 3, span_count, 1)  # Jenis layanan

        self.ui.tableWidget_Li.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_Li.resizeRowsToContents()
        
    def validasi_input(self, **kwargs):
        #VALIDASI INPUT TAK BOLEH KOSONG
        for key, value in kwargs.items():
            if not value:
                QtWidgets.QMessageBox.warning(self, "Peringatan", f"Kolom {key.replace('_', ' ').title()} harus diisi!")
                return False
        return True

    def validasi_angka(self, harga, jumlah_gerbong):
        #VALIDASI HARGA DAN JUMLAH GERBONG HARUS ANGKA
        try:
            harga = float(harga)
            jumlah_gerbong = int(jumlah_gerbong)
            if jumlah_gerbong <= 0:
                raise ValueError
            return harga, jumlah_gerbong
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Jumlah gerbong dan harga harus berupa angka yang valid!")
            return None, None

    def validasi_stasiun_waktu(self, stasiun, waktu):
        #VALIDASI JUMLAH STASIUN DAN WAKTU TRANSIT
        stasiun_list = [s.strip() for s in stasiun.split(",") if s.strip()]
        waktu_list = [w.strip() for w in waktu.split(",") if w.strip()]
        if len(stasiun_list) != len(waktu_list):
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Jumlah stasiun transit dan waktu transit harus sama!")
            return None, None
        return stasiun_list, waktu_list

    def load_format_gerbong(self, jenis_layanan):
        #LOAD FORMAT GERBONG BERDASARKAN JENIS LAYANAN
        try:
            with open(FORMATGERBONG, "r", encoding="utf-8") as file:
                format_gerbong_data = json.load(file)

            # Cari format gerbong yang sesuai
            return next((fg for fg in format_gerbong_data if fg["jenis_layanan"] == jenis_layanan), None)

        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def generate_gerbong(self, id_kereta, jumlah_gerbong, format_terpilih):
        #MEMBUAT FORMAT GERBONG
        return [
            {
                "gerbong_id": f"{id_kereta}-G{i}",
                "kapasitas": format_terpilih["kapasitas"],
                "kursi": format_terpilih["kursi"].copy()
            }
            for i in range(1, jumlah_gerbong + 1)
        ]
        
    def tambah_data_kereta(self):
        #INPUT UI
        nama = self.ui.input_nama_kereta_TambahData.text().strip()
        layanan = self.ui.input_Jenis_layanan_TambahData.text().strip()
        stasiun = self.ui.input_Stasiun_Transit_TambahData.text().strip()
        waktuTransit = self.ui.input_Waktu_Operasional_TambahData.text().strip()
        harga = self.ui.input_Tarif_Tiket_TambahData.text().strip()
        tanggal = self.ui.dateEdit_TambahData.date().toString('yyyy-MM-dd')
        jumlah_gerbong = self.ui.input_Jumla_Gerbong_TambahData.text().strip()

        stasiun_transit_list, waktu_transit_list = self.validasi_stasiun_waktu(stasiun, waktuTransit)
        if stasiun_transit_list is None:
            return
        
        if not self.validasi_input(nama=nama, layanan=layanan, harga=harga, jumlah_gerbong=jumlah_gerbong, stasiun=stasiun, waktu=waktu_transit_list):
            return
        
        harga, jumlah_gerbong = self.validasi_angka(harga, jumlah_gerbong)
        if harga is None:
            return
        

        # MUAT DATA YANG ADA
        self.load_data()  
        data = self.data if hasattr(self, "data") else []

        # MEMBUAT ID BARU BERDASARKAN DATA YANG SUDAH ADA
        existing_ids = [int(d["id_kereta"][2:]) for d in data if d["id_kereta"].startswith("KA")]
        new_id_number = max(existing_ids, default=0) + 1
        id_kereta_baru = f"KA{new_id_number:03}"

        # MENAMBAHKAN DATA GERBONG SESUAI JENIS LAYANAN
        format_terpilih = self.load_format_gerbong(layanan)
        if not format_terpilih:
            QtWidgets.QMessageBox.critical(self, "Error", "Format gerbong untuk jenis layanan ini tidak ditemukan!")
            return

        gerbong_baru = self.generate_gerbong(id_kereta_baru, jumlah_gerbong, format_terpilih)

        # MENYIMPAN DATA BARU DENGAN FORMAT DATABASE
        informasi_umum_baru = {
            "id_kereta": id_kereta_baru,
            "nama_kereta": nama,
            "jenis_layanan": layanan,
            "harga_tiket": harga
        }

        jadwal_kereta_baru = {
            "id_kereta": id_kereta_baru,
            "stasiun_transit": stasiun_transit_list,  # Simpan sebagai list
            "waktu_transit": waktu_transit_list       # Simpan sebagai list
        }

        kursi_kereta_baru = {
            "id_kereta": id_kereta_baru,
            "tanggal": tanggal,
            "gerbong": gerbong_baru
        }

        # MENYIMPAN DATA KE DATABASE
        try:
            def update_database(file_path, new_entry):
                existing_data = []
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        existing_data = json.load(file)
                existing_data.append(new_entry)  # Tambahkan data baru
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(existing_data, file, indent=4)

            update_database(INFOUMUM_DATABASE, informasi_umum_baru)
            update_database(JADWALKERETA_DATABASE, jadwal_kereta_baru)
            update_database(KURSIKERETA_DATABASE, kursi_kereta_baru)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")
            return
        
        #PERBARUI TABEL
        self.ui.tableWidget_Li.clearContents()
        self.ui.tableWidget_Li.setRowCount(0)
        
        self.load_data()

        QtWidgets.QMessageBox.information(self, "Sukses", "Data kereta berhasil diperbarui!")

    def edit_data_kereta(self):
        # INPUT UI
        id_kereta = self.ui.input_id_kereta_EditData.text().strip().upper()
        nama_kereta = self.ui.input_nama_kereta_EditData.text().strip()
        jenis_layanan = self.ui.input_nama_kereta_JenisLayanan.text().strip()
        stasiun_transit = self.ui.input_staisun_transit_EditData.text().strip()
        waktu_transit = self.ui.input_waktu_transit_EditData.text().strip()
        harga_tiket = self.ui.input_tarif_tiket_EditData.text().strip()
        tanggal = self.ui.dateEdit_TambahData_2.date().toString('yyyy-MM-dd')
        jumlah_gerbong = self.ui.input_jumlah_gerbong_EdiData.text().strip()

        stasiun_transit_list, waktu_transit_list = self.validasi_stasiun_waktu(stasiun_transit, waktu_transit)
        if stasiun_transit_list is None:
            return
        
        if not self.validasi_input(id_kereta=id_kereta, nama=nama_kereta, layanan=jenis_layanan, harga=harga_tiket, jumlah_gerbong=jumlah_gerbong, stasiun=stasiun_transit, waktu=waktu_transit):
            return
        
        harga_tiket, jumlah_gerbong = self.validasi_angka(harga_tiket, jumlah_gerbong)
        if harga_tiket is None:
            return
        
        # MEMBUKA DATA
        self.load_data()
        data = self.data 

        # CARI DATA KERETA BERDASARKAN ID
        kereta_ditemukan = next((kereta for kereta in data if kereta["id_kereta"] == id_kereta), None)
        if not kereta_ditemukan:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "ID Kereta tidak ditemukan!")
            return

        # MEMBUAT PEMBARUAN DATA KERETA
        kereta_ditemukan.update({
            "nama_kereta": nama_kereta,
            "jenis_layanan": jenis_layanan,
            "harga_tiket": harga_tiket,
            "stasiun_transit": stasiun_transit_list,
            "waktu_transit": waktu_transit_list,
            "tanggal": tanggal,
        })

        # MEMPERBARUI GERBONG
        format_terpilih = self.load_format_gerbong(jenis_layanan)
        if not format_terpilih:
            QtWidgets.QMessageBox.critical(self, "Error", "Format gerbong untuk jenis layanan ini tidak ditemukan!")
            return

        kereta_ditemukan["gerbong"] = self.generate_gerbong(id_kereta, jumlah_gerbong, format_terpilih)

        # MENYIMPAN PERUBAHAN KE DATABASE
        self.save_data(data)
        
        # MEMBERSIHKAN TABEL
        self.ui.tableWidget_Li.clearContents()
        self.ui.tableWidget_Li.setRowCount(0)
        
        # MENGAMBIL DATA ULANG YANG TELAH DIPERBAHARUI
        self.load_data()

        QtWidgets.QMessageBox.information(self, "Sukses", "Data kereta berhasil diperbarui!")

    def hapus_data_kereta(self):
        id_kereta = self.ui.input_id_Hapus_kereta.text().strip().lower()
            
        # LOAD LAGI DATABASE
        self.load_data()
            
        #MENYIMPAN DATA YANG BARU LOAD 
        data = self.data

        # BUAT LIST BARU UNTUK SEMUA DATA KERETA KECUALI DATA YANG DIHAPUS
        updated_data = [k for k in data if k.get("id_kereta", "").lower() != id_kereta]

        # VALIDASI DATA YANG AKAN DIHAPUS
        if len(updated_data) == len(data):
            QtWidgets.QMessageBox.information(self, "Info", "Kereta dengan ID tersebut tidak ditemukan.")
            return

        # SIMPAN ULANG DATABASE SESUDAH PENGHAPUSAN
        self.save_data(updated_data)
            
        # LOAD ULANG SESUDAH PENGHAPUSAN
        self.load_data()
            
        # TAMPILAN LIHAT JADWAL DIPERBARUI
        self.populate_table(self.data)
        QtWidgets.QMessageBox.information(self, "Sukses", "Data kereta berhasil dihapus!")

    def search_train_by_jenis_layanan(self):
        # INPUT UI
        jenis_layanan = self.ui.input_JenisLayananLihat_Jadwal.text().strip().lower()
        
        # PERBARUI TABEL
        self.ui.tableWidget_Li.setRowCount(0)

        # FILTER DATA
        filtered_data = [k for k in self.data if k.get("jenis_layanan", "").strip().lower() == jenis_layanan]

        if not filtered_data:
            QtWidgets.QMessageBox.information(self, "Hasil Pencarian", "Tidak ada kereta yang ditemukan.")
        else:
            self.populate_table(filtered_data)

    def populate_table_hapus_data(self, filtered_data):
        total_rows = sum(len(kereta.get("stasiun_transit", [])) for kereta in filtered_data)
        
        self.ui.tableWidget_Hapus_Data.setRowCount(total_rows)
        self.ui.tableWidget_Hapus_Data.setColumnCount(6)  # 5 Kolom: ID, Nama, Tanggal, Stasiun, Waktu

        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Stasiun Transit", "Waktu Transit", "jenis layanan"]
        self.ui.tableWidget_Hapus_Data.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_Hapus_Data.verticalHeader().setVisible(False)

        row = 0
        for kereta in filtered_data:
            id_kereta = kereta.get("id_kereta", "-")
            nama_kereta = kereta.get("nama_kereta", "-")
            tanggal = kereta.get("tanggal", "-")
            stasiun_transit = kereta.get("stasiun_transit", [])
            waktu_transit = kereta.get("waktu_transit", [])
            jenis_layanan = kereta.get("jenis_layanan", "-")

            span_count = len(stasiun_transit)  # Hitung jumlah baris yang harus digabung

            for i in range(len(stasiun_transit)):
                self.ui.tableWidget_Hapus_Data.setItem(row, 3, QtWidgets.QTableWidgetItem(stasiun_transit[i]))
                self.ui.tableWidget_Hapus_Data.setItem(row, 4, QtWidgets.QTableWidgetItem(waktu_transit[i] if i < len(waktu_transit) else "-"))
                row += 1

            # Menggabungkan sel untuk ID Kereta, Nama, Tanggal, dan Jenis Layanan
            span_count = len(stasiun_transit)
            self.ui.tableWidget_Hapus_Data.setItem(row - span_count, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.tableWidget_Hapus_Data.setItem(row - span_count, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.tableWidget_Hapus_Data.setItem(row - span_count, 2, QtWidgets.QTableWidgetItem(tanggal))
            self.ui.tableWidget_Hapus_Data.setItem(row - span_count, 5, QtWidgets.QTableWidgetItem(jenis_layanan))

            self.ui.tableWidget_Hapus_Data.setSpan(row - span_count, 0, span_count, 1)  # ID Kereta
            self.ui.tableWidget_Hapus_Data.setSpan(row - span_count, 1, span_count, 1)  # Nama Kereta
            self.ui.tableWidget_Hapus_Data.setSpan(row - span_count, 2, span_count, 1)  # Tanggal
            self.ui.tableWidget_Hapus_Data.setSpan(row - span_count, 5, span_count, 1)  # jenis layanan

        # Atur tampilan tabel
        self.ui.tableWidget_Hapus_Data.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_Hapus_Data.resizeRowsToContents()
            
    def search_train_by_id(self, data):
        id_kereta = self.ui.input_id_Hapus_kereta.text().strip().lower()
        data = self.data
        filtered_data = [k for k in data if k.get("id_kereta", "").lower() == id_kereta.lower()]
        
        if not filtered_data:
            QtWidgets.QMessageBox.information(self, "Hasil Pencarian", "Tidak ada kereta yang ditemukan.")
        else:
            self.populate_table_hapus_data(filtered_data)
            
 
    def clear_form(self):
        self.ui.input_nama_kereta_TambahData.clear()
        self.ui.input_Jenis_layanan_TambahData.clear()
        self.ui.input_Tarif_Tiket_TambahData.clear()
