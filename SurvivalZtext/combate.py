import random
from botin_enemigos import obtener_botin

RESET = "\033[0m"
BOLD = "\033[1m"  #(Negrita)
GREEN = "\033[92m"
LIGHT_GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"

def iniciar_combate(jugador, enemigo, objetos):

    print("\n⚔️ COMIENZA EL COMBATE")
    print(f"\nUn {enemigo.nombre} aparece.")

    while jugador.vida > 0 and enemigo.vivo():

        print("\n----------------")
        print(f"{jugador.nombre} ❤️ {jugador.vida}")
        print(f"{enemigo.nombre} ❤️ {enemigo.vida}")
        print("----------------")

        print("""
1. Atacar
2. Disparar
3. Defender
4. Huir
""")

        opcion = input("> ")

        # ==========================
        # ATAQUE CUERPO A CUERPO
        # ==========================

        if opcion == "1":

            arma = jugador.arma_cuerpo_a_cuerpo()

            if arma:

                daño = arma.daño + random.randint(-3, 3)

                daño -= enemigo.defensa

                if daño < 1:
                    daño = 1

                enemigo.vida -= daño

                print(f"\n{WHITE}🔪 Atacas con {arma.nombre}.{RESET}")
                print(f"{LIGHT_GREEN}Causas {daño} de daño.{RESET}")

                if arma.desgastar():

                    print(f"\n💥 Tu {arma.nombre} se ha roto.")

                    jugador.inventario.remove(arma)

            else:

                daño = random.randint(4, 8)

                daño -= enemigo.defensa

                if daño < 1:
                    daño = 1

                enemigo.vida -= daño

                print(f"\n👊{WHITE} Golpeas con los puños.{RESET}")
                print(f"{LIGHT_GREEN}Causas {daño} de daño.{RESET}")
                input("\nPulsa ENTER para continuar...")


        # ==========================
        # DISPARAR
        # ==========================

        elif opcion == "2":

            arma = jugador.arma_de_fuego()

            if arma is None:

                print(f"\n❌{YELLOW} No tienes un arma de fuego.{RESET}")
                input("\nPulsa ENTER para continuar...")

            elif jugador.municion <= 0:

                print(f"\n❌{YELLOW} No tienes munición.{RESET}")
                input("\nPulsa ENTER para continuar...")

            else:

                # ==========================
                # COMPROBAR ENCASQUILLAMIENTO
                # ==========================

                if random.randint(1, 100) <= arma.atasco:

                    print(
                        f"\n🔫{RED} ¡Tu {arma.nombre} se ha encasquillado!{RESET}"
                    )

                    input(
                        "\nPulsa ENTER para continuar..."
                    )

                else:

                    # ==========================
                    # CONSUMIR MUNICIÓN
                    # ==========================

                    jugador.municion -= 1

                    # ==========================
                    # CALCULAR DAÑO
                    # ==========================

                    daño = arma.daño + random.randint(-5, 5)

                    daño -= enemigo.defensa

                    if daño < 1:
                        daño = 1

                    enemigo.vida -= daño

                    print(
                        f"\n🔫{WHITE} Disparas con {arma.nombre}.{RESET}"
                    )

                    print(
                        f"{LIGHT_GREEN}Causas {daño} de daño.{RESET}"
                    )

                    input(
                        "\nPulsa ENTER para continuar..."
                    )

                # ==========================
                # DESGASTAR ARMA
                # ==========================

                if arma.desgastar():

                    print(
                        f"\n💥{YELLOW} Tu {arma.nombre} se ha roto.{RESET}"
                    )

                    jugador.inventario.remove(arma)

                    input(
                        "\nPulsa ENTER para continuar..."
                    )


        # ==========================
        # DEFENDER
        # ==========================

        elif opcion == "3":

            print(f"\n🛡️{CYAN} Adoptas una posición defensiva.{RESET}")

            jugador.defendiendo = True
            input("\nPulsa ENTER para continuar...")

        # ==========================
        # HUIR
        # ==========================

        elif opcion == "4":

            if random.randint(1, 100) <= 50:

                print(f"\n🏃{CYAN} Consigues escapar.{RESET}")
                input("\nPulsa ENTER para continuar...")

                return False

            else:

                print(f"\n❌{YELLOW} No consigues escapar.{RESET}")
                input("\nPulsa ENTER para continuar...")

        else:

            print("\nOpción no válida.")

            continue

        # ==========================
        # TURNO DEL ENEMIGO
        # ==========================

        if enemigo.vivo():

            daño = enemigo.atacar()

            if getattr(jugador, "defendiendo", False):

                daño //= 2

                jugador.defendiendo = False

            jugador.vida -= daño

            if jugador.vida < 0:

                jugador.vida = 0

            print(f"{RED}\n{enemigo.nombre} te causa {daño} de daño.{RESET}")
            input("\nPulsa ENTER para continuar...")

    # ==========================
    # FIN DEL COMBATE
    # ==========================

    if jugador.vida <= 0:

        print(f"{RED}\n☠️ Has muerto.{RESET}")

        return False

    print(f"{GREEN}\n🏆 Has derrotado a {enemigo.nombre}.{RESET}")

    jugador.experiencia += enemigo.experiencia

    jugador.comprobar_nivel()

    obtener_botin(
        jugador,
        enemigo,
        objetos
    )

    input("\nPulsa ENTER para continuar...")

    return True