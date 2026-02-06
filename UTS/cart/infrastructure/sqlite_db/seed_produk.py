import sqlite3

conn = sqlite3.connect("sqlite_db/katalog.db")
cur = conn.cursor()

produk = [
    ("Lipstik Matte", 75000),
    ("Foundation Liquid", 120000),
    ("Maskara Waterproof", 65000),
    ("Eyeliner Pen", 45000),
    ("Blush On Peach", 55000),
]

cur.executemany(
    "INSERT INTO produk (nama, harga) VALUES (?, ?)",
    produk
)

conn.commit()
conn.close()

print("Produk berhasil ditambahkan.")
