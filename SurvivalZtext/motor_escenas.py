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


    # VIDA

    if "vida" in opcion:

        jugador.vida += opcion["vida"]

        jugador.vida = max(
            0,
            min(jugador.vida,100)
        )


    # MORAL

    if "moral" in opcion:

        jugador.moral += opcion["moral"]

        jugador.moral = max(
            0,
            min(jugador.moral,100)
        )


    # MUNICIÓN SUELTA

    if "municion" in opcion:

        jugador.municion += opcion["municion"]

        print(
            f"\n🔫 Has conseguido {opcion['municion']} balas."
        )


    # OBJETOS

    if "objeto" in opcion:

        nombre = opcion["objeto"]


        if nombre in objetos:


            nuevo = deepcopy(
                objetos[nombre]
            )


            # Objetos apilables

            if nombre in (
                "Botella de agua",
                "Lata de comida",
                "Herramientas",
                "Pilas"
            ):


                for objeto in jugador.inventario:


                    if objeto.nombre == nombre:

                        objeto.cantidad += nuevo.cantidad

                        objeto.usos_restantes += nuevo.usos

                        print(
                            f"\n🎒 Has encontrado otro {nombre}."
                        )

                        break


                else:

                    jugador.inventario.append(
                        nuevo
                    )

                    print(
                        f"\n🎒 Has conseguido: {nombre}"
                    )


            else:

                jugador.inventario.append(
                    nuevo
                )

                print(
                    f"\n🎒 Has conseguido: {nombre}"
                )
    jugador.limitar_estadisticas()