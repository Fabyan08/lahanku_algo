import csv
import hashlib
from datetime import datetime, timedelta
from fpdf import FPDF
import re  # Untuk validasi email

# Fungsi untuk mendapatkan ID berikutnya
def get_next_id(filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                return int(rows[-1][0]) + 1
    except FileNotFoundError:
        pass
    return 1

# Menu utama
def main_menu():
    print("=== Selamat Datang di Lahanku ===")
    print("[1] Login")
    print("[2] Register")
    pilihan = input("Pilih menu: ")
    
    if pilihan == '1':
        login()
    elif pilihan == '2':
        register()
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        main_menu()

# Fungsi registrasi
def register():
    print("=== Registrasi ===")
    user_id = get_next_id("users.csv")  # Ambil ID berikutnya
    nama = input("Masukkan Nama: ")
    email = input("Masukkan Email: ")
    password = input("Masukkan Password: ")
    ktp = input("Masukkan No KTP: ")
    nomor_hp = input("Masukkan Nomor HP: ")
    alamat = input("Masukkan Alamat: ")
    
    print("Pilih jenis akun:")
    print("[1] Pengguna")
    print("[2] Pemilik Lahan")
    pilihan_level = input("Pilih (1/2): ")
    
    if pilihan_level == '1':
        level = "pengguna"
    elif pilihan_level == '2':
        level = "pemilik_lahan"
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        register()
        return
    
    # Enkripsi password
    password = hashlib.sha256(password.encode()).hexdigest()
    
    # Simpan data ke file CSV
    with open("users.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, nama, email, password , ktp, nomor_hp, alamat, level])
    
    print("Registrasi berhasil! Silakan login.")
    main_menu()

# Fungsi login
def is_valid_email(email):
    # Regex sederhana untuk validasi email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def login():
    print("=== Login ===")
    email = input("Masukkan Email: ").strip()
    password = input("Masukkan Password: ").strip()

    # Validasi format email
    if not is_valid_email(email):
        print("Format email tidak valid. Silakan coba lagi.")
        login()
        return

    # Enkripsi password untuk verifikasi
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open("users.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Lewati header, jika ada
            for row in reader:
                if len(row) < 8:  # Pastikan row memiliki cukup kolom
                    continue
                # Memeriksa kecocokan email dan password
                if row[2] == email and row[3] == password_hash:
                    print(f"Login berhasil! Selamat datang, {row[1]}")
                    show_menu(row[7], row[0])  # Tampilkan menu sesuai level, level berada pada kolom ke-7
                    return

    except FileNotFoundError:
        print("Database pengguna belum tersedia. Silakan registrasi terlebih dahulu.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print("Email atau password salah. Coba lagi.")
    main_menu()

# Menu sesuai level
def show_menu(level, user_id):
    print("\n=== Menu Utama ===")
    print("[0] Profil")
    if level == "pengguna":
        print("[1] Sewa Lahan")
        print("[2] Data Perjanjian")
        print("[3] Lihat History")
        pilihan = input("Pilih menu: ")
        if pilihan == '0':
            show_profile(level, user_id)  # Tampilkan menu Profil
        elif pilihan == '1':
            sewa_lahan(user_id)
        elif pilihan == '2':
            data_perjanjian(user_id)
        elif pilihan == '3':
            lihat_history(user_id)
        else:
            print("Fitur sedang dalam pengembangan.")
            show_menu(level, user_id)

    elif level == "pemilik_lahan":
        print("[1] Data Lahan")
        print("[2] List Penyewa")
        pilihan = input("Pilih menu: ")
        if pilihan == '0':
            show_profile(level, user_id)  # Tampilkan menu Profil
        elif pilihan == '1':
            crud_lahan(user_id)
        elif pilihan == '2':
            list_penyewa(user_id)  # Panggil fungsi baru untuk fitur List Penyewa
        else:
            print("Fitur sedang dalam pengembangan.")
            show_menu(level, user_id)

    elif level == "admin":
        print("[1] Rekap Penyewaan")
        print("[2] Rekap Jumlah Pengguna")

        while True:
            pilihan = input("Pilih menu: ")
            if pilihan == '1':
                rekap_penyewaan(user_id)  # Pastikan user_id diteruskan
                break
            elif pilihan == '2':
                rekap_jumlah_pengguna(user_id)
                break
            elif pilihan == '0':
                show_profile(level, user_id)  # Tampilkan menu Profil
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    else:
        print("Level akses tidak dikenali.")
        return
    


# SEMUA HAK AKSES

def show_profile(level, user_id):  # Add the 'level' argument here
    try:
        # Membaca file pengguna
        with open('users.csv', 'r') as file:
            users = list(csv.reader(file))

        # Mencari pengguna berdasarkan user_id
        user = next((u for u in users if u[0] == user_id), None)

        if not user:
            print("Pengguna tidak ditemukan.")
            return

        # Menampilkan data profil pengguna
        print("\n=== Profil Pengguna ===")
        print(f"ID Pengguna: {user[0]}")
        print(f"Nama: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Nomor KTP: {user[4]}")
        print(f"Nomor HP: {user[5]}")
        print(f"Alamat: {user[6]}")
        print("=" * 30)

        

        # Memberikan opsi untuk mengubah profil
        print("Pilih data yang ingin diubah:")
        print("[1] Nama")
        print("[2] Email")
        print("[3] Nomor KTP")
        print("[4] Nomor HP")
        print("[5] Alamat")
        print("[0] Kembali ke Menu Utama")
        print(" ")
        print("=====Logout=====")
        print("[9] Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            new_name = input("Masukkan nama baru: ")
            user[1] = new_name
            print(f"Nama berhasil diubah menjadi {new_name}")
        elif pilihan == '2':
            new_email = input("Masukkan email baru: ")
            user[2] = new_email
            print(f"Email berhasil diubah menjadi {new_email}")
        elif pilihan == '3':
            new_ktp = input("Masukkan nomor KTP baru: ")
            user[4] = new_ktp
            print(f"Nomor KTP berhasil diubah menjadi {new_ktp}")
        elif pilihan == '4':
            new_phone = input("Masukkan nomor HP baru: ")
            user[5] = new_phone
            print(f"Nomor HP berhasil diubah menjadi {new_phone}")
        elif pilihan == '5':
            new_address = input("Masukkan alamat baru: ")
            user[6] = new_address
            print(f"Alamat berhasil diubah menjadi {new_address}")
        elif pilihan == '0':
            show_menu(level, user_id)  # Kembali ke menu utama
            return
        elif pilihan == '9':
            print("Terima kasih telah menggunakan layanan kami. Sampai jumpa kembali!")
            return
        else:
            print("Pilihan tidak valid. Kembali ke menu utama.")
            show_menu(level, user_id)  # Kembali ke menu utama

        # Menyimpan perubahan ke file CSV
        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)
            show_menu(level, user_id)  # Kembali ke menu utama
            return

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# PENGGUNA

def sewa_lahan(user_id):
    print("\n=== Sewa Lahan ===")
    tanaman_cari = input("Masukkan tanaman yang ingin Anda tanam: ").lower()
    lahan_ditemukan = []

    print(f"\nLahan yang cocok untuk '{tanaman_cari}':")
    print(f"{'No':<5} {'Lokasi':<30} {'Tanaman':<40} {'Luas':<10} {'Harga/hektar':<15}")
    print("=" * 100)

    try:
        with open("lahan.csv", mode="r") as file:
            reader = csv.reader(file)
            lahan_data = list(reader)
            nomor = 1
            for row in lahan_data:
                tanaman_list = [tanaman.strip().lower() for tanaman in row[3].split(",")]
                if tanaman_cari in tanaman_list:
                    lahan_ditemukan.append(row)
                    print(f"{nomor:<5} {row[2]:<30} {row[3]:<40} {row[5]:<10} {row[6]:<15}")
                    nomor += 1
    except FileNotFoundError:
        print("Belum ada data lahan.")

    if not lahan_ditemukan:
        print("Tidak ada lahan yang cocok untuk tanaman tersebut.")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)
        return

    nomor_pilih = int(input("\nPilih nomor lahan yang ingin Anda sewa (0 untuk batal): "))
    if nomor_pilih == 0:
        show_menu("pengguna", user_id)
        return

    if 1 <= nomor_pilih <= len(lahan_ditemukan):
        detail_lahan(user_id, lahan_ditemukan[nomor_pilih - 1])
    else:
        print("Nomor tidak valid.")
        sewa_lahan(user_id)

def detail_lahan(user_id, lahan):
    print("\n=== Detail Lahan ===")
    print(f"Lokasi: {lahan[2]}")
    print(f"Tanaman yang bisa ditanam: {lahan[3]}")
    print(f"Deskripsi: {lahan[4]}")
    print(f"Luas: {lahan[5]} hektar")
    print(f"Harga per hektar (per bulan): {lahan[6]}")

    tanggal_sewa = input("\nMasukkan tanggal sewa (YYYY-MM-DD): ")
    durasi_bulan = int(input("Masukkan durasi sewa (dalam bulan): "))
    luas_sewa = float(input("Masukkan luas lahan yang ingin Anda sewa (hektar): "))

    try:
        tanggal_sewa_date = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
        tanggal_berakhir = tanggal_sewa_date + timedelta(days=30 * durasi_bulan)  # Perkiraan 30 hari per bulan
        total_harga = luas_sewa * float(lahan[6]) * durasi_bulan

        print(f"\nTanggal Berakhir: {tanggal_berakhir.strftime('%Y-%m-%d')}")
        print(f"Konfirmasi Harga: Rp {total_harga:,.2f}")
        konfirmasi = input("Apakah Anda ingin melanjutkan? (y/n): ").lower()

        if konfirmasi == 'y':
            tambah_sewa(user_id, lahan, tanggal_sewa, tanggal_berakhir.strftime('%Y-%m-%d'), luas_sewa, total_harga)
            print("Sewa berhasil ditambahkan. Menunggu perjanjian.")
        else:
            print("Sewa dibatalkan.")
    except ValueError:
        print("Format tanggal tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)

def tambah_sewa(user_id, lahan, tanggal_sewa, tanggal_berakhir, luas_sewa, total_harga):
    try:
        # Membaca file sewa.csv untuk mendapatkan ID terakhir
        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            # Menemukan ID tertinggi yang sudah ada, jika ada
            last_id = 0
            for row in rows:
                if len(row) > 0 and row[0].isdigit():
                    last_id = max(last_id, int(row[0]))  # Ambil ID tertinggi

        new_id = last_id + 1  # ID baru adalah ID terakhir + 1

        # Menambahkan data baru dengan ID yang unik
        with open("sewa.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                new_id,                # ID Sewa yang baru
                user_id,               # ID Penyewa
                lahan[0],              # ID Lahan
                tanggal_sewa,          # Tanggal Sewa
                tanggal_berakhir,      # Tanggal Berakhir
                luas_sewa,             # Luas yang Disewa
                total_harga,           # Total Harga
                "Belum Perjanjian"     # Status
            ])
        print(f"Data penyewaan dengan ID {new_id} berhasil ditambahkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def get_username(user_id):
    """
    Fungsi untuk mendapatkan nama pengguna dari users.csv berdasarkan user_id.
    """
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(user_id):  # Membandingkan ID pengguna sebagai string
                return row[1]  # Mengembalikan nama pengguna
    return "Unknown"  # Jika tidak ditemukan

def buat_surat_perjanjian(data, user_id):
    """
    Fungsi untuk membuat surat perjanjian.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Judul surat perjanjian
    pdf.cell(200, 10, txt="Surat Perjanjian Sewa Lahan", ln=True, align='C')
    pdf.ln(10)

    # Menambahkan detail perjanjian
    pdf.cell(200, 10, txt=f"Tanggal Sewa: {data[2]}", ln=True)
    pdf.cell(200, 10, txt=f"Tanggal Berakhir: {data[3]}", ln=True)
    pdf.cell(200, 10, txt=f"Luas Lahan: {data[4]} hektar", ln=True)
    
    # Mengubah harga sewa menjadi float dan menambahkannya ke dalam surat
    try:
        total_harga = float(data[5])  # Mengubah harga menjadi float
        pdf.cell(200, 10, txt=f"Total Harga: Rp {total_harga:,.2f}", ln=True)  # Format dengan 2 desimal
    except ValueError:
        pdf.cell(200, 10, txt="Total Harga: Rp 0,00", ln=True)  # Menangani jika data[5] bukan angka

    pdf.cell(200, 10, txt="Status: Belum Perjanjian", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Dengan ini kedua belah pihak sepakat untuk melaksanakan perjanjian ini.", ln=True)
    pdf.cell(200, 10, txt="Pihak 1: Pemilik Lahan", ln=True)
    pdf.cell(200, 10, txt="Pihak 2: Penyewa", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Tanda Tangan:", ln=True)
    pdf.cell(200, 10, txt="Pihak 1: ___________________", ln=True)
    pdf.cell(200, 10, txt="Pihak 2: ___________________", ln=True)

    # Mendapatkan nama pengguna dari user_id
    nama_penyewa = get_username(user_id).replace(" ", "_")  # Nama pengguna (ganti spasi dengan underscore)

    # Menyimpan file PDF dengan nama yang unik
    id_sewa = data[0]  # ID sewa
    file_name = f"{id_sewa}_{nama_penyewa}.pdf"  # Format nama file
    pdf.output(file_name)
    print(f"Surat perjanjian disimpan sebagai {file_name}.")

def data_perjanjian(user_id):
    print("\n=== Data Perjanjian ===")
    print(f"{'No':<5} {'Lokasi':<30} {'Tanggal Sewa':<15} {'Tanggal Berakhir':<15} {'Status':<20} {'ID Penyewa':<12} {'ID Lahan':<10}")
    print("="*100)

    data_sewa = []
    lokasi_dict = {}

    # Membaca file lahan.csv dan membuat kamus ID lokasi ke nama lokasi
    try:
        with open("lahan.csv", mode="r") as lahan_file:
            lahan_reader = csv.reader(lahan_file)
            for row in lahan_reader:
                lokasi_dict[row[0]] = row[2]  # row[0] = ID, row[2] = Nama Lokasi
    except FileNotFoundError:
        print("File 'lahan.csv' tidak ditemukan.")
        return

    # Membaca data dari file sewa.csv
    try:
        with open("sewa.csv", mode="r") as sewa_file:
            reader = csv.reader(sewa_file)
            for row in reader:
                # Filter hanya perjanjian yang sesuai dengan user_id
                if row[1] == str(user_id):  # row[1] adalah ID Penyewa
                    data_sewa.append(row)
                    
    except FileNotFoundError:
        print("Belum ada data persewaan.")
        return

    if not data_sewa:
        print("Tidak ada perjanjian yang perlu dibuat.")
        input("\nTekan Enter untuk kembali.")
        return

    # Menampilkan data perjanjian yang difilter dengan nomor urut dimulai dari 1
    for i, row in enumerate(data_sewa, start=1):
        lokasi_id = row[2]  # ID lokasi ada di kolom ketiga (index 2) dari sewa.csv
        lokasi_name = lokasi_dict.get(lokasi_id, "Tidak Dikenal")  # Mendapatkan nama lokasi dari dictionary
        tanggal_sewa = row[3]  # Tanggal Sewa ada di kolom ke-4
        tanggal_berakhir = row[4]  # Tanggal Berakhir ada di kolom ke-5
        status = row[7]  # Status ada di kolom ke-8
        id_penyewa = row[4]  # ID penyewa ada di kolom ke-5
        id_lahan = row[2]  # ID lahan ada di kolom ke-3

        # Menampilkan data perjanjian
        print(f"{i:<5} {lokasi_name:<30} {tanggal_sewa:<15} {tanggal_berakhir:<15} {status:<20} {id_penyewa:<12} {id_lahan:<10}")

    pilihan = input("\nMasukkan nomor perjanjian untuk dibuat (atau 0 untuk batal): ")
    if pilihan.isdigit() and 1 <= int(pilihan) <= len(data_sewa):
        nomor = int(pilihan) - 1
        buat_surat_perjanjian(data_sewa[nomor], user_id)
        print("Surat perjanjian berhasil dibuat dan disimpan sebagai PDF.")
    else:
        print("Pilihan tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)
    
def lihat_history(user_id):
    try:
        # Membaca data sewa untuk mencocokkan user_id
        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            data_sewa = [row for row in reader if len(row) > 7 and row[1] == str(user_id)]  # Kolom ke-2 adalah user_id

        if not data_sewa:
            print("\nTidak ada data history penyewaan untuk user ini.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        # Menampilkan data dalam tabel
        print("\n=== History Penyewaan ===")
        print(f"{'No.':<5}{'ID Sewa':<10}{'Status':<15}{'Tgl Sewa':<15}{'Tgl Selesai':<15}{'Harga':<10}")
        for i, row in enumerate(data_sewa, start=1):
            print(f"{i:<5}{row[0]:<10}{row[7]:<15}{row[3]:<15}{row[4]:<15}Rp {float(row[6]):,.2f}")

        # Memilih data untuk melihat detail
        pilihan = input("\nMasukkan nomor untuk melihat detail (atau 0 untuk kembali): ")
        if pilihan == '0':
            show_menu("pengguna", user_id)
            return
        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(data_sewa)):
            print("Nomor tidak valid.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        # Menampilkan detail data
        detail = data_sewa[int(pilihan) - 1]
        print("\n=== Detail Penyewaan ===")
        print(f"ID Sewa: {detail[0]}")
        print(f"Status: {detail[7]}")
        print(f"Tanggal Sewa: {detail[3]}")
        print(f"Tanggal Selesai: {detail[4]}")
        print(f"Luas yang Disewa: {detail[5]} hektar")
        print(f"Total Harga: Rp {float(detail[6]):,.2f}")

        # Mengecek jika status masih "Belum Perjanjian"
        if detail[6] == "Belum Perjanjian":
            print("\nStatus masih 'Belum Perjanjian'. Tidak bisa mengubah status menjadi 'Berjalan' atau 'Selesai'.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        # Mengubah status
        print("\nUbah status:")
        print("[1] Berjalan")
        print("[2] Selesai")
        status_input = input("Pilih status baru: ")
        if status_input == '1':
            status_baru = "Berjalan"
        elif status_input == '2':
            status_baru = "Selesai"
        else:
            print("Pilihan tidak valid.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        # Update status di file sewa.csv
        with open("sewa.csv", mode="r") as file:
            rows = list(csv.reader(file))
        
        # Cari dan update data berdasarkan nomor yang dipilih oleh pengguna (index)
        selected_row = data_sewa[int(pilihan) - 1]  # Dapatkan data yang dipilih
        for row in rows:
            if len(row) > 7 and row[0] == selected_row[0] and row[2] == str(user_id):  # Cek berdasarkan ID Sewa dan ID Penyewa
                row[7] = status_baru  # Mengubah status pada kolom yang sesuai
                break  # Hanya update satu baris yang dipilih

        # Menulis ulang file sewa.csv dengan baris yang telah diupdate
        with open("sewa.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"\nStatus berhasil diubah menjadi '{status_baru}'.")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)

    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e.filename}")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)

# PEMILIK LAHAN =========

# Fungsi CRUD untuk lahan
def crud_lahan(user_id):
    print("\n=== Data Lahan ===")
    print("[1] Tambah Lahan")
    print("[2] Lihat Semua Lahan")
    print("[0] Kembali")
    pilihan = input("Pilih menu: ")
    
    if pilihan == '1':
        tambah_lahan(user_id)
    elif pilihan == '2':
        lihat_lahan(user_id)
    elif pilihan == '0':
        show_menu("pemilik_lahan", user_id)
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        crud_lahan(user_id)

def tambah_lahan(user_id):
    print("\n=== Tambah Lahan ===")
    lahan_id = get_next_id("lahan.csv")  # ID lahan otomatis
    lokasi = input("Masukkan lokasi lahan: ")
    tanaman = input("Masukkan jenis tanaman (pisahkan dengan koma, contoh: padi,jagung): ")
    deskripsi = input("Masukkan deskripsi lahan: ")
    luas = input("Masukkan luas tanah (dalam hektar): ")
    harga_per_hektar = input("Masukkan harga per hektar: ")

    # Simpan ke CSV
    with open("lahan.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([lahan_id, user_id, lokasi, tanaman, deskripsi, luas, harga_per_hektar])
    
    print("Lahan berhasil ditambahkan!")
    crud_lahan(user_id)

def lihat_lahan(user_id):
    print("\n=== Daftar Lahan ===")
    print(f"{'ID':<5} {'Lokasi':<15} {'Tanaman':<20} {'Luas':<10} {'Harga':<10}")
    print("="*60)
    lahan_ada = False  # Penanda jika ada data
    
    try:
        with open("lahan.csv", mode="r") as file:
            reader = csv.reader(file)
            lahan_data = list(reader)
            for row in lahan_data:
                if row[1] == user_id:  # Hanya tampilkan lahan milik user
                    lahan_ada = True
                    print(f"{row[0]:<5} {row[2]:<15} {row[3]:<20} {row[5]:<10} {row[6]:<10}")
    except FileNotFoundError:
        print("Belum ada data lahan.")
    
    if not lahan_ada:
        print("Tidak ada data lahan milik Anda.")
        input("\nTekan Enter untuk kembali.")
        crud_lahan(user_id)
        return

    print("\n[1] Hapus Lahan")
    print("[0] Kembali")
    pilihan = input("Pilih menu: ")
    if pilihan == '1':
        hapus_lahan(user_id, lahan_data)
    elif pilihan == '0':
        crud_lahan(user_id)
    else:
        print("Pilihan tidak valid.")
        lihat_lahan(user_id)

def list_penyewa(user_id):
    print("\n=== List Penyewa ===")
    try:
        with open("lahan.csv", mode="r") as lahan_file, open("sewa.csv", mode="r") as sewa_file, open("users.csv", mode="r") as users_file:
            lahan_reader = csv.reader(lahan_file)
            sewa_reader = csv.reader(sewa_file)
            users_reader = list(csv.reader(users_file))  # Simpan semua data pengguna untuk pencarian
            
            # Ambil semua lahan milik pemilik
            lahan_pemilik = [lahan for lahan in lahan_reader if lahan[1] == user_id]
            if not lahan_pemilik:
                print("Anda belum memiliki lahan terdaftar.")
                return
            
            # Ambil data penyewaan terkait berdasarkan ID Lahan
            sewa_terkait = [sewa for sewa in sewa_reader if any(sewa[2] == lahan[0] for lahan in lahan_pemilik)]
            if not sewa_terkait:
                print("Belum ada penyewa untuk lahan Anda.")
                return
            
            print(f"{'No':<5} {'ID Lahan':<10} {'Lokasi':<20} {'Nama Penyewa':<20} {'Status':<15}")
            print("=" * 70)
            penyewa_dict = {}
            
            for i, sewa in enumerate(sewa_terkait, start=1):
                # Cari lahan berdasarkan ID Lahan
                lahan = next((l for l in lahan_pemilik if l[0] == sewa[2]), None)
                if not lahan:
                    print(f"ID Lahan {sewa[2]} tidak ditemukan.")
                    continue  # Lewati jika lahan tidak ditemukan
                
                # Cari pengguna berdasarkan ID Pengguna
                penyewa = next((u for u in users_reader if u[0] == sewa[1]), None)  # Cari berdasarkan ID Pengguna
                if not penyewa:
                    print(f"ID Pengguna {sewa[1]} tidak ditemukan.")
                    continue  # Lewati jika pengguna tidak ditemukan
                
                penyewa_dict[str(i)] = (sewa, lahan, penyewa)
                print(f"{i:<5} {lahan[0]:<10} {lahan[2]:<20} {penyewa[1]:<20} {sewa[7]:<15}")
            
            pilihan = input("\nPilih nomor untuk melihat detail (0 untuk kembali): ")
            if pilihan == "0":
                show_menu("pemilik_lahan", user_id)
            if pilihan in penyewa_dict:
                detail_penyewa(penyewa_dict[pilihan], user_id)
            else:
                print("Nomor tidak valid.")
    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e}")

def detail_penyewa(data, user_id):
    sewa, lahan, penyewa = data
    print("\n=== Detail Penyewa ===")
    print(f"Nama Penyewa: {penyewa[1]}")
    print(f"Email Penyewa: {penyewa[2]}")
    print(f"No KTP: {penyewa[4]}")
    print(f"Lokasi Lahan: {lahan[2]}")
    print(f"Deskripsi: {lahan[4]}")
    print(f"Luas yang Disewa: {sewa[2]} hektar")
    print(f"Tanggal Sewa: {sewa[4]}")
    print(f"Tanggal Berakhir: {sewa[3]}")
    print(f"Total Harga: Rp {float(sewa[6]):,.2f}")  # Changed from sewa[6] to sewa[5]
    print(f"Status: {sewa[7]}")

    if sewa[7].lower() == "Belum Berjalan":
        # Jika status sudah "Belum Berjalan", tanyakan apakah ingin menghapus data
        konfirmasi = input("\nStatus sudah 'Belum Berjalan'. Apakah Anda ingin menghapus data ini? (y/n): ").lower()
        if konfirmasi == 'y':
            hapus_data_sewa(sewa)
            print("Data sewa berhasil dihapus.")
        else:
            print("Data sewa tidak dihapus.")
    elif sewa[7].lower() == "Selesai":
        # Jika status sudah "Selesai", kembali ke menu List Penyewa
        input("\nStatus sudah 'Selesai'. Tekan Enter untuk kembali ke List Penyewa.")
    else:
        # Jika status belum "Belum Berjalan", tanyakan apakah ingin menyetujui perjanjian
        konfirmasi = input("\nApakah Anda ingin menyetujui perjanjian ini? (y/n): ").lower()
        if konfirmasi == 'y':
            update_status_sewa(sewa)
            print("Perjanjian berhasil disetujui. Status diperbarui menjadi 'Belum Berjalan'.")
        else:
            print("Perjanjian tidak disetujui.")

    # Setelah selesai melihat detail, kembali ke List Penyewa
    list_penyewa(user_id)

# Contoh fungsi untuk menghapus data (dummy function)
def hapus_data_sewa(sewa):
    print(f"Data sewa dengan ID {sewa[0]} telah dihapus.")

def update_status_sewa(sewa):
    # Baca semua data sewa
    with open("sewa.csv", mode="r") as file:
        rows = list(csv.reader(file))
    
    # Ubah status pada data yang sesuai
    for row in rows:
        if row[:7] == sewa[:7]:  # Bandingkan semua field kecuali status
            row[7] = "Belum Berjalan"
    
    # Tulis ulang data ke file
    with open("sewa.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Fungsi untuk menghapus lahan berdasarkan ID
def hapus_lahan(user_id, lahan_data):
    print("\n=== Hapus Lahan ===")
    id_lahan = input("Masukkan ID Lahan yang ingin dihapus: ")
    lahan_dihapus = False

    # Filter data untuk menghapus lahan sesuai ID dan pemilik
    with open("lahan.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        for row in lahan_data:
            if row[0] == id_lahan and row[1] == user_id:
                lahan_dihapus = True
            else:
                writer.writerow(row)
    
    if lahan_dihapus:
        print(f"Lahan dengan ID {id_lahan} berhasil dihapus.")
    else:
        print(f"Lahan dengan ID {id_lahan} tidak ditemukan atau bukan milik Anda.")
    
    input("\nTekan Enter untuk kembali.")
    lihat_lahan(user_id)

# ADMIN =================
def rekap_penyewaan(user_id):
    try:
        # Membaca file CSV
        with open("sewa.csv", "r") as sewa_file, open("users.csv", "r") as user_file, open("lahan.csv", "r") as lahan_file:
            sewa_reader = csv.reader(sewa_file)
            user_reader = csv.reader(user_file)
            lahan_reader = csv.reader(lahan_file)

            # Membuat mapping untuk user dan lahan
            user_map = {row[0]: row[1] for row in user_reader if len(row) >= 2}  # id_user -> nama_user
            lahan_map = {
                row[0]: {"lokasi": row[2], "id_pemilik": row[1]} for row in lahan_reader if len(row) >= 3
            }  # id_lahan -> {lokasi, id_pemilik}

            print("\n=== List Penyewa ===")
            print(f"{'No':<5} {'ID Lahan':<10} {'Lokasi':<20} {'Nama Penyewa':<20} {'Nama Pemilik':<20} {'Status':<15}")
            print("=" * 80)

            # Menampilkan data penyewaan
            sewa_list = [row for row in sewa_reader if len(row) >= 8]  # Pastikan ada minimal 8 kolom sesuai format baru
            if not sewa_list:
                print("Tidak ada data penyewaan.")
                input("\nTekan Enter untuk kembali.")
                show_menu("admin", user_id)
                return

            for i, sewa in enumerate(sewa_list):
                id_lahan = sewa[2]  # Menggunakan ID Lahan yang ada pada kolom 3
                id_penyewa = sewa[1]  # Menggunakan ID Pengguna yang ada pada kolom 2
                lokasi_lahan = lahan_map.get(id_lahan, {}).get("lokasi", "Unknown")
                id_pemilik = lahan_map.get(id_lahan, {}).get("id_pemilik", "Unknown")
                nama_penyewa = user_map.get(id_penyewa, "Unknown")
                nama_pemilik = user_map.get(id_pemilik, "Unknown")
                status = sewa[7]  # Status pada kolom 8

                print(
                    f"{i+1:<5} {id_lahan:<10} {lokasi_lahan:<20} {nama_penyewa:<20} {nama_pemilik:<20} {status:<15}"
                )

            # Meminta input untuk detail
            while True:
                pilihan = input("\nMasukkan nomor untuk melihat detail (atau 0 untuk kembali): ")
                if pilihan == "0":
                    show_menu("admin", user_id)
                    return
                if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(sewa_list):
                    print("Pilihan tidak valid. Silakan coba lagi.")
                    continue

                # Tampilkan detail penyewaan
                index = int(pilihan) - 1
                detail = sewa_list[index]
                tampilkan_detail(detail, user_map, lahan_map)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        input("\nTekan Enter untuk kembali.")
        show_menu("admin", user_id)


def tampilkan_detail(sewa, user_map, lahan_map):
    try:
        # Menyesuaikan dengan kolom pada sewa.csv
        id_sewa = sewa[0]  # ID Sewa (kolom 1)
        id_penyewa = sewa[1]  # ID Pengguna (kolom 2)
        id_lahan = sewa[2]  # ID Lahan (kolom 3)
        tanggal_mulai = sewa[3]  # Tanggal Mulai (kolom 4)
        tanggal_selesai = sewa[4]  # Tanggal Selesai (kolom 5)
        durasi = sewa[5]  # Durasi (kolom 6)
        total_biaya = sewa[6]  # Total Biaya (kolom 7)
        status = sewa[7]  # Status (kolom 8)

        # Mengambil data lokasi dan pemilik lahan
        lokasi_lahan = lahan_map.get(id_lahan, {}).get("lokasi", "Unknown")
        id_pemilik = lahan_map.get(id_lahan, {}).get("id_pemilik", "Unknown")

        # Mengambil nama penyewa dan nama pemilik
        nama_penyewa = user_map.get(id_penyewa, "Unknown")
        nama_pemilik = user_map.get(id_pemilik, "Unknown")

        # Menampilkan detail penyewaan
        print("\n=== Detail Penyewaan ===")
        print(f"ID Penyewa     : {id_penyewa}")
        print(f"Nama Penyewa   : {nama_penyewa}")
        print(f"ID Sewa        : {id_sewa}")
        print(f"ID Lahan       : {id_lahan}")
        print(f"Lokasi Lahan   : {lokasi_lahan}")
        print(f"Nama Pemilik   : {nama_pemilik}")
        print(f"Tanggal Mulai  : {tanggal_mulai}")
        print(f"Tanggal Selesai: {tanggal_selesai}")
        print(f"Durasi         : {durasi} tahun")
        print(f"Total Biaya    : Rp {float(total_biaya):,.0f}")
        print(f"Status         : {status}")
        print("=" * 30)

    except Exception as e:
        print(f"Terjadi kesalahan saat menampilkan detail: {e}")

def rekap_jumlah_pengguna(user_id):
    try:
        # Membaca file CSV
        with open("users.csv", "r") as user_file, open("sewa.csv", "r") as sewa_file:
            user_reader = csv.reader(user_file)
            sewa_reader = csv.reader(sewa_file)

            # Membaca data pengguna dan memfilter berdasarkan level 'pengguna'
            users = [row for row in user_reader if len(row) >= 2 and row[-1] == 'pengguna']  # Pastikan level adalah 'pengguna'
            if not users:
                print("Tidak ada data pengguna dengan level 'pengguna'.")
                return  

            # Membaca data penyewaan
            sewa_list = [row for row in sewa_reader if len(row) >= 2]  # Pastikan ada minimal 2 kolom
            pengguna_menyewa = {sewa[1] for sewa in sewa_list}  # Set id pengguna yang melakukan penyewaan (kolom 2)

            # Menampilkan data rekap
            print("\n=== Rekap Jumlah Pengguna ===")
            print(f"Total Pengguna dengan level 'pengguna': {len(users)}")
            print(f"Total Pengguna yang Melakukan Penyewaan: {len(pengguna_menyewa)}\n")
            print(f"{'No':<5} {'ID Pengguna':<15} {'Nama Pengguna':<20} {'Status':<20}")
            print("=" * 60)

            for i, user in enumerate(users):
                id_user = user[0]
                nama_user = user[1]
                status = "Menyewa" if id_user in pengguna_menyewa else "Belum Menyewa"
                print(f"{i+1:<5} {id_user:<15} {nama_user:<20} {status:<20}")

            input("\nTekan Enter untuk kembali.")
            show_menu("admin", user_id)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Jalankan program
main_menu()