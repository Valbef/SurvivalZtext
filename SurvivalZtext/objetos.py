from objeto import Objeto
from efectos import write, writefast


# ===========================
# EFECTOS DE LOS OBJETOS
# ===========================

def comer_lata(jugador):

    jugador.hambre -= 25
    jugador.vida += 10
    jugador.moral += 3

    if jugador.vida > 100:
        jugador.vida = 100


def beber_agua(jugador):

    jugador.sed -= 40
    jugador.vida += 3
    jugador.moral += 2

    if jugador.vida > 100:
        jugador.vida = 100

def comer_carne_cruda(jugador):

    jugador.hambre -= 10
    jugador.vida += 5
    jugador.moral -= 5

    write("Lo importante es sobrevivir...")

    if jugador.vida > 100:
        jugador.vida = 100

def comer_carne_infectada_cruda(jugador):

    jugador.hambre -= 5
    jugador.vida -= 15
    jugador.moral -= 15

    write("¿En serio te has comido esto?..")
    write("...")
    write("...")
    write("Te encuentras mal, tu salud y tu moral bajan...")

    if jugador.vida > 100:
        jugador.vida = 100

def comer_carne_cocinada(jugador):
    jugador.hambre -= 35
    jugador.vida += 15
    jugador.moral += 5

    write("Parece que sabe mejor cocinada...")

    if jugador.vida > 100:
        jugador.vida = 100


def comer_carne_infectada_cocinada(jugador):
    jugador.hambre -= 15
    jugador.vida += 2
    jugador.moral -= 10

    write("¿En que estabas pensando?")
    write("...")
    write("Esto sabe realmente mal...")
    write("...")
    write("Por lo menos no te duele el estomago.")


    if jugador.vida > 100:
        jugador.vida = 100



def curar(jugador):

    jugador.vida += 40

    if jugador.vida > 100:
        jugador.vida = 100


def fumar_cigarrillos(jugador):

    # =====================================
    # BUSCAR CAJA DE CERILLAS
    # =====================================

    caja_cerillas = None

    for objeto in jugador.inventario:

        if (
            objeto.nombre == "Caja de cerillas"
            and objeto.usos_restantes > 0
        ):
            caja_cerillas = objeto
            break

    # =====================================
    # COMPROBAR CERILLAS
    # =====================================

    if caja_cerillas is None:

        print(
            "\n❌ No tienes cerillas para encender el cigarrillo."
        )

        input(
            "\nPulsa ENTER para continuar..."
        )

        return False

    # =====================================
    # CONSUMIR 1 CERILLA
    # =====================================

    caja_cerillas.usos_restantes -= 1

    caja_cerillas.cantidad = (
        caja_cerillas.usos_restantes
        + caja_cerillas.usos
        - 1
    ) // caja_cerillas.usos

    if caja_cerillas.usos_restantes <= 0:

        jugador.inventario.remove(
            caja_cerillas
        )

        print(
            "\n🔥 Has usado la última cerilla."
        )

    # =====================================
    # EFECTO DEL CIGARRILLO
    # =====================================

    jugador.sed += 2
    jugador.vida += 3
    jugador.moral += 4

    if jugador.vida > 100:
        jugador.vida = 100

    print(
        "\n🚬 Has fumado un cigarrillo."
    )

    return True


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
    kit = None

    for obj in jugador.inventario:

        if obj.nombre == "Herramientas":
            herramientas = obj
            break

        elif obj.nombre == "Kit de reparación":
            kit = obj

    # =========================
    # COMPROBAR RECURSO
    # =========================

    if herramientas is None and kit is None:

        print("\n❌ No tienes herramientas para reparar.")

        return

    # =========================
    # COMPROBAR OBJETO
    # =========================

    if objeto.durabilidad is None:

        print("\n❌ Este objeto no se puede reparar.")

        return

    if objeto.durabilidad >= 100:

        print("\n🔧 El objeto ya está en perfecto estado.")

        return

    # =========================
    # CAJA DE HERRAMIENTAS
    # =========================

    if herramientas is not None:

        reparacion = random.randint(10, 30)

        herramientas.usar(jugador)

        print(
            f"\n🔧 Has reparado {objeto.nombre} "
            f"+{reparacion} durabilidad."
        )

        if herramientas.usos_restantes <= 0:

            jugador.inventario.remove(herramientas)

            print(
                "\n🔧 La caja de herramientas se ha agotado."
            )

    # =========================
    # KIT DE REPARACIÓN
    # =========================

    else:

        reparacion = random.randint(5, 15)

        kit.cantidad -= 1

        kit.usos_restantes -= 1

        print(
            f"\n🧰 Has usado un Kit de reparación."
        )

        print(
            f"🔧 Has reparado {objeto.nombre} "
            f"+{reparacion} durabilidad."
        )

        if kit.cantidad <= 0:

            jugador.inventario.remove(kit)

            print(
                "\n🧰 Te has quedado sin Kits de reparación."
            )

    # =========================
    # APLICAR REPARACIÓN
    # =========================

    objeto.durabilidad += reparacion

    if objeto.durabilidad > 100:

        objeto.durabilidad = 100

