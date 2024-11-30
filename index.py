import csv
import hashlib
from datetime import datetime, timedelta
from fpdf import FPDF
import re  # Untuk validasi email

# Fungsi untuk mendapatkan ID berikutnya
def id_berikutnya(filename):
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
    user_id = id_berikutnya("users.csv")  # Ambil ID berikutnya
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
            for row in reader:
                if len(row) < 8: 
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
            print("Pilihan tidak valid. Silahkan coba lagi")
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
            print("Pilihan tidak valid. Silahkan coba lagi")
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
            # return

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
        else:
            print("Sewa dibatalkan.")
    except ValueError:
        print("Format tanggal tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)

def tambah_sewa(user_id, lahan, tanggal_sewa, tanggal_berakhir, luas_sewa, total_harga):
    try:
        # Membaca file lahan.csv untuk mendapatkan informasi lahan
        with open("lahan.csv", mode="r") as file:
            reader = csv.reader(file)
            lahan_data = list(reader)
        
        max_luas = None
        for row in lahan_data:
            if len(row) > 1 and row[0] == lahan[0]:  # Cocokkan ID lahan
                max_luas = float(row[5])  # Ambil luas maksimal (hektar)
                break
        
        if max_luas is None:
            print("ID lahan tidak ditemukan. Pastikan data 'lahan.csv' benar.")
            return

        # Membaca file sewa.csv untuk mengecek total luas yang telah disewa
        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            sewa_data = list(reader)
        
        total_luas_disewa = 0
        for row in sewa_data:
            if len(row) > 5 and row[2] == lahan[0]:  # Cocokkan ID lahan
                sewa_start = datetime.strptime(row[3], "%Y-%m-%d")
                sewa_end = datetime.strptime(row[4], "%Y-%m-%d")
                input_start = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
                input_end = datetime.strptime(tanggal_berakhir, "%Y-%m-%d")
                
                # Cek apakah rentang tanggal bertumpang tindih
                if not (input_end < sewa_start or input_start > sewa_end):
                    total_luas_disewa += float(row[5])  # Tambahkan luas sewa
        
        # Validasi apakah masih ada sisa luas yang tersedia
        if total_luas_disewa + luas_sewa > max_luas:
            print(f"Lahan sudah tersewa penuh untuk tanggal tersebut. Total luas tersedia: {max_luas - total_luas_disewa} hektar.")
            return

        # Membaca file users.csv untuk mendapatkan nomor telepon pemilik
        with open("users.csv", mode="r") as file:
            reader = csv.reader(file)
            users_data = list(reader)
        
        id_pemilik = None
        nomor_telepon_pemilik = None
        for row in lahan_data:
            if row[0] == lahan[0]:
                id_pemilik = row[1]
                break
        
        for row in users_data:
            if row[0] == id_pemilik and row[7] == "pemilik_lahan":  # Cocokkan ID pemilik dan role
                nomor_telepon_pemilik = row[5]  # Ambil nomor telepon
                break

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
        print(f"Untuk perjanjian, dapat menghubungi nomor telepon pemilik lahan: {nomor_telepon_pemilik}")
        print("Sewa berhasil ditambahkan. Menunggu perjanjian.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def get_username(user_id):
    # Fungsi sederhana untuk mendapatkan nama pengguna dari file users.csv
    with open("users.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[0] == str(user_id):
                return row[1]  # Nama pengguna
    return "Unknown"


def data_perjanjian(user_id):
    print("\n=== Data Perjanjian ===")
    print(f"{'No':<5} {'Lokasi':<30} {'Tanggal Sewa':<15} {'Tanggal Berakhir':<15} {'Status':<20}  {'ID Lahan':<10}")
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
        show_menu("pengguna", user_id)
        return

    # Menampilkan data perjanjian yang difilter dengan nomor urut dimulai dari 1
    for i, row in enumerate(data_sewa, start=1):
        lokasi_id = row[2]  # ID lokasi ada di kolom ketiga (index 2) dari sewa.csv
        lokasi_name = lokasi_dict.get(lokasi_id, "Tidak Dikenal")  # Mendapatkan nama lokasi dari dictionary
        tanggal_sewa = row[3]  # Tanggal Sewa ada di kolom ke-4
        tanggal_berakhir = row[4]  # Tanggal Berakhir ada di kolom ke-5
        status = row[7]  # Status ada di kolom ke-8
        id_lahan = row[2]  # ID lahan ada di kolom ke-3

        # Menampilkan data perjanjian
        print(f"{i:<5} {lokasi_name:<30} {tanggal_sewa:<15} {tanggal_berakhir:<15} {status:<20} {id_lahan:<10}")

    pilihan = input("\nMasukkan nomor perjanjian untuk dibuat (atau 0 untuk batal): ")
    if pilihan.isdigit() and 1 <= int(pilihan) <= len(data_sewa):
        nomor = int(pilihan) - 1
        buat_surat_perjanjian(data_sewa[nomor], user_id)
        print("Surat perjanjian berhasil dibuat dan disimpan sebagai PDF.")
    else:
        print("Pilihan tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)

def buat_surat_perjanjian(data, user_id):
    print("Pengembangan")

def lihat_history(user_id):
    print("Pengembangan")

def list_penyewa(user_id):
    print("Pengembangan")

def crud_lahan(user_id):
    print("Pengembangan")
    
def rekap_penyewaan(user_id):
    print("Pengembangan")

def jumlah_pengguna():
    print("Pengembangan")
    
def rekap_jumlah_pengguna():
    print("Pengembangan")


# Jalankan program
main_menu()