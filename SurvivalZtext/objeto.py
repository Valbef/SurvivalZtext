class Objeto:

    def __init__(
            self,
            nombre,
            tipo,
            peso,
            descripcion,
            efecto=None,
            daño=0,
            durabilidad=None,
            desgaste=0,
            atasco=0,
            apilable=True,
            cantidad=1,
            usos=None,
            reparable=False,
            accion_principal="Usar"
    ):

        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso
        self.descripcion = descripcion
        self.reparable = reparable
        self.accion_principal = accion_principal


        self.efecto = efecto

        # Estadísticas de armas
        self.daño = daño
        self.durabilidad = durabilidad
        self.desgaste = desgaste
        self.atasco = atasco

        #Objetos consumibles
        self.cantidad = cantidad
        self.usos = usos
        if usos is None:
            self.usos_restantes = None
        else:
            self.usos_restantes = cantidad * usos



    def usar(self, jugador):
        if not self.efecto:
            return False

        self.efecto(jugador)
        jugador.limitar_estadisticas()

        # Si el objeto tiene varios usos
        if self.usos is not None:
            self.usos_restantes -= 1

            self.cantidad = (self.usos_restantes + self.usos - 1) // self.usos

            return self.usos_restantes <= 0

        return True


    def desgastar(self):

        import random

        # Si el objeto no tiene durabilidad, no hacemos nada
        if self.durabilidad is None:
            return False

        # ¿Se desgasta?
        if random.randint(1, 100) <= self.desgaste:

            perdida = random.randint(1, 3)

            self.durabilidad -= perdida

            if self.durabilidad < 0:
                self.durabilidad = 0

            return self.durabilidad == 0

        return False

    def es_consumible(self):

        return self.usos is not None and self.usos > 1

    def tiene_durabilidad(self):

        return self.durabilidad is not None

    def es_reparable(self):

        return self.reparable and self.tiene_durabilidad()

    def es_arma(self):

        return self.tipo == "arma"

    def es_municion(self):

        return self.tipo == "municion"

    def es_historia(self):

        return self.tipo == "historia"

    def es_utilidad(self):

        return self.tipo == "utilidad"

    def es_comida(self):

        return self.nombre == "Lata de comida"

    def es_agua(self):

        return self.nombre == "Botella de agua"

    def es_tabaco(self):

        return self.nombre == "Caja de cigarrillos"

    def estado(self):

        if self.durabilidad is None:
            return ""

        if self.durabilidad >= 90:
            return "Como nuevo"

        elif self.durabilidad >= 70:
            return "Buen estado"

        elif self.durabilidad >= 50:
            return "Usado"

        elif self.durabilidad >= 25:
            return "Dañado"

        elif self.durabilidad > 0:
            return "Muy deteriorado"

        else:
            return "Roto"


    def datos(self):

        return {

            "nombre": self.nombre,
            "tipo": self.tipo,
            "peso": self.peso,
            "descripcion": self.descripcion,
            "daño": self.daño,
            "durabilidad": self.durabilidad,
            "desgaste": self.desgaste,
            "atasco": self.atasco,
            "cantidad": self.cantidad,
            "usos": self.usos,
            "usos_restantes": self.usos_restantes

        }