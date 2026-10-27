#tama_002
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan role pada judul jendela aplikasi
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # Menyimpan ID buku yang sedang dipilih
        self.id_buku_terpilih = None

        # Menghubungkan tombol dengan fungsi Controller
        self.view.btn_simpan.configure(
            command=self.simpan_data
        )
        self.view.btn_update.configure(
            command=self.update_data
        )
        self.view.btn_hapus.configure(
            command=self.hapus_data
        )

        # Event ketika baris tabel dipilih
        self.view.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        # Membatasi akses pengguna non-admin
        if self.user_role != "admin":
            self.view.btn_simpan.configure(
                state="disabled",
                text="Akses Terkunci (Khusus Admin)"
            )
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Memuat data saat aplikasi dibuka
        self.muat_data_tabel()

    # MENAMPILKAN DATA KE TABEL
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    # MEMILIH DATA DARI TABEL
    def pilih_data(self, event=None):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            return

        item = self.view.tabel.item(pilihan[0])
        data = item["values"]

        # Simpan ID buku yang dipilih
        self.id_buku_terpilih = data[0]

        # Masukkan data ke form jika pengguna admin
        if self.user_role == "admin":
            self.view.entry_judul.delete(0, "end")
            self.view.entry_judul.insert(0, data[1])

            self.view.entry_penulis.delete(0, "end")
            self.view.entry_penulis.insert(0, data[2])

            self.view.entry_tahun.delete(0, "end")
            self.view.entry_tahun.insert(0, data[3])

    # MEMBERSIHKAN FORM
    def bersihkan_form(self):
        if self.user_role == "admin":
            self.view.entry_judul.delete(0, "end")
            self.view.entry_penulis.delete(0, "end")
            self.view.entry_tahun.delete(0, "end")

        self.id_buku_terpilih = None

        # Hilangkan seleksi tabel
        for item in self.view.tabel.selection():
            self.view.tabel.selection_remove(item)

    # MENYIMPAN DATA BARU
    def simpan_data(self):
        # Pemeriksaan hak akses
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menambah data!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        try:
            tahun = int(tahun)
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return

        berhasil = self.model.create_buku(
            judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data gagal disimpan. Periksa koneksi database."
            )

    # MEMPERBARUI DATA
    def update_data(self):
        # Pemeriksaan hak akses
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk memperbarui data!"
            )
            return

        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku dari tabel terlebih dahulu!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        try:
            tahun = int(tahun)
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin memperbarui data buku ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.update_buku(
            self.id_buku_terpilih,
            judul,
            penulis,
            tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data gagal diperbarui. Periksa koneksi database."
            )

    # MENGHAPUS DATA
    def hapus_data(self):
        # Pemeriksaan hak akses
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menghapus data!"
            )
            return

        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku dari tabel terlebih dahulu!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Apakah kamu yakin ingin menghapus data buku ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(
            self.id_buku_terpilih
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data gagal dihapus. Periksa koneksi database."
            )

    # MENJALANKAN APLIKASI
    def run(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = BukuController(user_role="admin")
    app.run()
