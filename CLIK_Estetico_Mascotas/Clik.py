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