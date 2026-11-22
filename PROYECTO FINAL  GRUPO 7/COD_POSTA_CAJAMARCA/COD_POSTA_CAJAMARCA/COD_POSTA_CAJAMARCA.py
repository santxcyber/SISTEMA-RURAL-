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


# 2 enfermeras registradas para triaje (puedes cambiar sus datos)
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


def generar_codigo_unico():
    if len(pacientes) >= 100:
        return None
    while True:
        numero = random.randint(1, 100)
        codigo = f"HP-{numero:03d}"
        if codigo not in codigos_usados:
            codigos_usados.append(codigo)
            return codigo


while True:
    print("-----------------------------------------")
    print("  SISTEMARURAL-PE | P.S. PORCÓN BAJO")
    print("-----------------------------------------")
    print("1. Registrar paciente")
    print("2. Buscar paciente (DNI o Código)")
    print("3. Ingresar triaje (requiere DNI enfermera)")
    print("4. Ver pacientes registrados")
    print("5. Salir")
    print("-----------------------------------------")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        print("--- REGISTRAR PACIENTE ---")
        if len(pacientes) >= 100:
            print("Error: Se alcanzó el límite máximo de 100 pacientes.")
            continue

        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            continue

        dni = input("DNI (8 dígitos): ").strip()
        if len(dni) != 8 or not dni.isdigit():
            print("Error: El DNI debe tener exactamente 8 números.")
            continue

        if buscar_paciente(dni) is not None:
            print("Error: Ese DNI ya está registrado en el sistema.")
            continue

        direccion = input("Dirección: ").strip()
        if not direccion:
            print("Error: La dirección no puede estar vacía.")
            continue

        num_telf = input("Número de teléfono del paciente (9 dígitos): ").strip()
        if len(num_telf) != 9 or not num_telf.isdigit():
            print("Error: El teléfono del paciente debe tener 9 dígitos numéricos.")
            continue

        num_emergencia = input("Número de teléfono de emergencia (9 dígitos): ").strip()
        if len(num_emergencia) != 9 or not num_emergencia.isdigit():
            print("Error: El teléfono de emergencia debe tener 9 dígitos numéricos.")
            continue

        grupo_sanguineo = input("Grupo sanguíneo (ej. O+, A+, B+, AB+): ").strip().upper()
        if not grupo_sanguineo:
            print("Error: El grupo sanguíneo no puede estar vacío.")
            continue

        sis_resp = input("¿Tiene seguro SIS? (si / no): ").strip().lower()
        if sis_resp == "si":
            tiene_sis = "Sí"
        elif sis_resp == "no":
            tiene_sis = "No"
        else:
            print("Error: Responda solo 'si' o 'no' para el seguro SIS.")
            continue

        codigo = generar_codigo_unico()
        nuevo_paciente = Paciente(
            nombre,
            dni,
            num_telf,
            direccion,
            num_emergencia,
            codigo,
            grupo_sanguineo,
            tiene_sis,
        )
        pacientes.append(nuevo_paciente)

        print("\n¡Paciente registrado con éxito!")
        print(
            f"Código generado: {codigo} | Nombre: {nombre} | "
            f"DNI oculto: {nuevo_paciente.dni_oculto()} | SIS: {tiene_sis}"
        )

    elif opcion == "2":
        print("--- BUSCAR PACIENTE ---")
        dato = input("Ingrese DNI o Código a buscar: ").strip()
        p = buscar_paciente(dato)
        if p is not None:
            print("\n¡Encontrado!")
            print(f"Nombre: {p.nombre}")
            print(f"Código: {p.codigo}")
            print(f"DNI: {p.dni_oculto()}")
            print(f"Dirección: {p.direccion}")
            print(f"Teléfono: {p.num_telf} | Emergencia: {p.num_emergencia}")
            print(f"Grupo sanguíneo: {p.grupo_sanguineo} | Seguro SIS: {p.tiene_sis}")
            if p.triaje is not None:
                print("\n--- Datos de Triaje ---")
                print(f" Fecha: {p.triaje['fecha']}")
                print(f" Enfermera: {p.triaje['enfermera']}")
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
        dni_enf = input("Ingrese su DNI de enfermera para acceder: ").strip()
        enf = buscar_enfermera_por_dni(dni_enf)

        if enf is None:
            print("Acceso denegado: DNI de enfermera no válido.")
        else:
            print(f"Bienvenida, Enfermera {enf.nombre} ({enf.codigo_cep}).")
            dato = input("DNI o Código del paciente para triaje: ").strip()
            p = buscar_paciente(dato)

            if p is None:
                print("Paciente no encontrado. Debe registrarlo primero en la opción 1.")
            else:
                fecha = input("Fecha del triaje (ej. 21/11/2026): ").strip()
                if not fecha:
                    print("Error: La fecha no puede estar vacía.")
                    continue

                print(f"Paciente encontrado: {p.nombre}")
                try:
                    sistolica = int(input("Presión sistólica (ej. 120): "))
                    diastolica = int(input("Presión diastólica (ej. 80): "))
                    fc = int(input("Frecuencia cardíaca en lpm (ej. 75): "))
                    fr = int(input("Frecuencia respiratoria en rpm (ej. 18): "))
                    temp = float(input("Temperatura en °C (ej. 36.5): "))
                    peso = float(input("Peso en kg (ej. 70.5): "))
                    talla = float(input("Talla en metros (ej. 1.70): "))

                    if not (50 <= sistolica <= 250):
                        raise ValueError("La presión sistólica debe estar entre 50 y 250 mmHg.")
                    if not (30 <= diastolica <= 150):
                        raise ValueError("La presión diastólica debe estar entre 30 y 150 mmHg.")
                    if not (30 <= fc <= 220):
                        raise ValueError("La frecuencia cardíaca debe estar entre 30 y 220 lpm.")
                    if not (8 <= fr <= 60):
                        raise ValueError("La frecuencia respiratoria debe estar entre 8 y 60 rpm.")
                    if not (34.0 <= temp <= 43.0):
                        raise ValueError("La temperatura debe ser un valor realista entre 34.0°C y 43.0°C.")
                    if not (1.0 <= peso <= 500.0):
                        raise ValueError("El peso debe estar entre 1 kg y 500 kg.")
                    if not (0.5 <= talla <= 2.5):
                        raise ValueError("La talla debe estar en metros (ej. 1.70) y ser válida.")

                    imc = peso / (talla * talla)
                    imc_redondeado = round(imc, 2)

                    p.triaje = {
                        "fecha": fecha,
                        "enfermera": enf.nombre,
                        "presion": f"{sistolica}/{diastolica}",
                        "fc": fc,
                        "fr": fr,
                        "temp": temp,
                        "peso": peso,
                        "talla": talla,
                        "imc": imc_redondeado,
                    }

                    print("\n¡Triaje guardado correctamente!")
                    print(f" Fecha: {fecha} | Atendido por: {enf.nombre}")
                    print(f" IMC Calculado: {imc_redondeado}")
                    print(f" Presión: {sistolica}/{diastolica} mmHg")
                    print(f" Frecuencia Cardíaca: {fc} lpm")
                    print(f" Frecuencia Respiratoria: {fr} rpm")
                    print(f" Temperatura: {temp} °C")
                    print(f" Peso: {peso} kg | Talla: {talla} m")

                except ValueError as e:
                    print(f"Error de validación: {e}")

    elif opcion == "4":
        if len(pacientes) <= 0:
            print("No hay pacientes registrados. Intente registrar pacientes.")
        else:
            for i in range(len(pacientes)):
                pac = pacientes[i]
                print("-----------------------------------------")
                print(f"Paciente {i + 1}:")
                print(f"Nombre: {pac.nombre}")
                print(f"DNI: {pac.dni_oculto()}")
                print(f"Código: {pac.codigo}")
                print(f"Dirección: {pac.direccion}")
                print(f"Teléfono: {pac.num_telf} | Emergencia: {pac.num_emergencia}")
                print(f"Grupo sanguíneo: {pac.grupo_sanguineo} | Seguro SIS: {pac.tiene_sis}")
                if pac.triaje is not None:
                    print("Triaje registrado:")
                    print(f" Fecha: {pac.triaje['fecha']}")
                    print(f" Enfermera: {pac.triaje['enfermera']}")
                    print(f" Presión Arterial: {pac.triaje['presion']} mmHg")
                    print(f" Frecuencia Cardíaca: {pac.triaje['fc']} lpm")
                    print(f" Frecuencia Respiratoria: {pac.triaje['fr']} rpm")
                    print(f" Temperatura: {pac.triaje['temp']} °C")
                    print(f" Peso: {pac.triaje['peso']} kg | Talla: {pac.triaje['talla']} m")
                    print(f" IMC: {pac.triaje['imc']}")
                else:
                    print("Aún no tiene triaje registrado.")

    elif opcion == "5":
        print("Saliendo del sistema. ¡Hasta luego!")
        break

    else:
        print("Opción incorrecta. Intente de nuevo.")

    input("\nPresiona Enter para continuar...")