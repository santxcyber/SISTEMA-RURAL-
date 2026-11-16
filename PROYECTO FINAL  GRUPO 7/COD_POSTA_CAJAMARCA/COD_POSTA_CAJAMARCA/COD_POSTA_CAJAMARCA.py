import os


def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")



class Persona:

  def __init__(self, nombre, dni):
    self.__nombre = nombre
    self.__dni = dni


  def get_dni(self):
    return self.__dni

  def get_dni_oculto(self):
    return "****" + self.__dni[4:]

  def get_nombre(self):
    return self.__nombre


class Doctor(Persona):

  def __init__(self, nombre, dni, especialidad):
    super().__init__(nombre, dni)
    self.especialidad = especialidad


class Paciente(Persona):

  def __init__(self, nombre, dni, codigo):
    super().__init__(nombre, dni)
    self.codigo = codigo
    self.triaje = None
    self.programa_atencion = None


class Triaje:

  def __init__(
      self,
      sistolica,
      diastolica,
      fc,
      fr,
      temperatura,
      saturacion,
      peso,
      talla,
  ):
    self.presion_sistolica = sistolica
    self.presion_diastolica = diastolica
    self.frecuencia_cardiaca = fc
    self.frecuencia_respiratoria = fr
    self.temperatura = temperatura
    self.saturacion_oxigeno = saturacion
    self.peso_kg = peso
    self.talla_m = talla / 100 if talla > 3 else talla

  def calcular_imc(self):
    if self.talla_m <= 0:
      raise ValueError("La talla debe ser mayor a 0.")
    return self.peso_kg / (self.talla_m**2)

  def mostrar_datos(self):
    imc = self.calcular_imc()
    return (
        f"  • Presión Arterial: {self.presion_sistolica}/{self.presion_diastolica} mmHg\n"
        f"  • Frecuencia Cardíaca: {self.frecuencia_cardiaca} lpm\n"
        f"  • Frecuencia Respiratoria: {self.frecuencia_respiratoria} rpm\n"
        f"  • Temperatura: {self.temperatura} °C\n"
        f"  • Saturación de Oxígeno: {self.saturacion_oxigeno} %\n"
        f"  • Peso: {self.peso_kg} kg | Talla: {self.talla_m:.2f} m\n"
        f"  • IMC: {imc:.2f} kg/m²"
    )


class CitaMedica:

  def __init__(self, id_cita, fecha, turno, paciente, doctor):
    self.id_cita = id_cita
    self.fecha = fecha
    self.turno = turno  # "Mañana" o "Tarde"
    self.paciente = paciente
    self.doctor = doctor



pacientes = []
citas = []
doctor_turno = Doctor("Dr. Carlos Mendoza", "12345678", "Medicina General")


def validar_entrada(dato):
  dato = dato.strip().upper()
  if not dato:
    raise ValueError("El campo no puede estar vacío.")

  if dato.startswith("HP-") and dato[3:].isdigit():
    return "CODIGO", dato

  if not dato.isdigit() or len(dato) != 8:
    raise ValueError(
        "Debe ingresar un DNI de 8 números o un código válido (ej. HP-001)."
    )

  return "DNI", dato


