import sqlite3
import os

DB_NAME = "perpustakaan.db"


# ---------------------------------------------------------
# 1. KONEKSI & SETUP DATABASE
# ---------------------------------------------------------
def get_connection():   
    """Membuka koneksi ke database SQLite3."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_database():
    """Membuat tabel 'buku' jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            pengarang TEXT NOT NULL,
            tahun_terbit INTEGER,
            stok INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# 2. CREATE - Tambah data buku
# ---------------------------------------------------------
def tambah_buku():
    print("\n--- TAMBAH BUKU BARU ---")
    judul = input("Judul buku      : ").strip()
    pengarang = input("Pengarang       : ").strip()

    if judul == "" or pengarang == "":
        print(">> Judul dan Pengarang tidak boleh kosong!")
        return

    tahun_terbit = input_angka("Tahun terbit    : ")
    stok = input_angka("Stok buku       : ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO buku (judul, pengarang, tahun_terbit, stok) VALUES (?, ?, ?, ?)",
        (judul, pengarang, tahun_terbit, stok)
    )
    conn.commit()
    conn.close()
    print(f">> Buku '{judul}' berhasil ditambahkan!")


# ---------------------------------------------------------
# 3. READ - Lihat semua data buku
# ---------------------------------------------------------
def lihat_semua_buku():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku ORDER BY id ASC")
    data = cursor.fetchall()
    conn.close()

    print("\n--- DAFTAR SEMUA BUKU ---")
    tampilkan_tabel(data)


# ---------------------------------------------------------
# 4. READ - Cari buku berdasarkan judul/pengarang
# ---------------------------------------------------------
def cari_buku():
    print("\n--- CARI BUKU ---")
    kata_kunci = input("Masukkan judul/pengarang yang dicari: ").strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM buku WHERE judul LIKE ? OR pengarang LIKE ?",
        (f"%{kata_kunci}%", f"%{kata_kunci}%")
    )
    data = cursor.fetchall()
    conn.close()

    if not data:
        print(">> Data tidak ditemukan.")
    else:
        tampilkan_tabel(data)


# ---------------------------------------------------------
# 5. UPDATE - Ubah data buku
# ---------------------------------------------------------
def update_buku():
    print("\n--- UPDATE DATA BUKU ---")
    lihat_semua_buku()

    id_buku = input_angka("\nMasukkan ID buku yang ingin diupdate: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku WHERE id = ?", (id_buku,))
    buku = cursor.fetchone()

    if not buku:
        print(">> ID buku tidak ditemukan.")
        conn.close()
        return

    print(f"\nData saat ini -> Judul: {buku[1]} | Pengarang: {buku[2]} | Tahun: {buku[3]} | Stok: {buku[4]}")
    print("(Kosongkan input jika tidak ingin mengubah field tersebut)\n")

    judul_baru = input(f"Judul baru [{buku[1]}]        : ").strip() or buku[1]
    pengarang_baru = input(f"Pengarang baru [{buku[2]}]   : ").strip() or buku[2]

    tahun_input = input(f"Tahun terbit baru [{buku[3]}] : ").strip()
    tahun_baru = int(tahun_input) if tahun_input.isdigit() else buku[3]

    stok_input = input(f"Stok baru [{buku[4]}]          : ").strip()
    stok_baru = int(stok_input) if stok_input.isdigit() else buku[4]

    cursor.execute(
        "UPDATE buku SET judul=?, pengarang=?, tahun_terbit=?, stok=? WHERE id=?",
        (judul_baru, pengarang_baru, tahun_baru, stok_baru, id_buku)
    )
    conn.commit()
    conn.close()
    print(">> Data buku berhasil diupdate!")


# ---------------------------------------------------------
# 6. DELETE - Hapus data buku
# ---------------------------------------------------------
def hapus_buku():
    print("\n--- HAPUS DATA BUKU ---")
    lihat_semua_buku()

    id_buku = input_angka("\nMasukkan ID buku yang ingin dihapus: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku WHERE id = ?", (id_buku,))
    buku = cursor.fetchone()

    if not buku:
        print(">> ID buku tidak ditemukan.")
        conn.close()
        return

    konfirmasi = input(f"Yakin ingin menghapus '{buku[1]}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        cursor.execute("DELETE FROM buku WHERE id = ?", (id_buku,))
        conn.commit()
        print(">> Buku berhasil dihapus!")
    else:
        print(">> Penghapusan dibatalkan.")

    conn.close()


# ---------------------------------------------------------
# FUNGSI BANTUAN (HELPER)
# ---------------------------------------------------------
def tampilkan_tabel(data):
    if not data:
        print(">> Belum ada data buku.")
        return

    print(f"{'ID':<4}{'Judul':<25}{'Pengarang':<20}{'Tahun':<8}{'Stok':<6}")
    print("-" * 63)
    for row in data:
        id_, judul, pengarang, tahun, stok = row
        print(f"{id_:<4}{judul:<25}{pengarang:<20}{str(tahun):<8}{stok:<6}")


def input_angka(teks):
    """Memastikan input berupa angka, ulang jika salah."""
    while True:
        nilai = input(teks).strip()
        if nilai.isdigit():
            return int(nilai)
        print(">> Masukkan angka yang valid!")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ---------------------------------------------------------
# MENU UTAMA
# ---------------------------------------------------------
def menu_utama():
    setup_database()

    while True:
        print("\n" + "=" * 40)
        print("   APLIKASI CRUD PERPUSTAKAAN (CLI)")
        print("=" * 40)
        print("1. Tambah Buku")
        print("2. Lihat Semua Buku")
        print("3. Cari Buku")
        print("4. Update Buku")
        print("5. Hapus Buku")
        print("0. Keluar")
        print("=" * 40)

        pilihan = input("Pilih menu (0-5): ").strip()

        if pilihan == "1":
            tambah_buku()
        elif pilihan == "2":
            lihat_semua_buku()
        elif pilihan == "3":
            cari_buku()
        elif pilihan == "4":
            update_buku()
        elif pilihan == "5":
            hapus_buku()
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print(">> Pilihan tidak valid, coba lagi.")

        input("\nTekan ENTER untuk kembali ke menu...")
        clear_screen()


if __name__ == "__main__":
    menu_utama()