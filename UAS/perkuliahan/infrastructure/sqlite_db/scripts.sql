
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT,
    password TEXT,
    status TEXT
);

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

