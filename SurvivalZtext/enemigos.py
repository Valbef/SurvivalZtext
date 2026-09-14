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
            probabilidad=35,
            zonas=None
        ),

        "perro": Enemigo(
            "Perro infectado",
            20,
            6,
            2,
            10,
            probabilidad=40,
            zonas=None
        ),

        "lobo": Enemigo(
            "Lobo infectado",
            25,
            7,
            2,
            12,
            probabilidad=40,
            zonas=["Bosque",
                   "Camping"]
        ),

        "gato": Enemigo(
            "Gato infectado",
            15,
            5,
            2,
            10,
            probabilidad=40,
            zonas=None
        ),



        "corredor": Enemigo(
            "Infectado corredor",
            55,
            15,
            3,
            35,
            probabilidad=20,
            zonas=None
        ),



        "bruto": Enemigo(
            "Infectado bruto",
            90,
            20,
            6,
            100,
            probabilidad=5,
            zonas=None
        ),



        "saqueador": Enemigo(
            "Saqueador",
            80,
            20,
            5,
            75,
            probabilidad=10,
            zonas=["Centro Ciudad",
                   "Comisaria",
                   "Supermercado",
                   "Gasolinera",
                   "Camping"]
        ),

        "vagabundo": Enemigo(
            "Vagabundo",
            50,
            10,
            1,
            25,
            probabilidad=10,
            zonas=["Centro Ciudad",
                   "Comisaria",
                   "Supermercado",
                   "Gasolinera",
                   "Camping"]
        )

    }