def buscar_paciente(dato_validado):
  # Usamos filter y lambda 
  resultado = list(
      filter(
          lambda p: p.get_dni() == dato_validado
          or p.codigo.upper() == dato_validado,
          pacientes,
      )
  )
  return resultado[0] if resultado else None



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
  print("6. Mostrar registros y reporte estadístico HIS")
  print("7. Salir y guardar respaldo")
  print("-----------------------------------------")
  opcion = input("Elige una opción: ")

  limpiar_pantalla()

  if opcion == "1":
    print("--- REGISTRAR PACIENTE ---")
    try:
      nombre = input("Nombre: ").strip()
      if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

      tipo_dni, dni = validar_entrada(input("DNI (8 dígitos): "))
      if tipo_dni != "DNI":
        raise ValueError("Debe ingresar un DNI de 8 dígitos.")

      tipo_cod, codigo = validar_entrada(
          input("Código Historia Posta (ej. HP-001): ")
      )
      if tipo_cod != "CODIGO":
        raise ValueError("El código debe tener el formato HP-001.")

      if buscar_paciente(dni) is None and buscar_paciente(codigo) is None:
        nuevo = Paciente(nombre, dni, codigo)
        pacientes.append(nuevo)
        print("\nPaciente registrado con éxito:")
        print(
            f"Código: {nuevo.codigo} | Paciente: {nuevo.get_nombre()} | DNI:"
            f" {nuevo.get_dni_oculto()}"
        )
      else:
        print("Ese DNI o Código ya existe.")
    except ValueError as e:
      print(f"Error: {e}")

  elif opcion == "2":
    print("--- BUSCAR PACIENTE ---")
    try:
      _, dato = validar_entrada(input("DNI o Código Historia Posta a buscar: "))
      p = buscar_paciente(dato)

      if p is not None:
        print(
            f"\nEncontrado: {p.get_nombre()} | Código: {p.codigo} | DNI:"
            f" {p.get_dni_oculto()}"
        )
        if p.triaje is not None:
          print("--- Datos de Triaje ---")
          print(p.triaje.mostrar_datos())
        else:
          print("Aún no tiene triaje registrado.")
      else:
        print("Paciente no encontrado.")
    except ValueError as e:
      print(f"Error: {e}")

  elif opcion == "3":
    print("--- INGRESAR TRIAJE ---")
    try:
      tipo, dato = validar_entrada(
          input("DNI o Código Historia Posta para triaje: ")
      )
      p = buscar_paciente(dato)

      if p is None:
        if tipo == "DNI":
          codigo_nuevo = f"HP-{len(pacientes) + 1:03d}"
          p = Paciente("Paciente Preliminar", dato, codigo_nuevo)
          pacientes.append(p)
          print(
              "Paciente nuevo. Se creó Historia Posta preliminar única:"
              f" {p.codigo}"
          )
        else:
          print(
              "Código no encontrado. Ingrese su DNI para crear una historia"
              " nueva."
          )
          input("\nPresiona Enter para volver al menú...")
          continue
      else:
        print(f"Historial recuperado: {p.get_nombre()} | Código: {p.codigo}")

      sis = int(input("Presión sistólica (mmHg): "))
      dia = int(input("Presión diastólica (mmHg): "))
      fc = int(input("Frecuencia cardíaca (lpm): "))
      fr = int(input("Frecuencia respiratoria (rpm): "))
      temp = float(input("Temperatura (°C): "))
      sat = int(input("Saturación de oxígeno (%): "))
      peso = float(input("Peso (kg): "))
      talla = float(input("Talla (m o cm): "))

      # Validaciones simples de rangos fisiológicos (RF-02)
      if temp < 34.0 or temp > 42.5:
        raise ValueError("La temperatura debe estar entre 34.0 y 42.5 °C.")
      if sat < 50 or sat > 100:
        raise ValueError("La saturación debe estar entre 50% y 100%.")
      if peso <= 0 or peso >= 500:
        raise ValueError("El peso debe estar entre 1 y 500 kg.")
      if talla <= 0 or (talla > 3 and talla < 30) or talla >= 250:
        raise ValueError("La talla ingresada es inválida.")

      print("\nPrograma de atención:")
      print("1. Medicina General | 2. Vacunas | 3. Obstetricia")
      prog = input("Elige programa (1-3): ")
      if prog == "2":
        p.programa_atencion = "Vacunas"
      elif prog == "3":
        p.programa_atencion = "Obstetricia"
      else:
        p.programa_atencion = "Medicina General"

      p.triaje = Triaje(sis, dia, fc, fr, temp, sat, peso, talla)
      print("\nTriaje guardado correctamente:")
      print(p.triaje.mostrar_datos())

    except ValueError as e:
      print(f"Error de validación: {e}")

  elif opcion == "4":
    print("--- PROGRAMAR CITA MÉDICA ---")
    try:
      _, dato = validar_entrada(input("DNI o Código HP del paciente: "))
      p = buscar_paciente(dato)
      if p is None:
        print("Paciente no encontrado. Regístrelo primero en la opción 1.")
      else:
        fecha = input("Fecha de la cita (ej. 18/11/2026): ").strip()
        turno_op = input("Turno (1. Mañana | 2. Tarde): ").strip()
        turno = "Tarde" if turno_op == "2" else "Mañana"

        id_cita = f"CITA-{len(citas) + 1:03d}"
        nueva_cita = CitaMedica(id_cita, fecha, turno, p, doctor_turno)
        citas.append(nueva_cita)
        print(
            f"\nCita {id_cita} programada para {p.get_nombre()} en el turno"
            f" {turno}."
        )
    except ValueError as e:
      print(f"Error: {e}")

  elif opcion == "5":
    print("--- AGENDA DIARIA POR TURNO ---")
    turno_op = input("Ver turno (1. Mañana | 2. Tarde): ").strip()
    turno_buscado = "Tarde" if turno_op == "2" else "Mañana"

    # Usamos de filter + lambda :)
    citas_turno = list(filter(lambda c: c.turno == turno_buscado, citas))

    if not citas_turno:
      print(f"No hay citas registradas en el turno {turno_buscado}.")
    else:
      for c in citas_turno:
        print(
            f"[{c.id_cita}] Fecha: {c.fecha} | Paciente:"
            f" {c.paciente.get_nombre()} ({c.paciente.codigo}) | Doctor:"
            f" {c.doctor.get_nombre()}"
        )

  elif opcion == "6":
    print("--- REGISTROS Y CONSOLIDADO HIS (DIRESA) ---")
    if not pacientes:
      print("Aún no hay pacientes registrados.")
    else:
      med_general = 0
      vacunas = 0
      obstetricia = 0

      for i, p in enumerate(pacientes, start=1):
        print(
            f"\n{i}. {p.get_nombre()} | DNI: {p.get_dni_oculto()} | Código:"
            f" {p.codigo}"
        )
        if p.triaje is not None:
          print(p.triaje.mostrar_datos())
          print(f"  • Programa: {p.programa_atencion}")
          if p.programa_atencion == "Vacunas":
            vacunas += 1
          elif p.programa_atencion == "Obstetricia":
            obstetricia += 1
          else:
            med_general += 1
        else:
          print("  • Triaje: Pendiente")
        print("-" * 35)

      print("\n=== RESUMEN ESTADÍSTICO HIS (DIRESA CAJAMARCA) ===")
      print(f"• Medicina General: {med_general} atenciones")
      print(f"• Vacunas: {vacunas} atenciones")
      print(f"• Obstetricia: {obstetricia} atenciones")

  elif opcion == "7":
    #////////
    with open("respaldo_posta.txt", "w", encoding="utf-8") as archivo:
      archivo.write("RESPALDO PUESTO DE SALUD PORCÓN BAJO\n")
      for p in pacientes:
        archivo.write(
            f"{p.codigo} | {p.get_nombre()} | DNI: {p.get_dni_oculto()}\n"
        )
    print("Respaldo guardado en 'respaldo_posta.txt'. Saliendo...")
    break
  else:
    print("Opción incorrecta.")

  input("\nPresiona Enter para continuar...")