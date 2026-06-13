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

        
        
# Función para eliminar una mascota y sus servicios asociados
def eliminar_mascota():
    try:
        id_m = int(input("ID de mascota a eliminar: "))
    except ValueError:
        print("ID invalido")
        return

    cursor.execute("SELECT * FROM mascotas WHERE id=?", (id_m,))

    if cursor.fetchone() is None:
        print("No existe esa mascota")
        return

    confirmar = input("¿Eliminar mascota? (s/n): ").lower()

    if confirmar != "s":
        print("Operacion cancelada")
        return

    cursor.execute("DELETE FROM mascotas WHERE id=?", (id_m,))

    conn.commit()
    print("Mascota eliminada")

# Función para registrar un servicio realizado a una mascota
def registrar_servicio():
    try:
        mascota_id = int(input("ID de mascota: "))
    except ValueError:
        print("ID invalido")
        return

    cursor.execute("SELECT * FROM mascotas WHERE id=?", (mascota_id,))

    if cursor.fetchone() is None:
        print("La mascota no existe")
        return

    servicio = input("Servicio: ").strip()

    if len(servicio) < 4:
        print("Servicio invalido")
        return

    fecha = input("Fecha (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        print("Fecha invalida")
        return

    cursor.execute("""
        INSERT INTO servicios
        (mascota_id, servicio, fecha)
        VALUES (?, ?, ?)
    """, (mascota_id, servicio, fecha))

    conn.commit()
    print("Servicio registrado")

# Función para mostrar el historial completo de servicios
def ver_historial():
    cursor.execute("""
        SELECT mascotas.nombre,
               servicios.servicio,
               servicios.fecha
        FROM servicios
        JOIN mascotas
        ON mascotas.id = servicios.mascota_id
        ORDER BY servicios.fecha DESC
    """)

    datos = cursor.fetchall()

    if not datos:
        print("No hay servicios registrados")
        return

    print("\nHISTORIAL\n")

    for d in datos:
        print(f"Mascota: {d[0]}")
        print(f"Servicio: {d[1]}")
        print(f"Fecha: {d[2]}")
        print("----------------")
        