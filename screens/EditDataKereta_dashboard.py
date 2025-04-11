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
from datetime import datetime, timedelta
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from ui.dashboard_editDataKereta import Ui_dashboard_admin_Edit_Data as DashboardAdminEditData

INFOUMUM_DATABASE = "databases/informasi_umum.json"
JADWALKERETA_DATABASE = "databases/jadwal_kereta.json"
KURSIKERETA_DATABASE = "databases/kursi_kereta.json"
FORMATGERBONG = "databases/formatGerbong.json"
DELETEDDATA = "databases/deleted_records.json"

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
        self.jadwal_hari_ini()
        
    """ ======================== Navigasi Dashboard Edit Data Kereta ======================== """
    
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
        self.jadwal_hari_ini()
    def Tambah_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Tambah_jadwal_kereta)
    def Edit_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Edit_jadwal_kereta)
    def Hapus_Jadwal_kereta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Hapus_jadwal_kereta)
    def Go_to_Main(self):
        self.main_app.setCurrentWidget(self.main_app.dashboard_admin)
        
    """ ============================== Pengelolaan Data Aplikasi ============================== """
    
    def load_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal memuat file {filename}: {str(e)}")
            return []
        
    def load_data(self):
        """Memuat dan menggabungkan data dari semua database"""
        combined_data = {}
        
        # Muat semua data terlebih dahulu
        informasi_umum = self.load_json(INFOUMUM_DATABASE)
        jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)
        kursi_kereta = self.load_json(KURSIKERETA_DATABASE)
        
        # Gabungkan data berdasarkan id_kereta
        for data in [informasi_umum, jadwal_kereta, kursi_kereta]:
            for item in data:
                id_kereta = item.get("id_kereta")
                if id_kereta:
                    if id_kereta not in combined_data:
                        combined_data[id_kereta] = {}
                    combined_data[id_kereta].update(item)
        
        self.data = list(combined_data.values())
        return self.data
    
    def reset_table(self):
        """Mereset tabel ke keadaan awal"""
        self.ui.input_id_Hapus_kereta.clear()
        self.ui.tableWidget_Li.clearContents()  
        self.ui.tableWidget_Li.setRowCount(0) 
        self.ui.tableWidget_Hapus_Data.clearContents() 
        self.ui.tableWidget_Hapus_Data.setRowCount(0)
        self.jadwal_hari_ini() 
        
    def reset_form_tambah_data(self):
        """Mereset form tambah data"""
        self.ui.input_nama_kereta_TambahData.clear()    
        self.ui.input_Stasiun_Transit_TambahData.clear()
        self.ui.input_Waktu_Operasional_TambahData.clear()
        self.ui.input_Tarif_Tiket_TambahData.clear()
        self.ui.dateEdit_TambahData.setDate(QDate.currentDate()) 
        self.ui.input_Jumla_Gerbong_TambahData.clear()

    def reset_form_edit_data(self):
        """Mereset form edit data"""
        self.ui.input_id_kereta_EditData.clear()
        self.ui.input_staisun_transit_EditData.clear()
        self.ui.input_waktu_transit_EditData.clear()
        self.ui.input_tarif_tiket_EditData.clear()
        self.ui.input_jumlah_gerbong_EdiData.clear()
    
    def populate_table(self, data):
        """Mengisi tabel dengan data kereta"""
        self.ui.tableWidget_Li.setRowCount(0)  # Reset tabel
            
        # Set header tabel
        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Jenis Layanan", "Stasiun Transit", "Waktu Transit"]
        self.ui.tableWidget_Li.setColumnCount(len(headers))
        self.ui.tableWidget_Li.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_Li.verticalHeader().setVisible(False)
        
        # Isi data
        row = 0
        for kereta in data:
            id_kereta = kereta.get("id_kereta", "-")
            nama_kereta = kereta.get("nama_kereta", "-")
            tanggal = kereta.get("tanggal", "-")
            jenis_layanan = kereta.get("jenis_layanan", "-")
            stasiun_transit = kereta.get("stasiun_transit", [])
            waktu_transit = kereta.get("waktu_transit", [])
            
            span_count = len(stasiun_transit) or 1
            
            # Tambahkan baris sesuai jumlah stasiun transit
            self.ui.tableWidget_Li.setRowCount(self.ui.tableWidget_Li.rowCount() + span_count)
            
            # Isi data stasiun dan waktu transit
            for i in range(span_count):
                self.ui.tableWidget_Li.setItem(row + i, 4, QtWidgets.QTableWidgetItem(
                    stasiun_transit[i] if i < len(stasiun_transit) else "-"))
                self.ui.tableWidget_Li.setItem(row + i, 5, QtWidgets.QTableWidgetItem(
                    waktu_transit[i] if i < len(waktu_transit) else "-"))
            
            # Isi data umum dan gabungkan sel
            self.ui.tableWidget_Li.setItem(row, 0, QtWidgets.QTableWidgetItem(id_kereta))
            self.ui.tableWidget_Li.setItem(row, 1, QtWidgets.QTableWidgetItem(nama_kereta))
            self.ui.tableWidget_Li.setItem(row, 2, QtWidgets.QTableWidgetItem(tanggal))
            self.ui.tableWidget_Li.setItem(row, 3, QtWidgets.QTableWidgetItem(jenis_layanan))
            
            # Gabungkan sel untuk data umum
            if span_count > 1:
                for col in range(4):
                    self.ui.tableWidget_Li.setSpan(row, col, span_count, 1)
            
            row += span_count
            
        # Atur tampilan tabel
        self.ui.tableWidget_Li.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_Li.resizeRowsToContents()
    
    def jadwal_hari_ini(self):
        """Menampilkan jadwal kereta untuk hari ini dengan pengecekan lebih menyeluruh"""
        today = datetime.today().strftime("%Y-%m-%d")
        
        try:
            # Muat semua data terpisah untuk pengecekan
            kursi_data = self.load_json(KURSIKERETA_DATABASE)
            informasi_umum = self.load_json(INFOUMUM_DATABASE)
            jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)
            
            hasil_pencarian = []
            
            # Cari semua kereta yang beroperasi hari ini
            for kursi in kursi_data:
                if kursi["tanggal"] == today:
                    id_kereta = kursi["id_kereta"]
                    
                    # Cari informasi tambahan
                    info = next((i for i in informasi_umum if i["id_kereta"] == id_kereta), None)
                    jadwal = next((j for j in jadwal_kereta if j["id_kereta"] == id_kereta), None)
                    
                    if info and jadwal:
                        hasil_pencarian.append({
                            "id_kereta": id_kereta,
                            "nama_kereta": info["nama_kereta"],
                            "jenis_layanan": info["jenis_layanan"],
                            "tanggal": today,
                            "harga_tiket": info["harga_tiket"],
                            "stasiun_transit": jadwal["stasiun_transit"],
                            "waktu_transit": jadwal["waktu_transit"],
                            "gerbong": kursi["gerbong"]
                        })
                    else:
                        print(f"Data tidak lengkap untuk {id_kereta}")

            self.populate_table(hasil_pencarian)
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal memuat jadwal: {str(e)}")
        
    """ ============================== Pengelolaan Edit, Tambah, Hapus Data Aplikasi ============================== """

    def validasi_input(self, **kwargs):
        """Validasi input tidak boleh kosong"""
        for key, value in kwargs.items():
            if not value:
                QtWidgets.QMessageBox.warning(self, "Peringatan", f"Kolom {key.replace('_', ' ').title()} harus diisi!")
                return False
        return True

    def validasi_angka(self, harga, jumlah_gerbong):
        """Validasi input angka"""
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
        """Validasi jumlah stasiun dan waktu transit sama"""
        stasiun_list = [s.strip() for s in stasiun.split(",") if s.strip()]
        waktu_list = [w.strip() for w in waktu.split(",") if w.strip()]
        if len(stasiun_list) != len(waktu_list):
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Jumlah stasiun transit dan waktu transit harus sama!")
            return None, None
        return stasiun_list, waktu_list

    def load_format_gerbong(self, jenis_layanan):
        """Memuat format gerbong berdasarkan jenis layanan"""
        format_data = self.load_json(FORMATGERBONG)
        # Normalisasi case untuk pencarian (case insensitive)
        jenis_layanan = jenis_layanan.lower()
        return next((fg for fg in format_data if fg["jenis_layanan"].lower() == jenis_layanan), None)

    def generate_gerbong(self, id_kereta, jumlah_gerbong, format_terpilih):
        """Membuat data gerbong baru"""
        if not format_terpilih:
            return []
            
        return [
            {
                "gerbong_id": f"{id_kereta}-G{i}",
                "kapasitas": format_terpilih["kapasitas"],
                "kursi": format_terpilih["kursi"].copy()
            }
            for i in range(1, jumlah_gerbong + 1)
        ]
         
    def tambah_data_kereta(self):
        """Menambahkan data kereta baru dengan validasi tanggal dan membuat kursi untuk 30 hari ke depan"""
        # Validasi input dasar
        nama = self.ui.input_nama_kereta_TambahData.text().strip()
        layanan = self.ui.comboBox_Search_Data.currentText().strip()
        stasiun = self.ui.input_Stasiun_Transit_TambahData.text().strip()
        waktu = self.ui.input_Waktu_Operasional_TambahData.text().strip()
        harga = self.ui.input_Tarif_Tiket_TambahData.text().strip()
        jumlah_gerbong = self.ui.input_Jumla_Gerbong_TambahData.text().strip()
        
        # Validasi input tidak kosong
        if not self.validasi_input(nama=nama, layanan=layanan, harga=harga, 
                                jumlah_gerbong=jumlah_gerbong, stasiun=stasiun, waktu=waktu):
            return
        
        # Validasi angka
        harga, jumlah_gerbong = self.validasi_angka(harga, jumlah_gerbong)
        if harga is None:
            return
        
        # Validasi stasiun dan waktu transit
        stasiun_list, waktu_list = self.validasi_stasiun_waktu(stasiun, waktu)
        if stasiun_list is None:
            return
        
        # Validasi format gerbong
        format_gerbong = self.load_format_gerbong(layanan)
        if not format_gerbong:
            QtWidgets.QMessageBox.critical(self, "Error", f"Format gerbong untuk layanan '{layanan}' tidak ditemukan!")
            return
        
        # Validasi tanggal
        input_date = self.ui.dateEdit_TambahData.date()
        today = QDate.currentDate()
        
        if input_date < today:
            QtWidgets.QMessageBox.warning(
                self,
                "Tanggal Tidak Valid",
                "Tanggal operasional tidak boleh lebih awal dari hari ini!\n"
                f"Tanggal hari ini: {today.toString('dd/MM/yyyy')}"
            )
            return
        
        # Generate ID baru
        existing_ids = [int(d["id_kereta"][2:]) for d in self.data if d["id_kereta"].startswith("KA")]
        new_id = f"KA{max(existing_ids, default=0) + 1:03d}"
        
        # Konversi QDate ke string tanggal
        start_date = datetime(input_date.year(), input_date.month(), input_date.day())
        tanggal_str = start_date.strftime('%Y-%m-%d')
        
        try:
            # Tambahkan ke informasi umum
            with open(INFOUMUM_DATABASE, 'r+', encoding='utf-8') as f:
                info_data = json.load(f)
                info_data.append({
                    "id_kereta": new_id,
                    "nama_kereta": nama,
                    "jenis_layanan": layanan.lower(),
                    "harga_tiket": harga,
                    "jumlah_gerbong": int(jumlah_gerbong)
                })
                f.seek(0)
                json.dump(info_data, f, indent=4, ensure_ascii=False)
            
            # Tambahkan ke jadwal kereta
            with open(JADWALKERETA_DATABASE, 'r+', encoding='utf-8') as f:
                jadwal_data = json.load(f)
                jadwal_data.append({
                    "id_kereta": new_id,
                    "stasiun_transit": stasiun_list,
                    "waktu_transit": waktu_list
                })
                f.seek(0)
                json.dump(jadwal_data, f, indent=4, ensure_ascii=False)
            
            # Buat kursi untuk 30 hari ke depan
            with open(KURSIKERETA_DATABASE, 'r+', encoding='utf-8') as f:
                kursi_data = json.load(f)
                
                for i in range(30):
                    current_date = start_date + timedelta(days=i)
                    date_str = current_date.strftime('%Y-%m-%d')
                    
                    # Cek duplikasi
                    if not any(k['id_kereta'] == new_id and k['tanggal'] == date_str for k in kursi_data):
                        kursi_data.append({
                            "id_kereta": new_id,
                            "tanggal": date_str,
                            "gerbong": self.generate_gerbong(new_id, int(jumlah_gerbong), format_gerbong)
                        })
                
                f.seek(0)
                json.dump(kursi_data, f, indent=4, ensure_ascii=False)
            
            QtWidgets.QMessageBox.information(
                self,
                "Sukses",
                f"Data kereta {new_id} berhasil ditambahkan!\n"
                f"Kursi telah dibuat untuk 30 hari ke depan mulai dari {tanggal_str}"
            )
            
            self.reset_form_tambah_data()
            self.load_data()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Gagal menyimpan data: {str(e)}"
            )
            
    def edit_data_kereta(self):
            """Mengedit data kereta berdasarkan ID tanpa menggunakan tanggal input"""
            # Validasi ID Kereta
            id_kereta = self.ui.input_id_kereta_EditData.text().strip().upper()
            if not id_kereta:
                QtWidgets.QMessageBox.warning(self, "Peringatan", "ID Kereta harus diisi!")
                return

            # Ambil input dari UI
            stasiun = self.ui.input_staisun_transit_EditData.text().strip()
            layanan = self.ui.comboBox_EditData.currentText().strip()
            waktu = self.ui.input_waktu_transit_EditData.text().strip()
            harga = self.ui.input_tarif_tiket_EditData.text().strip()
            jumlah_gerbong = self.ui.input_jumlah_gerbong_EdiData.text().strip()

            # Validasi input
            stasiun_list = [s.strip() for s in stasiun.split(',') if s.strip()]
            waktu_list = [w.strip() for w in waktu.split(',') if w.strip()]
            
            if not stasiun_list or not waktu_list:
                QtWidgets.QMessageBox.warning(self, "Peringatan", "Stasiun dan waktu transit tidak boleh kosong!")
                return
                
            if len(stasiun_list) != len(waktu_list):
                QtWidgets.QMessageBox.warning(self, "Peringatan", 
                    "Jumlah stasiun transit dan waktu harus sama!")
                return

            try:
                harga = float(harga)
                jumlah_gerbong = int(jumlah_gerbong)
                if harga <= 0 or jumlah_gerbong <= 0:
                    raise ValueError
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Peringatan", 
                    "Harga dan jumlah gerbong harus berupa angka positif!")
                return

            # Baca semua data yang diperlukan
            with open(INFOUMUM_DATABASE, 'r', encoding='utf-8') as f:
                info_data = json.load(f)
            
            with open(JADWALKERETA_DATABASE, 'r', encoding='utf-8') as f:
                jadwal_data = json.load(f)
            
            with open(KURSIKERETA_DATABASE, 'r', encoding='utf-8') as f:
                kursi_data = json.load(f)

            # Cari data kereta yang akan diedit
            kereta_info = next((k for k in info_data if k.get("id_kereta") == id_kereta), None)
            if not kereta_info:
                QtWidgets.QMessageBox.warning(self, "Peringatan", "Data kereta tidak ditemukan!")
                return

            # Cek perubahan jenis layanan
            jenis_layanan_lama = kereta_info.get("jenis_layanan", "")
            jenis_layanan_baru = layanan.lower()
            format_berubah = jenis_layanan_lama != jenis_layanan_baru

            # Update data informasi umum
            for item in info_data:
                if item.get("id_kereta") == id_kereta:
                    item.update({
                        "jenis_layanan": jenis_layanan_baru,
                        "harga_tiket": harga,
                        "jumlah_gerbong": jumlah_gerbong
                    })
                    break

            # Update data jadwal
            for item in jadwal_data:
                if item.get("id_kereta") == id_kereta:
                    item.update({
                        "stasiun_transit": stasiun_list,
                        "waktu_transit": waktu_list
                    })
                    break

            # Update data kursi jika jenis layanan atau jumlah gerbong berubah
            if format_berubah or (jumlah_gerbong != kereta_info.get("jumlah_gerbong", 0)):
                format_gerbong = self.load_format_gerbong(jenis_layanan_baru)
                if not format_gerbong:
                    QtWidgets.QMessageBox.critical(self, "Error", "Format gerbong tidak ditemukan!")
                    return
                
                # Update semua kursi untuk kereta ini
                for k in kursi_data:
                    if k.get("id_kereta") == id_kereta:
                        k["gerbong"] = self.generate_gerbong(id_kereta, jumlah_gerbong, format_gerbong)

            # Simpan semua perubahan
            with open(INFOUMUM_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(info_data, f, indent=4, ensure_ascii=False)
            
            with open(JADWALKERETA_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(jadwal_data, f, indent=4, ensure_ascii=False)
            
            with open(KURSIKERETA_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(kursi_data, f, indent=4, ensure_ascii=False)

            QtWidgets.QMessageBox.information(
                self, 
                "Sukses", 
                f"Data kereta {id_kereta} berhasil diperbarui!\n"
                f"Jenis layanan: {jenis_layanan_baru}\n"
                f"Jumlah gerbong: {jumlah_gerbong}"
            )
            self.reset_form_edit_data()
            self.load_data()

    def hapus_data_kereta(self):
        """Menghapus data kursi dengan penanganan error yang lebih robust"""
        try:
            id_kereta = self.ui.input_id_Hapus_kereta.text().strip().upper()
            tanggal = self.ui.dateEdit_hapus_data_kereta.date().toString('yyyy-MM-dd')

            if not id_kereta:
                QtWidgets.QMessageBox.warning(self, "Peringatan", "ID Kereta harus diisi!")
                return

            # Baca data kursi
            with open(KURSIKERETA_DATABASE, 'r', encoding='utf-8') as f:
                try:
                    kursi_data = json.load(f)
                    if not isinstance(kursi_data, list):  # Pastikan ini list
                        kursi_data = []
                except (json.JSONDecodeError, FileNotFoundError):
                    kursi_data = []

            # Filter data yang akan dipertahankan
            kursi_baru = []
            for item in kursi_data:
                try:
                    # Pastikan item adalah dictionary dan memiliki key yang diperlukan
                    if (isinstance(item, dict) and 
                        item.get("id_kereta") != id_kereta or 
                        item.get("tanggal") != tanggal):
                        kursi_baru.append(item)
                except Exception as e:
                    print(f"Error processing item: {str(e)}")
                    continue

            # Simpan ke log penghapusan
            DELETED_RECORDS_LOG = "databases/deleted_records.json"
            deleted_records = {"deleted": []}
            
            try:
                with open(DELETED_RECORDS_LOG, 'r', encoding='utf-8') as f:
                    deleted_records = json.load(f)
                    if not isinstance(deleted_records, dict):
                        deleted_records = {"deleted": []}
            except (FileNotFoundError, json.JSONDecodeError):
                pass

            deleted_records["deleted"].append({
                "id_kereta": id_kereta,
                "tanggal": tanggal,
                "waktu_dihapus": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            with open(DELETED_RECORDS_LOG, 'w', encoding='utf-8') as f:
                json.dump(deleted_records, f, indent=4, ensure_ascii=False)

            # Simpan data kursi yang sudah difilter
            with open(KURSIKERETA_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(kursi_baru, f, indent=4, ensure_ascii=False)

            # Update UI
            self.ui.tableWidget_Hapus_Data.clearContents()
            self.ui.tableWidget_Hapus_Data.setRowCount(0)
            
            QtWidgets.QMessageBox.information(
                self, 
                "Sukses", 
                f"Data kursi {id_kereta} pada {tanggal} berhasil dihapus!"
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Terjadi kesalahan saat menghapus data:\n{str(e)}"
            )
            print(f"Error detail: {str(e)}")
        
    def search_train_by_jenis_layanan(self):
        """Mencari kereta berdasarkan jenis layanan dan tanggal dengan pengecekan data yang lebih akurat"""
    
        # Ambil input dari UI
        jenis = self.ui.comboBox_Search_Data.currentText().strip().lower()
        tanggal = self.ui.dateEdit_lihat_data_kereta.date().toString('yyyy-MM-dd')
            
        # Validasi input
        if not jenis or not tanggal:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Input Tidak Lengkap",
                    "Harap isi kedua field:\n- Jenis Layanan\n- Tanggal Pencarian"
                )
                return

        # Muat data langsung dari sumber terpisah untuk akurasi
        kursi_data = self.load_json(KURSIKERETA_DATABASE)
        informasi_umum = self.load_json(INFOUMUM_DATABASE)
        jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)
            
        # Dictionary untuk mapping cepat
        info_kereta = {item['id_kereta']: item for item in informasi_umum}
        jadwal_kereta_dict = {item['id_kereta']: item for item in jadwal_kereta}

        hasil = []
        for kursi in kursi_data:
                # Cari yang sesuai tanggal
                if kursi['tanggal'] == tanggal:
                    id_kereta = kursi['id_kereta']
                    
                    # Dapatkan info tambahan
                    info = info_kereta.get(id_kereta)
                    jadwal = jadwal_kereta_dict.get(id_kereta)
                    
                    # Cek jenis layanan dan kelengkapan data
                    if info and jadwal and info.get('jenis_layanan', '').lower() == jenis:
                        hasil.append({
                            'id_kereta': id_kereta,
                            'nama_kereta': info['nama_kereta'],
                            'jenis_layanan': info['jenis_layanan'],
                            'harga_tiket': info['harga_tiket'],
                            'tanggal': kursi['tanggal'],
                            'stasiun_transit': jadwal['stasiun_transit'],
                            'waktu_transit': jadwal['waktu_transit'],
                            'gerbong': kursi['gerbong']
                        })

        if not hasil:
                # Pesan error lebih informatif
                QtWidgets.QMessageBox.information(
                    self,
                    "Hasil Pencarian",
                    f"Tidak ditemukan kereta {jenis.title()} pada tanggal {tanggal}.\n\n"
                )
        else:
            self.populate_table(hasil)

    def populate_table_hapus_data(self, filtered_data):
        """Mengisi tabel untuk halaman hapus data"""
        self.ui.tableWidget_Hapus_Data.setRowCount(0)
            
        headers = ["ID Kereta", "Nama Kereta", "Tanggal", "Stasiun Transit", "Waktu Transit", "Jenis Layanan"]
        self.ui.tableWidget_Hapus_Data.setColumnCount(len(headers))
        self.ui.tableWidget_Hapus_Data.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_Hapus_Data.verticalHeader().setVisible(False)
        
        row = 0
        for kereta in filtered_data:
            stasiun_transit = kereta.get("stasiun_transit", [])
            span_count = len(stasiun_transit) or 1
            
            self.ui.tableWidget_Hapus_Data.setRowCount(self.ui.tableWidget_Hapus_Data.rowCount() + span_count)
            
            # Isi data stasiun dan waktu transit
            for i in range(span_count):
                self.ui.tableWidget_Hapus_Data.setItem(row + i, 3, QtWidgets.QTableWidgetItem(
                    stasiun_transit[i] if i < len(stasiun_transit) else "-"))
                self.ui.tableWidget_Hapus_Data.setItem(row + i, 4, QtWidgets.QTableWidgetItem(
                    kereta.get("waktu_transit", [])[i] if i < len(kereta.get("waktu_transit", [])) else "-"))
            
            # Isi data umum
            self.ui.tableWidget_Hapus_Data.setItem(row, 0, QtWidgets.QTableWidgetItem(kereta.get("id_kereta", "-")))
            self.ui.tableWidget_Hapus_Data.setItem(row, 1, QtWidgets.QTableWidgetItem(kereta.get("nama_kereta", "-")))
            self.ui.tableWidget_Hapus_Data.setItem(row, 2, QtWidgets.QTableWidgetItem(kereta.get("tanggal", "-")))
            self.ui.tableWidget_Hapus_Data.setItem(row, 5, QtWidgets.QTableWidgetItem(kereta.get("jenis_layanan", "-")))
            
            # Gabungkan sel untuk data umum
            if span_count > 1:
                for col in [0, 1, 2, 5]:
                    self.ui.tableWidget_Hapus_Data.setSpan(row, col, span_count, 1)
            
            row += span_count
            
        self.ui.tableWidget_Hapus_Data.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_Hapus_Data.resizeRowsToContents()
            
    def search_train_by_id(self):
        """Mencari kereta berdasarkan ID dan tanggal dengan pengecekan lebih robust"""
        try:
            # Ambil input dari UI
            id_kereta = self.ui.input_id_Hapus_kereta.text().strip().upper()
            tanggal = self.ui.dateEdit_hapus_data_kereta.date().toString('yyyy-MM-dd')
            
            # Validasi input
            if not id_kereta:
                QtWidgets.QMessageBox.warning(self, "Peringatan", "ID Kereta harus diisi!")
                return
                
            # Muat data terbaru dari semua sumber
            kursi_data = self.load_json(KURSIKERETA_DATABASE)
            informasi_umum = self.load_json(INFOUMUM_DATABASE)
            jadwal_kereta = self.load_json(JADWALKERETA_DATABASE)
            
            # Cari data yang sesuai
            hasil = []
            for kursi in kursi_data:
                if kursi["id_kereta"] == id_kereta and kursi["tanggal"] == tanggal:
                    # Cari informasi tambahan
                    info = next((i for i in informasi_umum if i["id_kereta"] == id_kereta), None)
                    jadwal = next((j for j in jadwal_kereta if j["id_kereta"] == id_kereta), None)
                    
                    if info and jadwal:
                        hasil.append({
                            "id_kereta": id_kereta,
                            "nama_kereta": info["nama_kereta"],
                            "jenis_layanan": info["jenis_layanan"],
                            "tanggal": tanggal,
                            "harga_tiket": info["harga_tiket"],
                            "stasiun_transit": jadwal["stasiun_transit"],
                            "waktu_transit": jadwal["waktu_transit"],
                            "gerbong": kursi["gerbong"]
                        })
            
            # Tampilkan hasil
            if not hasil:
                QtWidgets.QMessageBox.information(
                    self, 
                    "Hasil Pencarian",
                    f"Tidak ditemukan kereta dengan ID {id_kereta} pada tanggal {tanggal}.\n"
                )
            else:
                self.populate_table_hapus_data(hasil)
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Error",
                f"Terjadi kesalahan saat mencari kereta:\n{str(e)}"
            )

    """ ============================== Fitur Tambahan Update Kursi Otomatis ============================== """
            
    def update_kursi_kereta(self):
        """Memperbarui data kursi untuk 30 hari ke depan dengan penanganan error"""
        try:
            # Baca semua data yang diperlukan
            with open(KURSIKERETA_DATABASE, 'r', encoding='utf-8') as f:
                kursi_kereta = json.load(f)
            with open(INFOUMUM_DATABASE, 'r', encoding='utf-8') as f:
                informasi_umum = json.load(f)
            
            # Inisialisasi log penghapusan jika tidak ada
            deleted_records = {"deleted": []}
            try:
                with open(DELETEDDATA, 'r', encoding='utf-8') as f:
                    deleted_records = json.load(f)
                    if not isinstance(deleted_records, dict) or "deleted" not in deleted_records:
                        deleted_records = {"deleted": []}
            except (FileNotFoundError, json.JSONDecodeError):
                pass

            # Hitung rentang tanggal
            today = datetime.today().date()
            
            # Filter data kursi yang valid
            kursi_kereta_baru = []
            for kursi in kursi_kereta:
                try:
                    if isinstance(kursi, dict) and 'tanggal' in kursi:
                        kursi_date = datetime.strptime(kursi['tanggal'], '%Y-%m-%d').date()
                        if kursi_date >= today:
                            kursi_kereta_baru.append(kursi)
                except (ValueError, KeyError):
                    continue

            # Proses pembaruan untuk setiap kereta aktif
            for kereta in informasi_umum:
                try:
                    if not isinstance(kereta, dict):
                        continue
                        
                    id_kereta = kereta.get('id_kereta')
                    if not id_kereta:
                        continue
                    
                    format_gerbong = self.load_format_gerbong(kereta.get('jenis_layanan', ''))
                    if not format_gerbong:
                        continue
                    
                    # Generate data untuk 30 hari ke depan
                    for i in range(31):
                        tanggal = (today + timedelta(days=i)).strftime('%Y-%m-%d')
                        
                        # Skip jika di log penghapusan
                        if any(d.get('id_kereta') == id_kereta and d.get('tanggal') == tanggal 
                            for d in deleted_records.get('deleted', [])):
                            continue
                        
                        # Cek apakah data sudah ada
                        existing = next((k for k in kursi_kereta_baru 
                                        if isinstance(k, dict) and 
                                        k.get('id_kereta') == id_kereta and 
                                        k.get('tanggal') == tanggal), None)
                        
                        # Skip jika bukan hari ini dan sudah ada
                        if existing and i != 0:
                            continue
                        
                        # Generate data baru
                        gerbong = self.generate_gerbong(
                            id_kereta,
                            int(kereta.get('jumlah_gerbong', 0)),
                            format_gerbong
                        ) if isinstance(kereta.get('jumlah_gerbong'), (int, str)) else []
                        
                        new_data = {
                            'id_kereta': id_kereta,
                            'tanggal': tanggal,
                            'gerbong': gerbong
                        }
                        
                        if existing:
                            kursi_kereta_baru[kursi_kereta_baru.index(existing)] = new_data
                        else:
                            kursi_kereta_baru.append(new_data)
                            
                except Exception as e:
                    print(f"Error processing train {id_kereta}: {str(e)}")
                    continue

            # Simpan perubahan
            with open(KURSIKERETA_DATABASE, 'w', encoding='utf-8') as f:
                json.dump(kursi_kereta_baru, f, indent=4, ensure_ascii=False)
                
            print(f"Pembaruan selesai. Total data: {len(kursi_kereta_baru)}")
            return True
            
        except Exception as e:
            print(f"Gagal memperbarui kursi kereta: {str(e)}")
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Terjadi kesalahan saat memperbarui data:\n{str(e)}"
            )
            return False