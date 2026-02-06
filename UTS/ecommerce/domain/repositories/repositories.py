from ecommerce.infrastructure.sqlite_db.db_settings import get_connection
import os
from werkzeug.utils import secure_filename
from ecommerce.domain.entities.entities import (
    Kategori, Lokasi, Produk, Keranjang
)

# =====================
# KATEGORI REPOSITORY
# =====================
class KategoriRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM kategori ORDER BY nama").fetchall()
        conn.close()
        return [Kategori(id=r["id"], nama=r["nama"]) for r in rows]

    def get_or_create(self, nama):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM kategori WHERE nama=?",
            (nama,)
        ).fetchone()

        if row:
            conn.close()
            return row["id"]

        cur = conn.execute(
            "INSERT INTO kategori (nama) VALUES (?)",
            (nama,)
        )
        conn.commit()
        conn.close()
        return cur.lastrowid



# =====================
# PRODUK REPOSITORY
# =====================
class ProdukRepository:
    def get_filtered(self, kategori_id, lokasi_id, min_harga, max_harga, q):
        conn = get_connection()
        query = """
            SELECT p.*, k.nama AS kategori_nama, l.nama AS lokasi_nama
            FROM produk p
            JOIN kategori k ON p.kategori_id = k.id
            JOIN lokasi l ON p.lokasi_id = l.id
            WHERE 1=1
        """
        params = []

        if kategori_id:
            query += " AND p.kategori_id = ?"
            params.append(kategori_id)

        if lokasi_id:
            query += " AND p.lokasi_id = ?"
            params.append(lokasi_id)

        if min_harga:
            query += " AND p.harga >= ?"
            params.append(min_harga)

        if max_harga:
            query += " AND p.harga <= ?"
            params.append(max_harga)

        if q:
            query += " AND p.nama LIKE ?"
            params.append(f"%{q}%")

        rows = conn.execute(query, params
        ).fetchall()
        conn.close()

        return [
            Produk(
                id=r["id"],
                nama=r["nama"],
                kategori_id=r["kategori_id"],
                kategori_nama=r["kategori_nama"],
                lokasi_id=r["lokasi_id"],
                lokasi_nama=r["lokasi_nama"],
                harga=r["harga"],
                keterangan=r["keterangan"],
                gambar=r["gambar"]
            )
            for r in rows
        ]

    def add(self, nama, kategori_id, lokasi_id, harga, keterangan, gambar):
        conn = get_connection()
        conn.execute("""
            INSERT INTO produk (nama, kategori_id, lokasi_id, harga, keterangan, gambar)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nama, kategori_id, lokasi_id, harga, keterangan, gambar))
        conn.commit()

  # 🔥 UPDATE PRODUK
    def update(self, produk_id, data, file):
        conn = get_connection()

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join("flask_app/static/uploads", filename)
            file.save(filepath)

            conn.execute("""
                UPDATE produk SET
                nama=?, harga=?, keterangan=?, gambar=?
                WHERE id=?
            """, (
                data["nama"],
                data["harga"],
                data["keterangan"],
                f"uploads/{filename}",
                produk_id
            ))
        else:
            conn.execute("""
                UPDATE produk SET
                nama=?, harga=?, keterangan=?
                WHERE id=?
            """, (
                data["nama"],
                data["harga"],
                data["keterangan"],
                produk_id
            ))

        conn.commit()
        conn.close()

    # 🔥 DELETE PRODUK
    def delete(self, produk_id):
        conn = get_connection()
        conn.execute("DELETE FROM produk WHERE id=?", (produk_id,))
        conn.commit()
        conn.close()


# =====================
# KERANJANG REPOSITORY
# =====================
class KeranjangRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT k.id, p.id AS produk_id, p.nama, p.harga, k.jumlah
            FROM keranjang k
            JOIN produk p ON k.produk_id = p.id
        """).fetchall()
        conn.close()

        result = []
        for r in rows:
            subtotal = r["harga"] * r["jumlah"]
            result.append(
                Keranjang(
                    id=r["id"],
                    produk_id=r["produk_id"],
                    nama_produk=r["nama"],
                    harga=r["harga"],
                    jumlah=r["jumlah"],
                    subtotal=subtotal
                )
            )
        return result

    def get_by_produk(self, produk_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM keranjang WHERE produk_id=?",
            (produk_id,)
        ).fetchone()
        conn.close()
        return row

    def add(self, produk_id, jumlah):
        conn = get_connection()
        conn.execute(
            "INSERT INTO keranjang (produk_id, jumlah) VALUES (?, ?)",
            (produk_id, jumlah)
        )
        conn.commit()
        conn.close()

    def update_jumlah(self, id, jumlah):
        conn = get_connection()
        conn.execute(
            "UPDATE keranjang SET jumlah=? WHERE id=?",
            (jumlah, id)
        )
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = get_connection()
        conn.execute("DELETE FROM keranjang WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def delete_all(self):
        conn = get_connection()
        conn.execute("DELETE FROM keranjang")
        conn.commit()
        conn.close()


# =====================
# LOKASI REPOSITORY
# =====================
class LokasiRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM lokasi ORDER BY nama").fetchall()
        conn.close()
        return [Lokasi(id=r["id"], nama=r["nama"]) for r in rows]

    def get_or_create(self, nama):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM lokasi WHERE nama=?",
            (nama,)
        ).fetchone()

        if row:
            conn.close()
            return row["id"]

        cur = conn.execute(
            "INSERT INTO lokasi (nama) VALUES (?)",
            (nama,)
        )
        conn.commit()
        conn.close()
        return cur.lastrowid