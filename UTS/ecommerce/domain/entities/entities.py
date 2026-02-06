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