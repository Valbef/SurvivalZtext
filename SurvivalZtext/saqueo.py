import random
from copy import deepcopy
from enemigos import enemigo_aleatorio
from combate import iniciar_combate
from efectos import write, writefast

TABLAS_BOTIN = {

    "Bosque": [
        ("Madera", 25),
        ("Hierbas", 20),
        ("Botella de agua", 2)
    ],

    "Cabaña": [
        ("Botella de agua", 5),
        ("Madera", 15),
        ("Cuerda", 10),
        ("Tela", 10)
    ],

    "Gasolinera": [
        ("Botella de agua", 20),
        ("Lata de comida", 15),
        ("Caja de cigarrillos", 10),
        ("Herramientas", 7),
        ("Mapa", 3)
    ],

    "Centro Ciudad": [
        ("Lata de comida", 15),
        ("Botella de agua", 15),
        ("Caja de cigarrillos", 8),
        ("Pilas", 5)
    ],

    "Comisaría": [
        ("Lata de comida", 15),
        ("Caja de munición", 20),
        ("Caja de cigarrillos", 10),
        ("Botiquín", 5)
    ],

    "Hospital": [
        ("Botiquín", 35),
        ("Componentes electronicos", 8),
        ("Botella de agua", 10),
    ],

    "Laboratorio": [
        ("Botiquín", 30),
        ("Botella de agua", 5),
        ("Componentes electronicos", 10)
    ],

    "Centro Comercial": [
        ("Lata de comida", 20),
        ("Botella de agua", 15),
        ("Caja de cigarrillos", 10),
        ("Herramientas", 3),
        ("Cuerda", 10),
        ("Radio", 2)
    ],

    "Escuela": [
        ("Botella de agua", 15),
        ("Tela", 15)
    ],

    "Supermercado": [
        ("Lata de comida", 40),
        ("Botella de agua", 30),
        ("Cuerda", 10),
        ("Pilas", 10)
    ],

    "Estación Bomberos": [
        ("Botella de agua", 25),
        ("Botiquín", 10),
        ("Tela", 5),
        ("Cuerda", 10)
    ],

    "Camping": [
        ("Botella de agua", 15),
        ("Cuerda", 10),
        ("Lata de comida", 12),
        ("Caja de cigarrillos", 10)
    ],

    "Torre Radio": [
        ("Pilas", 10),
        ("Hierbas", 15),
        ("Componentes electronicos", 20),
        ("Radio", 5)
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

            jugador.moral -= 2

            write(
                f"\n🧟 Aparece un {enemigo.nombre}."
            )

            iniciar_combate(
                jugador,
                enemigo,
                objetos
            )


        else:

            daño = random.randint(
                5,
                enemigo.daño
            )

            jugador.vida -= daño
            jugador.moral -= 6

            writefast(
                f"""
        🩸 ¡Ataque sorpresa!

        Un {enemigo.nombre} te golpea antes de que puedas reaccionar.

        Pierdes {daño} de vida.
        Tu moral ha bajado.
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
                enemigo,
                objetos
            )

            if not resultado and jugador.vida <= 0:
                jugador.vida = 0

                write(
                    "\n☠️ Has muerto en combate."
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
                    "Herramientas",
                    "Caja de cigarrillos"
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

        jugador.moral -= 1

        print("No encuentras nada.")


    jugador.avanzar_tiempo(1)

    input("\nPulsa ENTER para continuar...")