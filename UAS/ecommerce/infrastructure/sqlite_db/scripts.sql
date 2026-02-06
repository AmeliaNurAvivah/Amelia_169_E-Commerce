CREATE TABLE IF NOT EXISTS pesanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT NOT NULL,
    total REAL NOT NULL,
    metode_pembayaran TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pesanan_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pesanan_id INTEGER NOT NULL,
    produk_id INTEGER NOT NULL,
    nama_produk TEXT NOT NULL,
    harga REAL NOT NULL,
    jumlah INTEGER NOT NULL,
    subtotal REAL NOT NULL,

    FOREIGN KEY (pesanan_id) REFERENCES pesanan(id)
);


