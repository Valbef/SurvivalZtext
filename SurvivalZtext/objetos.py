from objeto import Objeto


# ===========================
# EFECTOS DE LOS OBJETOS
# ===========================

def comer_lata(jugador):

    jugador.hambre -= 35
    jugador.vida += 5
    jugador.moral += 3


def beber_agua(jugador):

    jugador.sed -= 40
    jugador.vida += 3
    jugador.moral += 2


def curar(jugador):

    jugador.vida += 40

    if jugador.vida > 100:
        jugador.vida = 100


def abrir_caja_municion(jugador, objeto):

    if objeto.usos_restantes <= 0:

        print("\n❌ La caja está vacía.")

        return False


    jugador.municion += 6

    objeto.usos_restantes -= 1


    print("\n📦 Has abierto una caja de munición.")
    print("🔫 Has conseguido 6 balas.")


    if objeto.usos_restantes <= 0:

        print("📦 La caja de munición se ha agotado.")

        jugador.inventario.remove(objeto)

        return True


    return False

def reparar_objeto(jugador, objeto):

    import random

    herramientas = None

    for obj in jugador.inventario:

        if obj.nombre == "Herramientas":
            herramientas = obj
            break


    if herramientas is None:

        print("\n❌ No tienes herramientas para reparar.")

        return


    if objeto.durabilidad is None:

        print("\n❌ Este objeto no se puede reparar.")

        return


    if objeto.durabilidad >= 100:

        print("\n🔧 El objeto ya está en perfecto estado.")

        return


    reparacion = random.randint(10, 30)


    objeto.durabilidad += reparacion


    if objeto.durabilidad > 100:
        objeto.durabilidad = 100


    herramientas.usar(jugador)


    print(
        f"\n🔧 Has reparado {objeto.nombre} +{reparacion} durabilidad."
    )


    if herramientas.usos_restantes <= 0:

        jugador.inventario.remove(herramientas)

        print("🔧 La caja de herramientas se ha agotado.")


def consultar_mapa(jugador):
    posicion = jugador.localizacion

    mapa = f"""

==============================
            🗺️ MAPA
==============================


                 Torre Radio
                      |
                 Camping
                      |
                     Bosque
                    /     \\
             Cabaña       Gasolinera
                              |
                       Centro Ciudad
                      /      |       \\
             Comisaría   Escuela   Centro Comercial
                 |          |             |
             Hospital   Estación      Supermercado
                 |
            Laboratorio


==============================

Tu posición:

"""

    # Añadimos marcador según localización

    if posicion == "Refugio":
        mapa += """
🏠 Refugio  ◀ TU POSICIÓN
    |
  Bosque
"""

    elif posicion == "Bosque":
        mapa += """
                 Torre Radio
                      |
                 Camping
                      |
             🟢 BOSQUE ◀ TU POSICIÓN
              /        \\
          Cabaña     Gasolinera
"""

    elif posicion == "Gasolinera":
        mapa += """
             Bosque
                |
        ⛽ Gasolinera ◀ TU POSICIÓN
                |
        Centro Ciudad
"""

    elif posicion == "Centro Ciudad":
        mapa += """
        Gasolinera

             |

     🏙️ Centro Ciudad ◀ TU POSICIÓN

       /        |          \\

Comisaría   Escuela   Centro Comercial
"""

    elif posicion == "Hospital":
        mapa += """
        Comisaría

            |

     🏥 Hospital ◀ TU POSICIÓN

            |

       Laboratorio
"""

    elif posicion == "Laboratorio":
        mapa += """
             Hospital

                |

      🧪 Laboratorio ◀ TU POSICIÓN
"""

    elif posicion == "Centro Comercial":
        mapa += """
        Centro Ciudad

             |

     🛒 Centro Comercial ◀ TU POSICIÓN

             |

      Supermercado
"""

    elif posicion == "Supermercado":
        mapa += """
     Centro Comercial

             |

     🏪 Supermercado ◀ TU POSICIÓN
"""

    elif posicion == "Comisaría":
        mapa += """
       Centro Ciudad

             |

     🚔 Comisaría ◀ TU POSICIÓN

             |

        Hospital
"""

    else:
        mapa += f"""
📍 {posicion} ◀ TU POSICIÓN
"""

    print(mapa)

    input("\nPulsa ENTER para cerrar el mapa...")

# ===========================
# LISTA DE OBJETOS
# ===========================

def lista_objetos():

    return {

        # -------------------------
        # COMIDA
        # -------------------------

        "Lata de comida":

            Objeto(
                "Lata de comida",
                "comida",
                1,
                "Una lata que todavía parece segura.",
                efecto=comer_lata,
                apilable=True,
                cantidad=1,
                usos=2
            ),

        "Botella de agua":

            Objeto(
                "Botella de agua",
                "agua",
                1,
                "Agua potable.",
                efecto=beber_agua,
                apilable=True,
                cantidad=1,
                usos=3

            ),

        "Botiquín":

            Objeto(
                "Botiquín",
                "medicina",
                2,
                "Material médico básico.",
                apilable=True,
                efecto=curar
            ),

        # -------------------------
        # ARMAS
        # -------------------------

        "Cuchillo":

            Objeto(
                nombre="Cuchillo",
                tipo="arma",
                peso=1,
                descripcion="Un cuchillo de supervivencia.",
                daño=20,
                apilable=False,
                durabilidad=100,
                desgaste=10,
                accion_principal="Equipar"
            ),

        "Pistola":

            Objeto(
                nombre="Pistola",
                tipo="arma",
                peso=2,
                descripcion="Una pistola de 9 mm.",
                daño=35,
                apilable=False,
                durabilidad=100,
                desgaste=15,
                atasco=10,
                accion_principal="Equipar"
            ),

        # -------------------------
        # MUNICIÓN
        # -------------------------

        "Caja de munición":

            Objeto(
                nombre="Caja de munición",
                tipo="municion",
                peso=1,
                descripcion="Una caja con 6 balas.",
                cantidad=1,
                usos=1,
                accion_principal="Abrir"
            ),

        # -------------------------
        # UTILIDAD
        # -------------------------

        "Herramientas":

            Objeto(
                nombre="Herramientas",
                tipo="utilidad",
                peso=3,
                descripcion="Una caja de herramientas para reparar cosas.",
                apilable=True,
                cantidad=1,
                usos=4,
                accion_principal="Reparar"
            ),

        "Linterna":

            Objeto(
                nombre="Linterna",
                tipo="utilidad",
                peso=1,
                apilable=False,
                reparable=True,
                descripcion="Una linterna para explorar lugares oscuros.",
                accion_principal="Usar"
            ),

        "Pilas":

            Objeto(
                nombre="Pilas",
                tipo="utilidad",
                peso=1,
                descripcion="Pilas nuevas para dispositivos.",
                apilable=True,
                cantidad=1,
                usos=4,
                reparable=False,
                accion_principal="Recargar"
            ),

        # -------------------------
        # OBJETOS DE HISTORIA
        # -------------------------

        "Radio":

            Objeto(
                nombre="Radio",
                tipo="historia",
                peso=2,
                descripcion="Una radio portátil que puede captar señales.",
                apilable=False,
                durabilidad=100,
                desgaste=5,
                reparable=True,
                accion_principal="Usar"
            ),

        "Mapa":

            Objeto(
                nombre="Mapa",
                tipo="historia",
                peso=1,
                descripcion="Un mapa de la ciudad.",
                apilable=False,
                durabilidad=100,
                desgaste=7,
                reparable=False,
                accion_principal="Consultar"
            )
    }