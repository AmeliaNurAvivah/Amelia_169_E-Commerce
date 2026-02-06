# perkuliahan/application/use_cases.py


from perkuliahan.domain.repositories.repositories import ( 
    DosenRepository, MatakuliahRepository,KelasRepository, MahasiswaRepository
)

class DosenUseCase:
    def __init__(self):
        self.repo = DosenRepository()

    def list_dosen(self):
        return self.repo.get_all()

    def get_dosen(self, id):
        return self.repo.get_by_id(id)

    def tambah_dosen(self, nama, ndn):
        if not nama or not ndn:
            raise ValueError("Nama dan NDN wajib diisi")

        try:
            self.repo.add(nama, ndn)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("NDN dosen sudah terdaftar")
            raise

    def edit_dosen(self, id, nama, ndn):
        if not id or not nama or not ndn:
            raise ValueError("Data dosen tidak lengkap")

        try:
            self.repo.update(id, nama, ndn)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("NDN sudah digunakan dosen lain")
            raise

    def hapus_dosen(self, id):
        self.repo.delete(id)


class MatakuliahUseCase:
    def __init__(self):
        self.repo = MatakuliahRepository()

    def list_matakuliah(self):
        return self.repo.get_all()

    def get_matakuliah(self, id):
        return self.repo.get_by_id(id)

    def tambah_matakuliah(self, nama, dosen_id):
        if not nama or not dosen_id:
            raise ValueError("Nama mata kuliah dan dosen wajib diisi")

        try:
            self.repo.add(nama, dosen_id)
        except Exception as e:
            # SQLite UNIQUE constraint
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("Nama mata kuliah sudah terdaftar")
            raise

    def edit_matakuliah(self, id, nama, dosen_id):
        if not id or not nama or not dosen_id:
            raise ValueError("Data mata kuliah tidak lengkap")

        try:
            self.repo.update(id, nama, dosen_id)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("Nama mata kuliah sudah digunakan")
            raise

    def hapus_matakuliah(self, id):
        self.repo.delete(id)



class KelasUseCase:
    def __init__(self):
        self.repo = KelasRepository()

    def list_kelas(self):
        return self.repo.get_all()

    def get_kelas(self, id):
        return self.repo.get_by_id(id)

    def tambah_kelas(self, nama, matakuliah_id, dosen_id):
        self.repo.add(nama, matakuliah_id, dosen_id)

    def update_kelas(self, id, nama, matakuliah_id, dosen_id):
        self.repo.update(id, nama, matakuliah_id, dosen_id)

    def delete_kelas(self, id):
        self.repo.delete_by_id(id)


class MahasiswaUseCase:
    def __init__(self):
        self.repo = MahasiswaRepository()

    def list_by_kelas(self, kelas_id):
        return self.repo.get_by_kelas(kelas_id)

    def tambah_mahasiswa(self, nama, nim, kelas_id):
        self.repo.add(nama, nim, kelas_id)

    def edit_mahasiswa(self, id, nama, nim):
        self.repo.update(id, nama, nim)

    def hapus_mahasiswa(self, id):
        self.repo.delete(id)
