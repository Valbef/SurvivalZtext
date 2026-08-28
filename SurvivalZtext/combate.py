import random
from botin_enemigos import obtener_botin


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

                print(f"\n🔪 Atacas con {arma.nombre}.")
                print(f"Causas {daño} de daño.")

                if arma.desgastar():

                    print(f"\n💥 Tu {arma.nombre} se ha roto.")

                    jugador.inventario.remove(arma)

            else:

                daño = random.randint(4, 8)

                daño -= enemigo.defensa

                if daño < 1:
                    daño = 1

                enemigo.vida -= daño

                print(f"\n👊 Golpeas con los puños.")
                print(f"Causas {daño} de daño.")
                input("\nPulsa ENTER para continuar...")

        # ==========================
        # DISPARAR
        # ==========================

        elif opcion == "2":

            pistola = jugador.tiene_pistola()

            if pistola is None:

                print("\n❌ No tienes una pistola.")
                input("\nPulsa ENTER para continuar...")

            elif jugador.municion <= 0:

                print("\n❌ No tienes munición.")
                input("\nPulsa ENTER para continuar...")

            else:

                if random.randint(1, 100) <= pistola.atasco:

                    print("\n🔫 ¡La pistola se ha encasquillado!")
                    input("\nPulsa ENTER para continuar...")

                else:

                    jugador.municion -= 1

                    daño = pistola.daño + random.randint(-5, 5)

                    daño -= enemigo.defensa

                    if daño < 1:
                        daño = 1

                    enemigo.vida -= daño

                    print(f"\n🔫 Disparas.")
                    print(f"Causas {daño} de daño.")
                    input("\nPulsa ENTER para continuar...")

                if pistola.desgastar():

                    print("\n💥 La pistola se ha roto.")

                    jugador.inventario.remove(pistola)
                    input("\nPulsa ENTER para continuar...")

        # ==========================
        # DEFENDER
        # ==========================

        elif opcion == "3":

            print("\n🛡️ Adoptas una posición defensiva.")

            jugador.defendiendo = True
            input("\nPulsa ENTER para continuar...")

        # ==========================
        # HUIR
        # ==========================

        elif opcion == "4":

            if random.randint(1, 100) <= 50:

                print("\n🏃 Consigues escapar.")
                input("\nPulsa ENTER para continuar...")

                return False

            else:

                print("\n❌ No consigues escapar.")
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

            print(f"\n{enemigo.nombre} te causa {daño} de daño.")
            input("\nPulsa ENTER para continuar...")

    # ==========================
    # FIN DEL COMBATE
    # ==========================

    if jugador.vida <= 0:

        print("\n☠️ Has muerto.")

        return False

    print(f"\n🏆 Has derrotado a {enemigo.nombre}.")

    jugador.experiencia += enemigo.experiencia

    obtener_botin(
        jugador,
        enemigo,
        objetos
    )

    input("\nPulsa ENTER para continuar...")

    return True