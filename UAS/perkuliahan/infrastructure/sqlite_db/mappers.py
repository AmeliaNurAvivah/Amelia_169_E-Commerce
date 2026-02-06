from auth.domain.entities import User
from perkuliahan.domain.entities.entities import Dosen, Matakuliah, Kelas, Mahasiswa

def map_row_to_dosen(row):
    if row is None:
        return None
    return Dosen(id=row["id"], nama=row["nama"], ndn=row["ndn"])

def map_row_to_matakuliah(row):
    if row is None:
        return None
    return Matakuliah(id=row["id"], nama=row["nama"], dosen_id=row["dosen_id"])

def map_row_to_kelas(row):
    if row is None:
        return None
    return Kelas(id=row["id"], nama=row["nama"], matakuliah_id=row["matakuliah_id"], dosen_id=row["dosen_id"])

def map_row_to_mahasiswa(row):
    if row is None:
        return None
    return Mahasiswa(
        id=row["id"],
        nama=row["nama"],
        nim=row["nim"],
        kelas_id=row["kelas_id"]
    )


def user_from_dict(user_dict: dict) -> User:
    return User(
        id=user_dict["id"],
        username=user_dict["username"],
        password=user_dict["password"],
        status=user_dict["status"],
    )
    
    