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
            probabilidad=40
        ),

        "perro": Enemigo(
            "Perro infectado",
            20,
            6,
            2,
            10,
            probabilidad=30
        ),



        "corredor": Enemigo(
            "Infectado corredor",
            55,
            15,
            3,
            35,
            probabilidad=20
        ),



        "bruto": Enemigo(
            "Infectado bruto",
            100,
            25,
            8,
            100,
            probabilidad=8
        ),



        "saqueador": Enemigo(
            "Saqueador",
            80,
            20,
            5,
            75,
            probabilidad=15
        ),

        "vagabundo": Enemigo(
            "Vagabundo",
            50,
            10,
            1,
            25,
            probabilidad=10
        )

    }