from enemigo import Enemigo

import random


def enemigo_aleatorio():

    enemigos = crear_enemigos()

    lista = []

    for enemigo in enemigos.values():

        lista.extend(
            [enemigo] * enemigo.probabilidad
        )


    return random.choice(lista)



def crear_enemigos():


    return {


        "infectado": Enemigo(
            "Infectado",
            40,
            10,
            2,
            20,
            probabilidad=20,
            zonas=None
        ),

        "tambaleante": Enemigo(
            "Infectado tambaleante",
            35,
            10,
            2,
            15,
            probabilidad=15,
            zonas=["Bosque",
                   "Centro Ciudad",
                   "Gasolinera",
                   "Hospital",
                   "Laboratorio",
                   "Supermercado"]
        ),

        "perro": Enemigo(
            "Perro infectado",
            20,
            6,
            2,
            8,
            probabilidad=30,
            zonas=None
        ),

        "lobo": Enemigo(
            "Lobo infectado",
            25,
            7,
            2,
            12,
            probabilidad=25,
            zonas=["Bosque",
                   "Camping",
                   "Montaña",
                   "Cueva Montaña"
                   "Torre Radio"]
        ),

        "gato": Enemigo(
            "Gato infectado",
            15,
            5,
            2,
            5,
            probabilidad=35,
            zonas=None
        ),


        "corredor": Enemigo(
            "Infectado corredor",
            55,
            15,
            3,
            25,
            probabilidad=20,
            zonas=None
        ),


        "bruto": Enemigo(
            "Infectado bruto",
            90,
            18,
            6,
            40,
            probabilidad=4,
            zonas=None
        ),

        "experimento": Enemigo(
            "Experimento fallido",
            80,
            22,
            7,
            80,
            probabilidad=2,
            zonas=["Laboratorio"]
        ),


        "saqueador": Enemigo(
            "Saqueador",
            70,
            20,
            5,
            70,
            probabilidad=10,
            zonas=["Centro Ciudad",
                   "Comisaria",
                   "Supermercado",
                   "Gasolinera",
                   "Bar",
                   "Desguace",
                   "Camping"]
        ),

        "vagabundo": Enemigo(
            "Vagabundo",
            50,
            10,
            1,
            35,
            probabilidad=10,
            zonas=["Centro Ciudad",
                   "Comisaria",
                   "Hospital",
                   "Supermercado",
                   "Gasolinera",
                   "Iglesia"
                   "Cueva montaña"
                   "Camping"]
        )

    }