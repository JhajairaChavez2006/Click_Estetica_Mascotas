# Importación de las librerías necesarias
import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("spa_click.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Creación de la tabla de mascotas
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
# Creación de la tabla de servicios
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

# Función para registrar los datos de una nueva mascota y almacenarlos en la base de datos
def registrar_mascota():
    while True:
        nombre = input("Nombre: ").strip()
        if len(nombre) < 2:
            print("Nombre invalido")
            continue
        break

    while True:
        especie = input("Especie: ").strip()
        if len(especie) < 2:
            print("Especie invalida")
            continue
        break

    while True:
        raza = input("Raza: ").strip()
        if len(raza) < 2:
            print("Raza invalida")
            continue
        break

    while True:
        try:
            edad = int(input("Edad: "))
            if edad < 0:
                print("La edad no puede ser negativa")
                continue
            if edad > 30:
                print("Edad poco realista")
                continue
            break
        except ValueError:
            print("Ingrese un numero entero")

    while True:
        propietario = input("Propietario: ").strip()
        if len(propietario) < 3:
            print("Propietario invalido")
            continue
        break

    cursor.execute("""
        INSERT INTO mascotas
        (nombre, especie, raza, edad, propietario)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, especie, raza, edad, propietario))

    conn.commit()
    print("Mascota registrada correctamente")

# Función para mostrar las mascotas registradas ordenadas por ID o nombre
def ver_mascotas(order="id"):
    if order == "id":
        cursor.execute("SELECT * FROM mascotas ORDER BY id ASC")
    else:
        cursor.execute("SELECT * FROM mascotas ORDER BY nombre ASC")

    mascotas = cursor.fetchall()

    if not mascotas:
        print("No hay mascotas registradas")
        return

    print("\nLISTA DE MASCOTAS\n")

    for m in mascotas:
        print(f"ID: {m[0]}")
        print(f"Nombre: {m[1]}")
        print(f"Especie: {m[2]}")
        print(f"Raza: {m[3]}")
        print(f"Edad: {m[4]}")
        print(f"Propietario: {m[5]}")
        print("----------------------")
        