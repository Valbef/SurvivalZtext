import random
from copy import deepcopy
from enemigos import enemigo_aleatorio
from combate import iniciar_combate
from efectos import write, writefast

RESET = "\033[0m"
BOLD = "\033[1m"  #(Negrita)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"

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
        ("Tela", 10),
        ("Caja de cerillas", 5),
    ],

    "Gasolinera": [
        ("Botella de agua", 20),
        ("Lata de comida", 15),
        ("Caramelos", 5),
        ("Caja de cigarrillos", 10),
        ("Caja de cerillas", 15),
        ("Herramientas", 7),
        ("Mapa", 3)
    ],

    "Taller Mecanico": [
        ("Botella de agua", 10),
        ("Cerveza", 10),
        ("Caja de cigarrillos", 7),
        ("Caja de cerillas", 7),
        ("Herramientas", 10),
        ("Tuberia", 5),
        ("Metal", 2),
        ("Muelle", 7),
        ("Tornillo", 10)
    ],

    "Centro Ciudad": [
        ("Lata de comida", 15),
        ("Botella de agua", 15),
        ("Caramelos", 6),
        ("Caja de cigarrillos", 8),
        ("Caja de cerillas", 10),
        ("Pilas", 5)
    ],

    "Bar": [
        ("Cerveza", 25),
        ("Jamón Ibérico", 5),
        ("Caja de cigarrillos", 10),
        ("Caja de cerillas", 10),
        ("Botella de agua", 5)
    ],

    "Iglesia": [
        ("Caja de munición", 2),
        ("Botella de agua", 5),
        ("Hierbas", 10)
    ],

    "Comisaría": [
        ("Lata de comida", 15),
        ("Caja de munición", 20),
        ("Caja de cigarrillos", 10),
        ("Caja de cerillas", 15),
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
        ("Caramelos", 20),
        ("Botella de agua", 15),
        ("Caja de cigarrillos", 10),
        ("Caja de cerillas", 15),
        ("Herramientas", 3),
        ("Cuerda", 10),
        ("Radio", 2)
    ],

    "Escuela": [
        ("Botella de agua", 15),
        ("Caramelos", 5),
        ("Tela", 15)
    ],

    "Supermercado": [
        ("Lata de comida", 40),
        ("Botella de agua", 30),
        ("Jamón Ibérico", 2),
        ("Caramelos", 5),
        ("Cuerda", 10),
        ("Caja de cerillas", 20),
        ("Pilas", 10)
    ],

    "Estación Bomberos": [
        ("Botella de agua", 25),
        ("Botiquín", 10),
        ("Tuberia", 5),
        ("Tela", 5),
        ("Cuerda", 10)
    ],

    "Camping": [
        ("Botella de agua", 20),
        ("Cuerda", 10),
        ("Caramelos", 5),
        ("Lata de comida", 20),
        ("Caja de cigarrillos", 10),
        ("Jamón Ibérico", 2),
        ("Caja de cerillas", 10)
    ],

    "Torre Radio": [
        ("Pilas", 10),
        ("Hierbas", 15),
        ("Componentes electronicos", 20),
        ("Radio", 5)
    ],

    "Desguace": [
        ("Pilas", 2),
        ("Hierbas", 15),
        ("Componentes electronicos", 10),
        ("Herramientas", 1),
        ("Metal", 15),
        ("Tuberia", 5),
        ("Muelle", 7),
        ("Tornillo", 10)
    ],

    "Montaña": [
        ("Madera", 25),
        ("Hierbas", 30),
        ("Botella de agua", 2)
    ],

    "Cueva montaña": [
        ("Metal", 10),
        ("Hierbas", 20),
        ("Botella de agua", 2)
    ],

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
            f"\n{YELLOW}⚠️ Algo se mueve entre las sombras...{RESET}"
        )

        # 50% combate normal / 50% ataque sorpresa

        if random.randint(1, 100) <= 50:

            jugador.moral -= 2

            write(
                f"\n{YELLOW}🧟 Aparece un {enemigo.nombre}.{RESET}"
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
                f"""{RED}
        🩸 ¡Ataque sorpresa!{RESET}

{YELLOW}¡Un {enemigo.nombre} te golpea antes de que puedas reaccionar!{RESET}

        {RED}Pierdes {daño} de vida.
        Tu moral ha bajado.{RESET}
        """
            )

            if jugador.vida <= 0:

                jugador.vida = 0

                print(
                    f"\n{RED}☠️ Has muerto durante el saqueo.{RESET}"
                )

                return

            input(
                "\nPulsa ENTER para enfrentarte al enemigo..."
            )

            print(f"\n{YELLOW} Defiéndete del {enemigo.nombre}.{RESET}")


            resultado = iniciar_combate(
                jugador,
                enemigo,
                objetos
            )

            if not resultado and jugador.vida <= 0:

                jugador.vida = 0

                write(
                    f"\n☠️{RED} Has muerto en combate.{RESET}"
                )

                return

    # =========================
    # BOTÍN
    # =========================

    encontrados = 0

    maximo_botin = random.randint(1, 1)

    encontrado = False

    for nombre, probabilidad in TABLAS_BOTIN[lugar]:

        if encontrados >= maximo_botin:
            break

        if random.randint(1, 100) > probabilidad:
            continue

        # =========================
        # COMPROBAR QUE EXISTE
        # =========================

        if nombre not in objetos:

            print(
                f"\n⚠️ El objeto '{nombre}' "
                f"no existe en objetos.py."
            )

            continue

        objeto = deepcopy(
            objetos[nombre]
        )

        # =========================
        # OBJETOS APILABLES
        # =========================

        if objeto.apilable:

            # =====================================
            # OBJETOS CON USOS
            # =====================================
            # Cada unidad mantiene sus propios usos.
            # No se deben fusionar en un único objeto.

            if objeto.usos is not None:

                jugador.inventario.append(
                    objeto
                )

            # =====================================
            # OBJETOS SIN USOS
            # =====================================
            # Estos sí pueden acumularse normalmente.

            else:

                objeto_existente = None

                for obj in jugador.inventario:

                    if obj.nombre == nombre:
                        objeto_existente = obj
                        break

                if objeto_existente:

                    objeto_existente.cantidad += objeto.cantidad

                else:

                    jugador.inventario.append(
                        objeto
                    )

        # =========================
        # OBJETOS NO APILABLES
        # =========================

        else:

            jugador.inventario.append(
                objeto
            )

        print(
            f"{GREEN}Has encontrado {nombre}{RESET}"
        )

        encontrado = True

        encontrados += 1

    # =========================
    # SIN BOTÍN
    # =========================

    if not encontrado:

        jugador.moral -= 1

        print(
            f"{WHITE}No encuentras nada...{RESET}"
        )

    # =========================
    # PASO DEL TIEMPO
    # =========================

    jugador.avanzar_tiempo(1)

    input(
        "\nPulsa ENTER para continuar..."
    )

