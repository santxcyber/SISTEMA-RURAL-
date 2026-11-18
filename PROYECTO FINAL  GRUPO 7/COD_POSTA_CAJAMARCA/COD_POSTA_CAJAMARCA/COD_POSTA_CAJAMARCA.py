import os


def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")


# Clases simples sin atributos privados ni herencia raras
class Paciente:

  def __init__(self, nombre, dni, codigo):
    self.nombre = nombre
    self.dni = dni
    self.codigo = codigo
    self.triaje = None
    self.programa = "Medicina General"


class Cita:

  def __init__(self, id_cita, fecha, turno, paciente):
    self.id_cita = id_cita
    self.fecha = fecha
    self.turno = turno  # "Mañana" o "Tarde"
    self.paciente = paciente


# Listas globales para guardar la info mientras corre el programa
pacientes = []
citas = []


# Función simple para buscar paciente usando un ciclo for normal
def buscar_paciente(dato):
  for p in pacientes:
    if p.dni == dato or p.codigo.upper() == dato.upper():
      return p
  return None


# Menú Principal
while True:
  limpiar_pantalla()
  print("-----------------------------------------")
  print("  SISTEMARURAL-PE | P.S. PORCÓN BAJO")
  print("-----------------------------------------")
  print("1. Registrar paciente")
  print("2. Buscar paciente")
  print("3. Ingresar triaje")
  print("4. Programar cita médica")
  print("5. Ver agenda diaria (Mañana / Tarde)")
  print("6. Mostrar registros y reporte estadístico")
  print("7. Salir y guardar respaldo")
  print("-----------------------------------------")
  opcion = input("Elige una opción: ")

  limpiar_pantalla()

  if opcion == "1":
    print("--- REGISTRAR PACIENTE ---")
    nombre = input("Nombre: ").strip()
    dni = input("DNI (8 dígitos): ").strip()
    codigo = input("Código Historia Posta (ej. HP-001): ").strip()

    # Validaciones básicas con if
    if not nombre or not dni or not codigo:
      print("Error: Ningún campo puede estar vacío.")
    elif len(dni) != 8 or not dni.isdigit():
      print("Error: El DNI debe tener exactamente 8 números.")
    elif buscar_paciente(dni) is not None or buscar_paciente(codigo) is not None:
      print("Error: Ese DNI o Código ya existe.")
    else:
      nuevo_paciente = Paciente(nombre, dni, codigo)
      pacientes.append(nuevo_paciente)
      print("\n¡Paciente registrado con éxito!")
      # Ocultar DNI de forma sencilla mostrando solo los últimos 4
      dni_oculto = "****" + dni[4:]
      print(
          f"Código: {codigo} | Nombre: {nombre} | DNI oculto: {dni_oculto}"
      )

  elif opcion == "2":
    print("--- BUSCAR PACIENTE ---")
    dato = input("Ingrese DNI o Código a buscar: ").strip()
    p = buscar_paciente(dato)

    if p is not None:
      dni_oculto = "****" + p.dni[4:]
      print(f"\n¡Encontrado!")
      print(f"Nombre: {p.nombre}")
      print(f"Código: {p.codigo}")
      print(f"DNI: {dni_oculto}")

      if p.triaje is not None:
        print("\n--- Datos de Triaje ---")
        print(f"• Presión: {p.triaje['presion']}")
        print(f"• Temperatura: {p.triaje['temp']} °C")
        print(f"• Peso: {p.triaje['peso']} kg | Talla: {p.triaje['talla']} m")
        print(f"• IMC: {p.triaje['imc']}")
        print(f"• Programa: {p.programa}")
      else:
        print("\nAún no tiene triaje registrado.")
    else:
      print("Paciente no encontrado.")

  elif opcion == "3":
    print("--- INGRESAR TRIAJE ---")
    dato = input("DNI o Código del paciente para triaje: ").strip()
    p = buscar_paciente(dato)

    if p is None:
      print(
          "Paciente no encontrado. Debe registrarlo primero en la opción 1 o"
          " ingresar un DNI válido."
      )
    else:
      print(f"Paciente encontrado: {p.nombre}")
      try:
        sistolica = int(input("Presión sistólica: "))
        diastolica = int(input("Presión diastólica: "))
        temp = float(input("Temperatura (°C): "))
        peso = float(input("Peso (kg): "))
        talla = float(input("Talla (en metros, ej. 1.70): "))

        # Calcular IMC básico
        imc = peso / (talla * talla)

        print("\nPrograma de atención:")
        print("1. Medicina General")
        print("2. Vacunas")
        print("3. Obstetricia")
        prog_op = input("Elige programa (1-3): ").strip()

        if prog_op == "2":
          p.programa = "Vacunas"
        elif prog_op == "3":
          p.programa = "Obstetricia"
        else:
          p.programa = "Medicina General"

        # Guardar triaje como un diccionario simple
        p.triaje = {
            "presion": f"{sistolica}/{diastolica}",
            "temp": temp,
            "peso": peso,
            "talla": talla,
            "imc": round(imc, 2),
        }

        print("\n¡Triaje guardado correctamente!")
        print(f"IMC calculado: {round(imc, 2)} | Programa: {p.programa}")

      except ValueError:
        print("Error: Por favor ingresa números válidos en los campos.")

  elif opcion == "4":
    print("--- PROGRAMAR CITA MÉDICA ---")
    dato = input("DNI o Código del paciente: ").strip()
    p = buscar_paciente(dato)

    if p is None:
      print("Paciente no encontrado. Regístrelo primero.")
    else:
      fecha = input("Fecha de la cita (ej. 18/11/2026): ").strip()
      turno_op = input("Turno (1. Mañana | 2. Tarde): ").strip()
      turno = "Tarde" if turno_op == "2" else "Mañana"

      id_cita = f"CITA-00{len(citas) + 1}"
      nueva_cita = Cita(id_cita, fecha, turno, p)
      citas.append(nueva_cita)
      print(
          f"\nCita {id_cita} programada para {p.nombre} en el turno {turno} el"
          f" día {fecha}."
      )

  elif opcion == "5":
    print("--- AGENDA DIARIA POR TURNO ---")
    turno_op = input("Ver turno (1. Mañana | 2. Tarde): ").strip()
    turno_buscado = "Tarde" if turno_op == "2" else "Mañana"

    # Ciclo for normal para filtrar citas
    contador = 0
    for c in citas:
      if c.turno == turno_buscado:
        contador += 1
        print(
            f"[{c.id_cita}] Fecha: {c.fecha} | Paciente: {c.paciente.nombre}"
            f" ({c.paciente.codigo})"
        )

    if contador == 0:
      print(f"No hay citas registradas en el turno {turno_buscado}.")

  elif opcion == "6":
    print("--- REGISTROS Y REPORTE ESTADÍSTICO ---")
    if not pacientes:
      print("Aún no hay pacientes registrados.")
    else:
      med_general = 0
      vacunas = 0
      obstetricia = 0

      for i, p in enumerate(pacientes, start=1):
        dni_oculto = "****" + p.dni[4:]
        print(f"\n{i}. Nombre: {p.nombre} | DNI: {dni_oculto}")
        if p.triaje is not None:
          print(f"   • Programa: {p.programa} | IMC: {p.triaje['imc']}")
          if p.programa == "Vacunas":
            vacunas += 1
          elif p.programa == "Obstetricia":
            obstetricia += 1
          else:
            med_general += 1
        else:
          print("   • Triaje: Pendiente")
        print("-" * 30)

      print("\n=== RESUMEN ESTADÍSTICO ===")
      print(f"• Medicina General: {med_general}")
      print(f"• Vacunas: {vacunas}")
      print(f"• Obstetricia: {obstetricia}")

  elif opcion == "7":
    # Guardar respaldo básico en archivo de texto plano
    archivo = open("respaldo_posta.txt", "w", encoding="utf-8")
    archivo.write("RESPALDO PUESTO DE SALUD\n")
    for p in pacientes:
      dni_oculto = "****" + p.dni[4:]
      archivo.write(f"{p.codigo} - {p.nombre} - DNI: {dni_oculto}\n")
    archivo.close()
    print("Respaldo guardado en 'respaldo_posta.txt'. ¡Hasta luego!")
    break
  else:
    print("Opción incorrecta. Intente de nuevo.")

  input("\nPresiona Enter para continuar...")