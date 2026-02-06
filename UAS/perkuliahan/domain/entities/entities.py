from dataclasses import dataclass

@dataclass
class Dosen:
    def __init__(self, id=None, nama=None, ndn=None):
        self.id = id
        self.nama = nama
        self.ndn = ndn

@dataclass
class Matakuliah:
    def __init__(self, id=None, nama=None, dosen_id=None):
        self.id = id
        self.nama = nama
        self.dosen_id = dosen_id

@dataclass
class Kelas:
    def __init__(self, id=None, nama=None, matakuliah_id=None, dosen_id=None):
        self.id = id
        self.nama = nama
        self.matakuliah_id = matakuliah_id
        self.dosen_id = dosen_id

@dataclass
class Mahasiswa:
    def __init__(self, id=None, nama=None, nim=None, kelas_id=None):
        self.id = id
        self.nama = nama
        self.nim = nim
        self.kelas_id = kelas_id
