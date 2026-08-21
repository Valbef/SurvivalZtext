import random


class Enemigo:


    def __init__(
            self,
            nombre,
            vida,
            daño,
            defensa,
            experiencia,
            probabilidad=10
    ):

        self.nombre = nombre
        self.vida = vida
        self.daño = daño
        self.defensa = defensa
        self.experiencia = experiencia
        self.probabilidad = probabilidad



    def atacar(self):

        variacion = random.randint(
            self.daño - 3,
            self.daño + 3
        )

        if variacion < 0:
            variacion = 0

        return variacion



    def vivo(self):

        return self.vida > 0