from dataclasses import dataclass

# =====================
# KATEGORI
# =====================
@dataclass
class Kategori:
    id: int | None = None
    nama: str | None = None


# =====================
# PRODUK
# =====================
@dataclass
class Produk:
    id: int | None = None
    nama: str | None = None
    kategori_id: int | None = None
    kategori_nama: str | None = None
    lokasi_id: int | None = None
    lokasi_nama: str | None = None
    harga: float | None = None
    keterangan: str | None = None
    gambar: str | None = None


# =====================
# KERANJANG
# =====================
@dataclass
class Keranjang:
    id: int | None = None
    produk_id: int | None = None
    nama_produk: str | None = None
    harga: float | None = None
    jumlah: int | None = None
    subtotal: float | None = None  # hasil hitung, bukan dari DB


# =====================
# LOKASI
# =====================
@dataclass
class Lokasi:
    id: int | None = None
    nama: str | None = None
    
class Pesanan:
    def __init__(self, id=None, tanggal=None, total=0, metode_pembayaran="", status=""):
        self.id = id
        self.tanggal = tanggal
        self.total = total
        self.metode_pembayaran = metode_pembayaran
        self.status = status


class PesananItem:
    def __init__(self, id=None, pesanan_id=None, produk_id=None,
                 nama_produk="", harga=0, jumlah=0, subtotal=0):
        self.id = id
        self.pesanan_id = pesanan_id
        self.produk_id = produk_id
        self.nama_produk = nama_produk
        self.harga = harga
        self.jumlah = jumlah
        self.subtotal = subtotal
