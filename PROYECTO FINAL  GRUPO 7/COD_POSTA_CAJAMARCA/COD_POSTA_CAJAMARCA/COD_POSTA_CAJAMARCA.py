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

      # Lista simple para guardar a los pacientes registrados
pacientes = []


def buscar_paciente(dni):
  for p in pacientes:
    if p.dni == dni:
      return p
  return None


while True:
  print("\n--- MENÚ PRINCIPAL ---")
  print("1. Registrar paciente")
  print("2. Buscar paciente")
  print("3. Ingresar triaje")
  print("4. Salir")
  opcion = input("Elige una opción: ") if opcion == "1":
    nombre = input("Nombre: ")
    dni = input("DNI: ")
    codigo = input("Código: ")

    if buscar_paciente(dni) is None:
      pacientes.append(Paciente(nombre, dni, codigo))
      print("Paciente registrado.")
    else:
      print("Ese DNI ya existe.")

  elif opcion == "2":
    dni = input("DNI a buscar: ")
    p = buscar_paciente(dni)

    if p is not None:
      print(f"Encontrado: {p.nombre} | Código: {p.codigo}")
      if p.triaje is not None:
        print(f"IMC registrado: {p.triaje.calcular_imc():.2f}")
    else:
      print("Paciente no encontrado.")

  elif opcion == "3":
    dni = input("DNI del paciente para triaje: ")
    p = buscar_paciente(dni)

    if p is not None:
      sis = int(input("Presión sistólica: "))
      dia = int(input("Presión diastólica: "))
      fc = int(input("Frecuencia cardíaca: "))
      fr = int(input("Frecuencia respiratoria: "))
      temp = float(input("Temperatura: "))
      sat = int(input("Saturación de oxígeno: "))
      peso = float(input("Peso (kg): "))
      talla = float(input("Talla (m): "))

      p.triaje = Triaje(sis, dia, fc, fr, temp, sat, peso, talla)
      print(f"Triaje guardado. Su IMC es: {p.triaje.calcular_imc():.2f}")
    else:
      print("Primero debes registrar al paciente.")

  elif opcion == "4":
    print("Saliendo...")
    break
  else:
    print("Opción incorrecta.")
