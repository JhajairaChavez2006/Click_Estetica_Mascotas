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
        
# Buscar una mascota por su nombre
def buscar_mascota():
    nombre = input("Nombre a buscar: ").strip()

    if not nombre:
        print("Debe ingresar un nombre")
        return

    cursor.execute("""
        SELECT * FROM mascotas
        WHERE nombre LIKE ?
    """, (f"%{nombre}%",))

    resultados = cursor.fetchall()

    if not resultados:
        print("No se encontraron mascotas")
        return

    for r in resultados:
        print(f"""
ID: {r[0]}
Nombre: {r[1]}
Especie: {r[2]}
Raza: {r[3]}
Edad: {r[4]}
Propietario: {r[5]}
""")

# Modificar los datos de una mascota existente
def modificar_mascota():
    try:
        id_m = int(input("ID de mascota: "))
    except ValueError:
        print("ID invalido")
        return

    cursor.execute("SELECT * FROM mascotas WHERE id=?", (id_m,))

    if cursor.fetchone() is None:
        print("No existe esa mascota")
        return

    nombre = input("Nuevo nombre: ").strip()
    especie = input("Nueva especie: ").strip()
    raza = input("Nueva raza: ").strip()
    propietario = input("Nuevo propietario: ").strip()

    try:
        edad = int(input("Nueva edad: "))
        if edad < 0 or edad > 30:
            print("Edad invalida")
            return
    except ValueError:
        print("Edad invalida")
        return

    cursor.execute("""
        UPDATE mascotas
        SET nombre=?, especie=?, raza=?, edad=?, propietario=?
        WHERE id=?
    """, (nombre, especie, raza, edad, propietario, id_m))

    conn.commit()
    print("Mascota actualizada")     
        
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
        
#Función para mostrar el historial de una sola mascota
def ver_historial_mascota():

    try:
        id_m = int(input("ID de mascota: "))
    except ValueError:
        print("ID inválido")
        return

    cursor.execute("""
        SELECT mascotas.nombre,
               servicios.servicio,
               servicios.fecha
        FROM servicios
        JOIN mascotas
        ON mascotas.id = servicios.mascota_id
        WHERE mascotas.id = ?
        ORDER BY servicios.fecha DESC
    """, (id_m,))

    datos = cursor.fetchall()

    if not datos:
        print("No hay historial para esta mascota o no existe")
        return

    print("\nHISTORIAL DE MASCOTA\n")

    print(f"Mascota: {datos[0][0]}\n")

    for d in datos:
        print(f"Servicio: {d[1]}")
        print(f"Fecha: {d[2]}")
        print("----------------")

#Extraer datos del csv
def exportar_csv():
    cursor.execute("SELECT * FROM mascotas")
    mascotas = cursor.fetchall()

    with open("mascotas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nombre", "especie", "raza", "edad", "propietario"])
        writer.writerows(mascotas)

    cursor.execute("SELECT * FROM servicios")
    servicios = cursor.fetchall()

    with open("servicios.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "mascota_id", "servicio", "fecha"])
        writer.writerows(servicios)

    print("Exportacion completada")


#Menú 
while True:
    print("""
=============================
        SPA CLIK
=============================
1. Registrar mascota
2. Ver mascotas (ID)
3. Ver mascotas (A-Z)
4. Buscar mascota
5. Modificar mascota
6. Eliminar mascota
7. Registrar servicio
8. Ver historial general
9. Ver historial de una mascota
10. Exportar CSV
11. Salir
""")

    op = input("Opcion: ").strip()

    if op == "1":
        registrar_mascota()
    elif op == "2":
        ver_mascotas("id")
    elif op == "3":
        ver_mascotas("nombre")
    elif op == "4":
        buscar_mascota()
    elif op == "5":
        modificar_mascota()
    elif op == "6":
        eliminar_mascota()
    elif op == "7":
        registrar_servicio()
    elif op == "8":
        ver_historial()
    elif op == "9":
         ver_historial_mascota()
    elif op == "10":
        exportar_csv()
    elif op == "11":
        print("Saliendo...")
        break
    else:
        print("Opcion invalida")

conn.close()
