import random


class Persona:
    def __init__(self, nombre, dni, num_telf, direccion):
        self.nombre = nombre
        self.dni = dni
        self.num_telf = num_telf
        self.direccion = direccion

    def dni_oculto(self):
        return "****" + self.dni[4:]


class Paciente(Persona):
    def __init__(
        self,
        nombre,
        dni,
        num_telf,
        direccion,
        num_emergencia,
        codigo,
        grupo_sanguineo,
        tiene_sis,
    ):
        super().__init__(nombre, dni, num_telf, direccion)
        self.num_emergencia = num_emergencia
        self.codigo = codigo
        self.grupo_sanguineo = grupo_sanguineo
        self.tiene_sis = tiene_sis
        self.triaje = None


class Enfermera(Persona):
    def __init__(self, nombre, dni, num_telf, direccion, codigo_cep):
        super().__init__(nombre, dni, num_telf, direccion)
        self.codigo_cep = codigo_cep


enfermeras = [
    Enfermera("Lucía Mendoza", "41234567", "987654321", "Jr. Comercio 120", "CEP-10234"),
    Enfermera("Carla Quispe", "45678912", "912345678", "Av. Cajamarca 45", "CEP-20489"),
]

pacientes = []
codigos_usados = []


def buscar_paciente(dato):
    for p in pacientes:
        if p.dni == dato or p.codigo.upper() == dato.upper():
            return p
    return None


def buscar_enfermera_por_dni(dni_ingresado):
    for e in enfermeras:
        if e.dni == dni_ingresado:
            return e
    return None