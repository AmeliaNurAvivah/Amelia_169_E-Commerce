# ecommerce/application/use_cases.py
from ecommerce.domain.repositories.repositories import (
    KategoriRepository,
    LokasiRepository,
    ProdukRepository,
    KeranjangRepository,
)

# ambil yang konkret dari infrastructure
from ecommerce.infrastructure.sqlite_db.repositories.pesanan_repository import SQLitePesananRepository

from datetime import datetime
from ecommerce.domain.entities.entities import Pesanan, PesananItem


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
    def tambah_jumlah(self, keranjang_id):
        items = self.repo.get_all()
        item = next((k for k in items if k.id == keranjang_id), None)

        if item:
            jumlah_baru = item.jumlah + 1
            self.repo.update_jumlah(keranjang_id, jumlah_baru)

    def kurangi_jumlah(self, keranjang_id):
        items = self.repo.get_all()
        item = next((k for k in items if k.id == keranjang_id), None)

        if item and item.jumlah > 1:
            jumlah_baru = item.jumlah - 1
            self.repo.update_jumlah(keranjang_id, jumlah_baru)

class PesananUseCase:
    def __init__(self, keranjang_uc):
        self.repo = SQLitePesananRepository()
        self.keranjang_uc = keranjang_uc

    def buat_pesanan(self, metode):
        keranjang = self.keranjang_uc.list_keranjang()
        total = self.keranjang_uc.total_keranjang()

        pesanan = Pesanan(
            tanggal=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total=total,
            metode_pembayaran=metode,
            status="Menunggu"
        )

        items = []
        for k in keranjang:
            items.append(
                PesananItem(
                    produk_id=k.produk_id,
                    nama_produk=k.nama_produk,
                    harga=k.harga,
                    jumlah=k.jumlah,
                    subtotal=k.subtotal
                )
            )

        self.repo.simpan_pesanan(pesanan, items)
        self.keranjang_uc.kosongkan_keranjang()

    def list_pesanan(self):
        return self.repo.list_pesanan()

    def detail_pesanan(self, pesanan_id):
        return self.repo.detail_pesanan(pesanan_id)

    def ubah_status(self, pesanan_id, status):
        self.repo.ubah_status(pesanan_id, status)

    def hapus_pesanan(self, pesanan_id):
        self.repo.hapus_pesanan(pesanan_id)
