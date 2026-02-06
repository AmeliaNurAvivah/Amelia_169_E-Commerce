from infrastructure.sqlite_db.db_settings import get_connection
from infrastructure.sqlite_db.mappers import map_produk, map_keranjang
from domain.repositories.repositories import (
    ProdukRepository,
    KeranjangRepository
)

class ProdukRepositoryImpl(ProdukRepository):

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM produk")
        rows = cur.fetchall()
        conn.close()
        return [map_produk(r) for r in rows]
    

    def get_by_id(self, produk_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM produk WHERE id = ?",
            (produk_id,)
        )
        row = cur.fetchone()
        conn.close()
        return map_produk(row)


class KeranjangRepositoryImpl(KeranjangRepository):

    def add_item(self, produk_id: int, jumlah: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO keranjang (produk_id, jumlah) VALUES (?, ?)",
            (produk_id, jumlah)
        )
        conn.commit()
        conn.close()

    def get_items(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                k.id,
                p.id,
                p.nama,
                p.harga,
                k.jumlah
            FROM keranjang k
            JOIN produk p ON k.produk_id = p.id
        """)
        rows = cur.fetchall()
        conn.close()
        return [map_keranjang(r) for r in rows]

    def delete_item(self, item_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM keranjang WHERE id = ?",
            (item_id,)
        )
        conn.commit()
        conn.close()

    def clear(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM keranjang")
        conn.commit()
        conn.close()
