class Paciente:

  def __init__(self, nombre, dni, codigo):
    self.nombre = nombre
    self.dni = dni
    self.codigo = codigo
    self.triaje = None


pacientes = []


def buscar_paciente(dato):
  for p in pacientes:
    if p.dni == dato or p.codigo.upper() == dato.upper():
      return p
  return None


while True:
  print("-----------------------------------------")
  print("  SISTEMARURAL-PE | P.S. PORCÓN BAJO")
  print("-----------------------------------------")
  print("1. Registrar paciente")
  print("2. Buscar paciente (DNI o Código)")
  print("3. Ingresar triaje")
  print("4. Ver pacientes registrados")
  print("5. Salir")
  print("-----------------------------------------")
  opcion = input("Elige una opción: ")


  if opcion == "1":
    print("--- REGISTRAR PACIENTE ---")
    nombre = input("Nombre: ").strip()
    if not nombre:
      print("Error: El nombre no puede estar vacío.")
    else:
      dni = input("DNI (8 dígitos): ").strip()
      if len(dni) != 8 or not dni.isdigit():
        print("Error: El DNI debe tener exactamente 8 números.")
      else:
        codigo = input("Código Historia Posta (ej. HP-001): ").strip()
        if not codigo:
          print("Error: El código no puede estar vacío.")
        elif (
            buscar_paciente(dni) is not None
            or buscar_paciente(codigo) is not None
        ):
          print("Error: Ese DNI o Código ya existe en el sistema.")
        else:
          nuevo_paciente = Paciente(nombre, dni, codigo)
          pacientes.append(nuevo_paciente)
          print("\n¡Paciente registrado con éxito!")
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
        print(f" Presión Arterial: {p.triaje['presion']} mmHg")
        print(f" Frecuencia Cardíaca: {p.triaje['fc']} lpm")
        print(f" Frecuencia Respiratoria: {p.triaje['fr']} rpm")
        print(f" Temperatura: {p.triaje['temp']} °C")
        print(f" Peso: {p.triaje['peso']} kg | Talla: {p.triaje['talla']} m")
        print(f" IMC: {p.triaje['imc']}")
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
          "Paciente no encontrado. Debe registrarlo primero en la opción 1."
      )
    else:
      print(f"Paciente encontrado: {p.nombre}")
      try:
        sistolica = int(input("Presión sistólica (ej. 120): "))
        diastolica = int(input("Presión diastólica (ej. 80): "))
        fc = int(input("Frecuencia cardíaca en lpm (ej. 75): "))
        fr = int(input("Frecuencia respiratoria en rpm (ej. 18): "))
        temp = float(input("Temperatura en °C (ej. 36.5): "))
        peso = float(input("Peso en kg (ej. 70.5): "))
        talla = float(input("Talla en metros (ej. 1.70): "))

        # Validaciones de rangos lógicos y reales
        if not (50 <= sistolica <= 250):
          raise ValueError(
              "La presión sistólica debe estar entre 50 y 250 mmHg."
          )
        if not (30 <= diastolica <= 150):
          raise ValueError(
              "La presión diastólica debe estar entre 30 y 150 mmHg."
          )
        if not (30 <= fc <= 220):
          raise ValueError(
              "La frecuencia cardíaca debe estar entre 30 y 220 lpm."
          )
        if not (8 <= fr <= 60):
          raise ValueError(
              "La frecuencia respiratoria debe estar entre 8 y 60 rpm."
          )
        if not (34.0 <= temp <= 43.0):
          raise ValueError(
              "La temperatura debe ser un valor realista entre 34.0°C y 43.0°C."
          )
        if not (1.0 <= peso <= 500.0):
          raise ValueError("El peso debe estar entre 1 kg y 500 kg.")
        if not (0.5 <= talla <= 2.5):
          raise ValueError(
              "La talla debe estar en metros (ej. 1.70) y ser válida."
          )

        # Cálculo del IMC
        imc = peso / (talla * talla)
        imc_redondeado = round(imc, 2)

        # Guardar en el diccionario de triaje
        p.triaje = {
            "presion": f"{sistolica}/{diastolica}",
            "fc": fc,
            "fr": fr,
            "temp": temp,
            "peso": peso,
            "talla": talla,
            "imc": imc_redondeado,
        }

        print("\n¡Triaje guardado correctamente!")
        print(f" IMC Calculado: {imc_redondeado}")
        print(f" Presión: {sistolica}/{diastolica} mmHg")
        print(f" Frecuencia Cardíaca: {fc} lpm")
        print(f" Frecuencia Respiratoria: {fr} rpm")
        print(f" Temperatura: {temp} °C")
        print(f" Peso: {peso} kg | Talla: {talla} m")

      except ValueError as e:
        print(f"Error de validación: {e}")

  elif (opcion == "4"):
      if len(pacientes) <= 0:
          print("No hay pacientes registrados. Intente registrar pacientes.")

      for i in range(len(pacientes)):
          print("-----------------------------------------")
          print(f"Paciente {i+1}:")
          print(f"Nombre: {pacientes[i].nombre}")
          print(f"DNI: {pacientes[i].dni}")
          print(f"Código: {pacientes[i].codigo}")
          if pacientes[i].triaje is not None:
              print("Triaje registrado:")
              print(f" Presión Arterial: {pacientes[i].triaje['presion']} mmHg")
              print(f" Frecuencia Cardíaca: {pacientes[i].triaje['fc']} lpm")
              print(f" Frecuencia Respiratoria: {pacientes[i].triaje['fr']} rpm")
              print(f" Temperatura: {pacientes[i].triaje['temp']} °C")
              print(f" Peso: {pacientes[i].triaje['peso']} kg | Talla: {pacientes[i].triaje['talla']} m")
              print(f" IMC: {pacientes[i].triaje['imc']}")
          else:
              print("Aún no tiene triaje registrado.")
          print("-----------------------------------------")

  elif opcion == "5":
    print("Saliendo del sistema. ¡Hasta luego!")
    break
  else:
    print("Opción incorrecta. Intente de nuevo.")

  input("\nPresiona Enter para continuar...")