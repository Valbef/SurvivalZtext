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
        ("Tela", 30)
    ],

    "Infectado corredor": [
        ("Tela", 30, 1, 2),
        ("Metal", 5)
    ],

    # -------------------------
    # BRUTO
    # -------------------------

    "Infectado bruto": [
        ("Metal", 10),
        ("Tela", 35, 1, 2)
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

    for botin in botin_enemigo:

        nombre = botin[0]
        probabilidad = botin[1]

        if len(botin) >= 4:
            cantidad_minima = botin[2]
            cantidad_maxima = botin[3]
        else:
            cantidad_minima = 1
            cantidad_maxima = 1

        if random.randint(1, 100) > probabilidad:
            continue

        if nombre not in objetos:

            print(
                f"\n⚠️ El objeto '{nombre}' "
                f"no existe en objetos.py."
            )

            continue

        cantidad = random.randint(
            cantidad_minima,
            cantidad_maxima
        )

        objeto = deepcopy(
            objetos[nombre]
        )

        objeto.cantidad = cantidad

        if objeto.usos is not None:

            objeto.usos_restantes = (
                objeto.usos * cantidad
            )

        # =========================
        # OBJETOS APILABLES
        # =========================

        if objeto.apilable:

            for obj in jugador.inventario:

                if obj.nombre == nombre:

                    obj.cantidad += cantidad

                    if obj.usos is not None:
                        obj.usos_restantes += (
                            objeto.usos * cantidad
                        )

                    print(
                        f"📦 Has conseguido "
                        f"{cantidad} x {nombre}."
                    )

                    encontrado = True

                    break

            else:

                jugador.inventario.append(
                    objeto
                )

                print(
                    f"📦 Has conseguido "
                    f"{cantidad} x {nombre}."
                )

                encontrado = True

        # =========================
        # OBJETOS NO APILABLES
        # =========================

        else:

            for _ in range(cantidad):

                nuevo_objeto = deepcopy(
                    objetos[nombre]
                )

                jugador.inventario.append(
                    nuevo_objeto
                )

            print(
                f"📦 Has conseguido "
                f"{cantidad} x {nombre}."
            )

            encontrado = True

    if not encontrado:

        print(
            "No encuentras nada útil."
        )

    return encontrado