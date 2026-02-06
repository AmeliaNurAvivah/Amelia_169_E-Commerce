import sqlite3
from ecommerce.domain.entities.entities import Pesanan, PesananItem
from ecommerce.domain.repositories.repositories import PesananRepository
from ecommerce.infrastructure.sqlite_db.db_settings import DB_PATH


class SQLitePesananRepository(PesananRepository):

    def simpan_pesanan(self, pesanan, items):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO pesanan (tanggal, total, metode_pembayaran, status)
            VALUES (?, ?, ?, ?)
        """, (pesanan.tanggal, pesanan.total, pesanan.metode_pembayaran, pesanan.status))

        pesanan_id = cur.lastrowid

        for i in items:
            cur.execute("""
                INSERT INTO pesanan_item 
                (pesanan_id, produk_id, nama_produk, harga, jumlah, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pesanan_id,
                i.produk_id,
                i.nama_produk,
                i.harga,
                i.jumlah,
                i.subtotal
            ))

        conn.commit()
        conn.close()

    def list_pesanan(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        rows = cur.execute("SELECT * FROM pesanan ORDER BY id DESC").fetchall()
        conn.close()

        return [
            Pesanan(id=r[0], tanggal=r[1], total=r[2], metode_pembayaran=r[3], status=r[4])
            for r in rows
        ]

    def detail_pesanan(self, pesanan_id):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        rows = cur.execute(
            "SELECT * FROM pesanan_item WHERE pesanan_id=?",
            (pesanan_id,)
        ).fetchall()

        conn.close()

        return [
            PesananItem(
                id=r[0], pesanan_id=r[1], produk_id=r[2],
                nama_produk=r[3], harga=r[4], jumlah=r[5], subtotal=r[6]
            )
            for r in rows
        ]

    def ubah_status(self, pesanan_id, status):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("UPDATE pesanan SET status=? WHERE id=?", (status, pesanan_id))
        conn.commit()
        conn.close()

    def hapus_pesanan(self, pesanan_id):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("DELETE FROM pesanan_item WHERE pesanan_id=?", (pesanan_id,))
        cur.execute("DELETE FROM pesanan WHERE id=?", (pesanan_id,))

        conn.commit()
        conn.close()
