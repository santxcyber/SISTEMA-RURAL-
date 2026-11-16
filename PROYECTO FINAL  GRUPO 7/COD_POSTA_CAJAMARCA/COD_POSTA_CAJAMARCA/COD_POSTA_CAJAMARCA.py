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
  opcion = input("Elige una opción: ")