def reparar_con_kit(jugador, objeto):

    import random

    reparacion = random.randint(5, 15)

    objeto.durabilidad += reparacion

    if objeto.durabilidad > 100:
        objeto.durabilidad = 100

    print(
        f"\n🔧 Has reparado {objeto.nombre} "
        f"+{reparacion} durabilidad."
    )

def escuchar_radio(jugador):

    pilas = None

    for objeto in jugador.inventario:

        if objeto.nombre == "Pilas":
            pilas = objeto
            break

    if pilas is None or pilas.usos_restantes <= 0:

        print("\n🔋 La radio no tiene pilas.")

        return False

    # Consumir una pila
    pilas.usos_restantes -= 1

    jugador.moral += 30

    if jugador.moral > 100:
        jugador.moral = 100

    print("\n📻 Escuchas la radio.")

    print("🔋 Has gastado 1 pila.")

    if pilas.usos_restantes <= 0:

        print("\n🔋 Te has quedado sin pilas.")

        jugador.inventario.remove(pilas)

    return True



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
        # COMIDA (consumibles)
        # -------------------------

        "Lata de comida":

            Objeto(
                "Lata de comida",
                "comida",
                2,
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
                2,
                "Agua potable.",
                efecto=beber_agua,
                apilable=True,
                cantidad=1,
                usos=3

            ),

        "Carne infectada cruda":

            Objeto(
                "Carne infectada cruda",
                "comida",
                1,
                "Carne infectada cruda, esto huele horrible...",
                efecto=comer_carne_infectada_cruda,
                apilable=True,
                cantidad=1,
                usos=1
            ),

        "Carne cruda":

            Objeto(
                "Carne cruda",
                "comida",
                1,
                "Carne cruda, mejor no saber mas...",
                efecto=comer_carne_cruda,
                apilable=True,
                cantidad=1,
                usos=1
            ),

        "Carne infectada cocinada":

            Objeto(
                "Carne infectada cocinada",
                "comida",
                1,
                "Carne infectada cocinada, no tiene buena pinta...",
                efecto=comer_carne_infectada_cocinada,
                apilable=True,
                cantidad=1,
                usos=1
            ),

        "Carne cocinada":

            Objeto(
                "Carne cocinada",
                "comida",
                1,
                "Carne cocinada, no estarías comiendo carne cruda, verdad?...",
                efecto=comer_carne_cocinada,
                apilable=True,
                cantidad=1,
                usos=1
            ),

        "Botiquín":

            Objeto(
                nombre="Botiquín",
                tipo="medicina",
                peso=2,
                descripcion="Material médico básico.",
                efecto=curar,
                apilable=True,
                cantidad=1,
                usos=1,
                accion_principal="Usar"
            ),

        "Caja de cigarrillos":

            Objeto(
                "Caja de cigarrillos",
                "tabaco",
                0.5,
                "Una caja de cigarillos.",
                efecto=fumar_cigarrillos,
                apilable=True,
                cantidad=1,
                usos=20
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
                reparable=True,
                apilable=False,
                durabilidad=100,
                desgaste=10,
                accion_principal="Equipar"
            ),

        "Lanza":

            Objeto(
                nombre="Lanza",
                tipo="arma",
                peso=3,
                descripcion="Una lanza improvisada fabricada con madera y metal.",
                daño=25,
                durabilidad=100,
                desgaste=15,
                reparable=True,
                apilable=False,
                cantidad=1,
                accion_principal="Equipar"
            ),

        "Pistola":

            Objeto(
                nombre="Pistola",
                tipo="arma",
                peso=2,
                descripcion="Una pistola de 9 mm.",
                daño=35,
                reparable=True,
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

        "Kit de reparación":

            Objeto(
                nombre="Kit de reparación",
                tipo="utilidad",
                peso=1,
                descripcion="Un pequeño kit para reparar objetos dañados.",
                apilable=True,
                cantidad=1,
                usos=1,
                reparable=False,
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
                peso=0.5,
                descripcion="Pilas nuevas para dispositivos.",
                apilable=True,
                cantidad=1,
                usos=4,
                reparable=False,
                accion_principal="Recargar"
            ),

        "Caja de cerillas":

            Objeto(
                nombre="Caja de cerillas",
                tipo="utilidad",
                peso=0.5,
                descripcion="Una caja con 30 cerillas.",
                apilable=True,
                cantidad=1,
                usos=30
            ),

        # -------------------------
        # MATERIALES
        # -------------------------

        "Tela":

            Objeto(
                nombre="Tela",
                tipo="material",
                peso=1,
                descripcion="Un trozo de tela útil para fabricar objetos.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Hierbas":

            Objeto(
                nombre="Hierbas",
                tipo="material",
                peso=1,
                descripcion="Hierbas medicinales de el campo.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Cuerda":

            Objeto(
                nombre="Cuerda",
                tipo="material",
                peso=1,
                descripcion="Una cuerda resistente.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Piel":

            Objeto(
                nombre="Piel",
                tipo="material",
                peso=1,
                descripcion="Piel que puede utilizarse para fabricar equipo.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Madera":

            Objeto(
                nombre="Madera",
                tipo="material",
                peso=2,
                descripcion="Madera útil para fabricar objetos.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Metal":

            Objeto(
                nombre="Metal",
                tipo="material",
                peso=2,
                descripcion="Piezas de metal recuperadas.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),

        "Componentes electronicos":

            Objeto(
                nombre="Componentes electronicos",
                tipo="material",
                peso=0.5,
                descripcion="Componentes electronicos de dispositivos.",
                apilable=True,
                cantidad=1,
                accion_principal="Usar"
            ),



        # -------------------------
        # MOCHILAS
        # -------------------------

        "Mochila pequeña":

            Objeto(
                nombre="Mochila pequeña",
                tipo="mochila",
                peso=1,
                descripcion="Una mochila pequeña que aumenta la capacidad de carga en 15 kg.",
                capacidad=15,
                apilable=False,
                accion_principal="Equipar"
            ),

        "Mochila mediana":

            Objeto(
                nombre="Mochila mediana",
                tipo="mochila",
                peso=2,
                descripcion="Una mochila mediana que aumenta la capacidad de carga en 25 kg.",
                capacidad=25,
                apilable=False,
                accion_principal="Equipar"
            ),

        "Mochila grande":

            Objeto(
                nombre="Mochila grande",
                tipo="mochila",
                peso=3,
                descripcion="Una mochila grande que aumenta la capacidad de carga en 35 kg.",
                capacidad=35,
                apilable=False,
                accion_principal="Equipar"
            ),

        # -------------------------
        # OBJETOS DE HISTORIA
        # -------------------------

        "Radio":

            Objeto(
                nombre="Radio",
                tipo="historia",
                peso=1.5,
                descripcion="Una radio portátil que puede captar señales.",
                apilable=False,
                efecto=escuchar_radio,
                durabilidad=100,
                desgaste=5,
                reparable=True,
                accion_principal="Usar"
            ),

        "Mapa":

            Objeto(
                nombre="Mapa",
                tipo="historia",
                peso=0.5,
                descripcion="Un mapa de la ciudad.",
                apilable=False,
                durabilidad=100,
                desgaste=7,
                reparable=False,
                accion_principal="Consultar"
            )
    }