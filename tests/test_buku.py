
from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()


def test_get_all_buku():
    # Membuat objek BukuModel tanpa menjalankan koneksi database
    model = BukuModel.__new__(BukuModel)
    model.table_name = "buku"
    model.conn = MagicMock()

    # Menyiapkan cursor dan data buku tiruan
    cursor = MagicMock()
    model.conn.cursor.return_value = cursor

    data_buku = [
        {
            "id_buku": 1,
            "judul": "Pemrograman Python",
            "penulis": "Budi",
            "tahun_terbit": 2024
        }
    ]

    cursor.fetchall.return_value = data_buku

    # Memanggil fungsi yang diuji
    hasil = model.get_all_buku()

    # Memastikan hasil sesuai dengan data yang diharapkan
    assert hasil == data_buku

    # Memastikan query dijalankan dengan benar
    cursor.execute.assert_called_once_with("SELECT * FROM buku")

    # Memastikan cursor ditutup
    cursor.close.assert_called_once()
