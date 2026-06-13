import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("spa_click.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    raza TEXT NOT NULL,
    edad INTEGER NOT NULL,
    propietario TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INTEGER NOT NULL,
    servicio TEXT NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (mascota_id)
        REFERENCES mascotas(id)
        ON DELETE CASCADE
)
""")

conn.commit()