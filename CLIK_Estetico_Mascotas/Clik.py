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