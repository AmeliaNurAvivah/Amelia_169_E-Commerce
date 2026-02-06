from abc import ABC, abstractmethod
from perkuliahan.domain.entities.entities import Dosen, Matakuliah, Kelas
from perkuliahan.infrastructure.sqlite_db.db_settings import get_connection
from perkuliahan.infrastructure.sqlite_db.mappers import map_row_to_dosen, map_row_to_matakuliah, map_row_to_kelas, map_row_to_mahasiswa


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def get_by_id(self, id): pass

    @abstractmethod
    def add(self, *args, **kwargs): pass

    @abstractmethod
    def update(self, *args, **kwargs): pass

    @abstractmethod
    def delete(self, id): pass
    
class DosenRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM dosen ORDER BY id").fetchall()
        conn.close()
        return [map_row_to_dosen(r) for r in rows]

    def get_by_id(self, id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM dosen WHERE id=?", (id,)).fetchone()
        conn.close()
        return map_row_to_dosen(row)

    def add(self, nama, ndn):
        conn = get_connection()
        conn.execute("INSERT INTO dosen (nama, ndn) VALUES (?, ?)", (nama, ndn))
        conn.commit()
        conn.close()

    def update(self, id, nama, ndn):
        conn = get_connection()
        conn.execute("UPDATE dosen SET nama=?, ndn=? WHERE id=?", (nama, ndn, id))
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = get_connection()
        conn.execute("DELETE FROM dosen WHERE id=?", (id,))
        conn.commit()
        conn.close()


class MatakuliahRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM matakuliah ORDER BY id").fetchall()
        conn.close()
        return [map_row_to_matakuliah(r) for r in rows]

    def add(self, nama, dosen_id):
        conn = get_connection()
        conn.execute("INSERT INTO matakuliah (nama, dosen_id) VALUES (?, ?)", (nama, dosen_id))
        conn.commit()
        conn.close()

    def update(self, id, nama, dosen_id):
        conn = get_connection()
        conn.execute("UPDATE matakuliah SET nama=?, dosen_id=? WHERE id=?", (nama, dosen_id, id))
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = get_connection()
        conn.execute("DELETE FROM matakuliah WHERE id=?", (id,))
        conn.commit()
        conn.close()


class KelasRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM kelas ORDER BY id").fetchall()
        conn.close()
        return [map_row_to_kelas(r) for r in rows]

    def add(self, nama, matakuliah_id, dosen_id):
        conn = get_connection()
        conn.execute("INSERT INTO kelas (nama, matakuliah_id, dosen_id) VALUES (?, ?, ?)", (nama, matakuliah_id, dosen_id))
        conn.commit()
        conn.close()

    def update(self, id, nama, matakuliah_id, dosen_id):
        conn = get_connection()
        conn.execute("UPDATE kelas SET nama=?, matakuliah_id=?, dosen_id=? WHERE id=?", (nama, matakuliah_id, dosen_id, id))
        conn.commit()
        conn.close()
        
    def get_by_id(self, id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM kelas WHERE id=?",
            (id,)
        ).fetchone()
        conn.close()
        return map_row_to_kelas(row)

    def delete_by_id(self, id):
        conn = get_connection()
        conn.execute("DELETE FROM kelas WHERE id=?", (id,))
        conn.commit()
        conn.close()
        
        
class MahasiswaRepository:
    def get_by_kelas(self, kelas_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM mahasiswa WHERE kelas_id=? ORDER BY id",
            (kelas_id,)
        ).fetchall()
        conn.close()
        return [map_row_to_mahasiswa(r) for r in rows]

    def add(self, nama, nim, kelas_id):
        conn = get_connection()
        conn.execute(
            "INSERT INTO mahasiswa (nama, nim, kelas_id) VALUES (?, ?, ?)",
            (nama, nim, kelas_id)
        )
        conn.commit()
        conn.close()

    def update(self, id, nama, nim):
        conn = get_connection()
        conn.execute(
            "UPDATE mahasiswa SET nama=?, nim=? WHERE id=?",
            (nama, nim, id)
        )
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = get_connection()
        conn.execute("DELETE FROM mahasiswa WHERE id=?", (id,))
        conn.commit()
        conn.close()


class IDosenRepository(BaseRepository):
    pass


class IMatakuliahRepository(BaseRepository):
    @abstractmethod
    def get_by_dosen(self, dosen_id: int) -> list[Matakuliah]:
        pass


class IKelasRepository(BaseRepository):
    @abstractmethod
    def get_by_matakuliah(self, matakuliah_id: int) -> list[Kelas]:
        pass