import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "katalog.db")


print("DB FINAL:", os.path.abspath(DB_NAME))

def get_connection():
    return sqlite3.connect(DB_NAME)
