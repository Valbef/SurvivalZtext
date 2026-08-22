import random
from copy import deepcopy
from enemigos import enemigo_aleatorio
from combate import iniciar_combate



TABLAS_BOTIN = {

    "Hospital": [
        ("Botiquín", 30),
        ("Botella de agua", 20),
        ("Radio", 1)
    ],

    "Supermercado": [
        ("Lata de comida", 40),
        ("Botella de agua", 30),
        ("Pilas", 10)
    ],

    "Centro Ciudad": [
        ("Lata de comida", 10),
        ("Botella de agua", 15),
        ("Pilas", 5)
    ],

    "Centro Comercial": [
        ("Lata de comida", 10),
        ("Botella de agua", 15),
        ("Herramientas", 3),
        ("Radio", 5)
    ],

    "Comisaría": [
        ("Lata de comida", 10),
        ("Caja de munición", 30),
        ("Botiquín", 15)
    ],

    "Gasolinera": [
        ("Botella de agua", 15),
        ("Lata de comida", 10),
        ("Herramientas", 7),
        ("Mapa", 4)
    ],

    "Bosque": [
        ("Botella de agua", 10)
    ]
}

def saquear(jugador, objetos):

    lugar = jugador.localizacion

    if lugar not in TABLAS_BOTIN:

        print("\nNo parece haber nada interesante.")
        input("\nPulsa ENTER para continuar...")

        return



    print("\n🔍 Buscando...")

    # =========================
    # POSIBLE EMBOSCADA
    # =========================

    if random.randint(1, 100) <= 25:


        enemigo = enemigo_aleatorio()


        print(
            f"\n⚠️ Algo se mueve entre las sombras..."
        )

        # 50% combate normal / 50% ataque sorpresa

        if random.randint(1, 100) <= 50:

            print(
                f"\n🧟 Aparece un {enemigo.nombre}."
            )

            iniciar_combate(
                jugador,
                enemigo
            )


        else:

            daño = random.randint(
                5,
                enemigo.daño
            )

            jugador.vida -= daño

            print(
                f"""
        🩸 ¡Ataque sorpresa!

        Un {enemigo.nombre} te golpea antes de que puedas reaccionar.

        Pierdes {daño} de vida.
        """
            )

            if jugador.vida <= 0:
                jugador.vida = 0

                print(
                    "\n☠️ Has muerto durante el saqueo."
                )

                return

            input(
                "\nPulsa ENTER para enfrentarte al enemigo..."
            )

            print(
                f"\n🧟 Defiendete de el {enemigo.nombre}."
            )

            resultado = iniciar_combate(
                jugador,
                enemigo
            )

            if not resultado and jugador.vida <= 0:
                jugador.vida = 0

                print(
                    "\n☠️ Has muerto durante el combate."
                )

                return

    encontrados = 0
    maximo_botin = random.randint(1,1)


    encontrado = False


    for nombre, probabilidad in TABLAS_BOTIN[lugar]:

        if encontrados >= maximo_botin:
            break

        if random.randint(1,100) <= probabilidad:

            objeto = deepcopy(objetos[nombre])

            # Objetos consumibles apilables
            if nombre in (
                    "Botella de agua",
                    "Lata de comida",
                    "Pilas",
                    "Herramientas"
            ):

                for obj in jugador.inventario:

                    if obj.nombre == nombre:
                        obj.cantidad += 1
                        obj.usos_restantes += obj.usos

                        break

                else:

                    jugador.inventario.append(objeto)

            # Objetos únicos o con durabilidad individual
            else:

                jugador.inventario.append(objeto)

            print(f"Has encontrado {nombre}")

            encontrado = True

            encontrados += 1

    if not encontrado:

        print("No encuentras nada.")


    jugador.avanzar_tiempo(1)

    input("\nPulsa ENTER para continuar...")
