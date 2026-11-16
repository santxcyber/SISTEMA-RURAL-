class Persona:

  def __init__(self, nombre, dni):
    self.nombre = nombre
    self.dni = dni


class Paciente(Persona):

  def __init__(self, nombre, dni, codigo):
    super().__init__(nombre, dni)
    self.codigo = codigo
    self.triaje = None


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
    # ARREGLO IMC: Si ingresan la talla en cm (ej. 170), se convierte automáticamente a metros (1.70)
    self.talla_m = talla / 100 if talla > 3 else talla

  def calcular_imc(self):
    if self.talla_m <= 0:
      raise ValueError("La talla debe ser mayor a 0.")
    return self.peso_kg / (self.talla_m**2)

  # NUEVO: Muestra todos los datos del triaje con sus símbolos y unidades
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


# Lista simple para guardar a los pacientes registrados
pacientes = []


def validar_entrada(dato):
  dato = dato.strip().upper()
  if not dato:
    raise ValueError("El campo no puede estar vacío.")

  if dato.startswith("HP-") and dato[3:].isdigit():
    return "CODIGO", dato

  if not dato.isdigit() or len(dato) != 8:
    raise ValueError(
        "Debe ingresar un DNI de 8 números (sin letras) o un código válido (ej. HP-001)."
    )

  return "DNI", dato


def buscar_paciente(dato_validado):
  for p in pacientes:
    if p.dni == dato_validado or p.codigo.upper() == dato_validado:
      return p
  return None


while True:
  print ("----------------------")
  print("    MENÚ PRINCIPAL ")
  print("1. Registrar paciente")
  print("2. Buscar paciente")
  print("3. Ingresar triaje")
  print("4. Salir")
  print ("----------------------")
  opcion = input("Elige una opción: ")

  if opcion == "1":
    try:
      nombre = input("Nombre: ")
      _, dni = validar_entrada(input("DNI (8 dígitos): "))
      codigo = input("Código Historia Posta (ej. HP-001): ").strip().upper()

      if buscar_paciente(dni) is None and buscar_paciente(codigo) is None:
        pacientes.append(Paciente(nombre, dni, codigo))
        print("Paciente registrado.")
      else:
        print("Ese DNI o Código ya existe.")
    except ValueError as e:
      print(f"Error: {e}")

  elif opcion == "2":
    try:
      _, dato = validar_entrada(input("DNI o Código Historia Posta a buscar: "))
      p = buscar_paciente(dato)

      if p is not None:
        print(f"\nEncontrado: {p.nombre} | Código: {p.codigo}")
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
              f"Paciente nuevo. Se creó Historia Posta preliminar única: {p.codigo}"
          )
        else:
          print(
              "Código de historia no encontrado. Ingrese su DNI para crear una nueva."
          )
          continue
      else:
        print(f"Historial recuperado: {p.nombre} | Código: {p.codigo}")

      sis = int(input("Presión sistólica (mmHg): "))
      dia = int(input("Presión diastólica (mmHg): "))
      fc = int(input("Frecuencia cardíaca (lpm): "))
      fr = int(input("Frecuencia respiratoria (rpm): "))
      temp = float(input("Temperatura (°C): "))
      sat = int(input("Saturación de oxígeno (%): "))
      peso = float(input("Peso (kg): "))
      talla = float(input("Talla (m o cm): "))

      if peso <= 0 or talla <= 0:
        raise ValueError("El peso y la talla deben ser mayores a 0.")

      p.triaje = Triaje(sis, dia, fc, fr, temp, sat, peso, talla)
      print("\nTriaje guardado correctamente:")
      print(p.triaje.mostrar_datos())

    except ValueError as e:
      print(f"Error de validación: {e}")

  elif opcion == "4":
    print("Saliendo...")
    break
  else:
    print("Opción incorrecta.")