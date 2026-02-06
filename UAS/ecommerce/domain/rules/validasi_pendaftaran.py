class ValidasiPendaftaran:

    @staticmethod
    def boleh_daftar(mahasiswa, mata_kuliah, sudah_terdaftar: bool):

        if mahasiswa is None:
            return False, "Mahasiswa tidak ditemukan"

        if mata_kuliah is None:
            return False, "Mata kuliah tidak ditemukan"

        if sudah_terdaftar:
            return False, "Mahasiswa sudah terdaftar di mata kuliah ini"

        return True, "Valid"
