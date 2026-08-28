import random
from copy import deepcopy


# ===========================
# BOTÍN DE LOS ENEMIGOS
# ===========================

BOTIN_ENEMIGOS = {

    # -------------------------
    # Animales
    # -------------------------

    "Perro infectado": [
        ("Piel", 80, 1, 2)
    ],

    "Gato infectado": [
        ("Piel", 70)
    ],

    # -------------------------
    # INFECTADOS
    # -------------------------

    "Infectado": [
        ("Tela", 20)
    ],

    "Infectado corredor": [
        ("Tela", 30, 1, 2),
        ("Metal", 5)
    ],

    # -------------------------
    # BRUTO
    # -------------------------

    "Infectado bruto": [
        ("Metal", 5),
        ("Tela", 30, 1,2)
    ],

    # -------------------------
    # SAQUEADOR
    # -------------------------

    "Saqueador": [
        ("Metal", 40),
        ("Tela", 30),
        ("Hierbas", 15),
        ("Cuerda", 20)
    ],

    # -------------------------
    # VAGABUNDO
    # -------------------------

    "Vagabundo": [
        ("Tela", 25),
        ("Hierbas", 20),
        ("Cuerda", 15, 1, 2),
        ("Componentes electronicos", 30)
    ]

}


# ===========================
# OBTENER BOTÍN
# ===========================

def obtener_botin(jugador, enemigo, objetos):

    if enemigo.nombre not in BOTIN_ENEMIGOS:

        return

    botin_enemigo = BOTIN_ENEMIGOS[enemigo.nombre]

    encontrado = False

    print("\n🎒 Buscando entre los restos...")

    for nombre, probabilidad in botin_enemigo:

        if random.randint(1, 100) <= probabilidad:

            objeto = deepcopy(objetos[nombre])

            # -------------------------
            # OBJETOS APILABLES
            # -------------------------

            if objeto.apilable:

                for obj in jugador.inventario:

                    if obj.nombre == nombre:

                        obj.cantidad += objeto.cantidad

                        if obj.usos is not None:
                            obj.usos_restantes += obj.usos

                        print(f"📦 Has conseguido {nombre}.")

                        encontrado = True

                        break

                else:

                    jugador.inventario.append(objeto)

                    print(f"📦 Has conseguido {nombre}.")

                    encontrado = True

            # -------------------------
            # OBJETOS NO APILABLES
            # -------------------------

            else:

                jugador.inventario.append(objeto)

                print(f"📦 Has conseguido {nombre}.")

                encontrado = True

    if not encontrado:

        print("No encuentras nada útil.")

    return encontrado

