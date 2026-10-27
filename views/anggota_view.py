
import customtkinter as ctk
from tkinter import ttk


class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Perpustakaan - Data Anggota")
        self.geometry("800x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ================= FRAME KIRI =================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Anggota",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Input nama anggota
        self.entry_nama = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Anggota"
        )
        self.entry_nama.pack(
            pady=10, padx=15, fill="x"
        )

        # Input alamat anggota
        self.entry_alamat = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Alamat"
        )
        self.entry_alamat.pack(
            pady=10, padx=15, fill="x"
        )

        # Tombol simpan
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green"
        )
        self.btn_simpan.pack(
            pady=10, padx=15, fill="x"
        )

        # Tombol update
        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color="blue"
        )
        self.btn_update.pack(
            pady=10, padx=15, fill="x"
        )

        # Tombol hapus
        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="red"
        )
        self.btn_hapus.pack(
            pady=10, padx=15, fill="x"
        )

        # Tombol bersihkan form
        self.btn_bersihkan = ctk.CTkButton(
            self.frame_kiri,
            text="Bersihkan Form",
            fg_color="gray"
        )
        self.btn_bersihkan.pack(
            pady=10, padx=15, fill="x"
        )

        # ================= FRAME KANAN =================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(
            row=0, column=1, padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Anggota Perpustakaan",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Tabel anggota
        kolom = ("id_anggota", "nama", "alamat")

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=15
        )

        self.tabel.heading("id_anggota", text="ID")
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")

        self.tabel.column(
            "id_anggota", width=50, anchor="center"
        )
        self.tabel.column("nama", width=150)
        self.tabel.column("alamat", width=250)

        self.tabel.pack(
            fill="both", expand=True, padx=15, pady=10
        )


if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()
