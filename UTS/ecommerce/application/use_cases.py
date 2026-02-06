# ecommerce/application/use_cases.py
from ecommerce.domain.repositories.repositories import (
    KategoriRepository,
    LokasiRepository,
    ProdukRepository,
    KeranjangRepository
)

class ProdukUseCase:
    def __init__(self):
        self.produk_repo = ProdukRepository()
        self.kategori_repo = KategoriRepository()
        self.lokasi_repo = LokasiRepository()

    def list_produk(self, kategori_id=None, lokasi_id=None, min_harga=None, max_harga=None, q=None):
        return self.produk_repo.get_filtered(
            kategori_id, lokasi_id, min_harga, max_harga, q
        )
        
    def tambah_produk(self, nama, kategori_nama, lokasi_nama, harga, keterangan, gambar):
        kategori_id = self.kategori_repo.get_or_create(kategori_nama)
        lokasi_id = self.lokasi_repo.get_or_create(lokasi_nama)

        self.produk_repo.add(
            nama=nama,
            kategori_id=kategori_id,
            lokasi_id=lokasi_id,
            harga=harga,
            keterangan=keterangan,
            gambar=gambar
        )

    # 🔥 REVISI BARU
    def update_produk(self, produk_id, data, file):
        self.produk_repo.update(produk_id, data, file)

    def hapus_produk(self, produk_id):
        self.produk_repo.delete(produk_id)


class KategoriUseCase:
    def __init__(self):
        self.repo = KategoriRepository()

    def list_kategori(self):
        return self.repo.get_all()


class LokasiUseCase:
    def __init__(self):
        self.repo = LokasiRepository()

    def list_lokasi(self):
        return self.repo.get_all()


class KeranjangUseCase:
    def __init__(self):
        self.repo = KeranjangRepository()

    def list_keranjang(self):
        return self.repo.get_all()

    def total_keranjang(self):
        items = self.repo.get_all()
        return sum(item.subtotal for item in items)

    def tambah_ke_keranjang(self, produk_id, jumlah=1):
        item = self.repo.get_by_produk(produk_id)
        if item:
            self.repo.update_jumlah(item["id"], item["jumlah"] + jumlah)
        else:
            self.repo.add(produk_id, jumlah)

    def hapus_dari_keranjang(self, keranjang_id):
        self.repo.delete(keranjang_id)

    def kosongkan_keranjang(self):
        self.repo.delete_all()
