import random
from copy import deepcopy
from escenas import ESCENAS_POR_ZONA, escenas


def comprobar_escena(jugador, objetos):

    zona = jugador.localizacion


    if zona not in ESCENAS_POR_ZONA:
        return


    # Probabilidad de escena
    if random.randint(1, 100) > 30:
        return


    escena = random.choice(
        ESCENAS_POR_ZONA[zona]
    )


    ejecutar_escena(
        jugador,
        escena,
        objetos
    )


def ejecutar_escena(jugador, nombre_escena, objetos):

    if nombre_escena not in escenas:

        print("Escena no encontrada.")

        return


    escena = escenas[nombre_escena]


    print("\n====================")
    print(escena["texto"])
    print("====================")


    for numero, opcion in escena["opciones"].items():

        print(
            f"{numero}. {opcion['texto']}"
        )


    while True:

        eleccion = input("\n> ")


        if eleccion in escena["opciones"]:

            resultado = escena["opciones"][eleccion]

            aplicar_efectos(
                jugador,
                resultado,
                objetos
            )

            return resultado.get("destino")



        else:

            print("Opción no válida.")



def aplicar_efectos(jugador, opcion, objetos):

    # =========================
    # VIDA
    # =========================

    if "vida" in opcion:

        jugador.vida += opcion["vida"]

        jugador.vida = max(
            0,
            min(jugador.vida, 100)
        )

    # =========================
    # MORAL
    # =========================

    if "moral" in opcion:

        jugador.moral += opcion["moral"]

        jugador.moral = max(
            0,
            min(jugador.moral, 100)
        )

    # =========================
    # MUNICIÓN
    # =========================

    if "municion" in opcion:

        jugador.municion += opcion["municion"]

        print(
            f"\n🔫 Has conseguido "
            f"{opcion['municion']} balas."
        )

    # =========================
    # OBJETOS
    # =========================

    if "objeto" in opcion:

        objetos_encontrados = opcion["objeto"]

        # Si es un solo objeto, lo convertimos en lista
        if isinstance(objetos_encontrados, str):
            objetos_encontrados = [objetos_encontrados]

        for nombre in objetos_encontrados:

            if nombre not in objetos:
                print(
                    f"\n❌ El objeto '{nombre}' no existe."
                )
                continue

            nuevo = deepcopy(
                objetos[nombre]
            )

            # =========================
            # OBJETOS APILABLES
            # =========================

            if nuevo.apilable:

                encontrado = False

                for objeto in jugador.inventario:

                    if objeto.nombre == nombre:

                        objeto.cantidad += nuevo.cantidad

                        if objeto.usos is not None:

                            objeto.usos_restantes += (
                                nuevo.usos_restantes
                            )

                        print(
                            f"\n🎒 Has conseguido otro "
                            f"{nombre}."
                        )

                        encontrado = True
                        break

                if not encontrado:

                    jugador.inventario.append(
                        nuevo
                    )

                    print(
                        f"\n🎒 Has conseguido: {nombre}"
                    )

            # =========================
            # OBJETOS NO APILABLES
            # =========================

            else:

                jugador.inventario.append(
                    nuevo
                )

                print(
                    f"\n🎒 Has conseguido: {nombre}"
                )


    # =========================
    # COMBATE
    # =========================

    if "combate" in opcion:

        from enemigos import crear_enemigos
        from combate import iniciar_combate

        enemigos = crear_enemigos()

        nombre_enemigo = opcion["combate"]

        if nombre_enemigo in enemigos:

            enemigo = deepcopy(
                enemigos[nombre_enemigo]
            )

            iniciar_combate(
                jugador,
                enemigo,
                objetos
            )

        else:

            print(
                f"\n❌ Enemigo no encontrado: "
                f"{nombre_enemigo}"
            )


    # =========================
    # ESTADÍSTICAS
    # =========================

    jugador.limitar_estadisticas()

    return opcion.get("destino")
