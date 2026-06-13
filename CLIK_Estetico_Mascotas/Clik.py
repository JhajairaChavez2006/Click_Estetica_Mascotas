#Mostrar historial de una sola mascota
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