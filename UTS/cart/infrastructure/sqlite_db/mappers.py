from domain.entities.entities import Produk, KeranjangItem

def map_produk(row):
    return Produk(
        id=row[0],
        nama=row[1],
        harga=row[2]
    )


def map_keranjang(row):
    return KeranjangItem(
        id=row[0],
        produk_id=row[1],
        nama_produk=row[2],
        harga=row[3],
        jumlah=row[4]
    )
