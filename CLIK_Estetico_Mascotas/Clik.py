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