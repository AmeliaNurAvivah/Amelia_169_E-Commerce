from auth.domain.entities import User
from ecommerce.domain.entities.entities import Kategori, Produk, Keranjang

# ======================
# KATEGORI MAPPER
# ======================
def map_row_to_kategori(row) -> Kategori:
    if row is None:
        return None
    return Kategori(
        id=row["id"],
        nama=row["nama"]
    )

# ======================
# PRODUK MAPPER
# ======================
def map_row_to_produk(row) -> Produk:
    if row is None:
        return None
    return Produk(
        id=row["id"],
        nama=row["nama"],
        kategori_id=row["kategori_id"],
        lokasi=row.get("lokasi"),
        keterangan=row.get("keterangan"),
        harga=row.get("harga"),
        gambar=row.get("gambar")
    )

# ======================
# KERANJANG MAPPER
# ======================
def map_row_to_keranjang(row) -> Keranjang:
    if row is None:
        return None
    return Keranjang(
        id=row["id"],
        produk=None,  # objek Produk akan diisi di use case
        produk_id=row["produk_id"],
        jumlah=row.get("jumlah", 0)
    )



def user_from_dict(user_dict: dict) -> User:
    return User(
        id=user_dict["id"],
        username=user_dict["username"],
        password=user_dict["password"],
        status=user_dict["status"],
    )
    
    