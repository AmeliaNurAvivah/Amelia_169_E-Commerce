import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "kampus.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS dosen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    ndn TEXT
);

CREATE TABLE IF NOT EXISTS matakuliah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    dosen_id INTEGER,
    FOREIGN KEY(dosen_id) REFERENCES dosen(id)
);

CREATE TABLE IF NOT EXISTS kelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    matakuliah_id INTEGER,
    dosen_id INTEGER,
    FOREIGN KEY(matakuliah_id) REFERENCES matakuliah(id),
    FOREIGN KEY(dosen_id) REFERENCES dosen(id)
);
""")

conn.commit()
conn.close()

print("Database & tabel berhasil dibuat.")
