from config.database import Database


class AnggotaModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "anggota"

    # READ: Mengambil semua data anggota
    def get_all_anggota(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    f"SELECT * FROM {self.table_name} ORDER BY id_anggota"
                )
                return cursor.fetchall()
            except Exception as e:
                print("Gagal mengambil data anggota:", e)
                return []
            finally:
                cursor.close()
        return []

    # CREATE: Menambahkan anggota baru
    def create_anggota(self, nama, alamat):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = f"""
                    INSERT INTO {self.table_name} (nama, alamat)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (nama, alamat))
                self.conn.commit()
                return True
            except Exception as e:
                self.conn.rollback()
                print("Gagal menyimpan anggota:", e)
                return False
            finally:
                cursor.close()
        return False

    # UPDATE: Memperbarui anggota berdasarkan ID
    def update_anggota(self, id_anggota, nama, alamat):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = f"""
                    UPDATE {self.table_name}
                    SET nama = %s, alamat = %s
                    WHERE id_anggota = %s
                """
                cursor.execute(query, (nama, alamat, id_anggota))
                self.conn.commit()
                return cursor.rowcount >= 0
            except Exception as e:
                self.conn.rollback()
                print("Gagal memperbarui anggota:", e)
                return False
            finally:
                cursor.close()
        return False

    # DELETE: Menghapus anggota berdasarkan ID
    def delete_anggota(self, id_anggota):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = f"""
                    DELETE FROM {self.table_name}
                    WHERE id_anggota = %s
                """
                cursor.execute(query, (id_anggota,))
                self.conn.commit()
                return cursor.rowcount == 1
            except Exception as e:
                self.conn.rollback()
                print("Gagal menghapus anggota:", e)
                return False
            finally:
                cursor.close()
        return False
    