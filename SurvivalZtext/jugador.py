from collections import defaultdict
from objeto import Objeto

def barra(valor, maximo=100, longitud=20):
    valor = max(0, min(valor, maximo))

    llenos = int((valor / maximo) * longitud)

    vacios = longitud - llenos

    return "█" * llenos + "░" * vacios

class Jugador:


    def __init__(self,nombre):

        self.nombre = nombre
        self.nivel = 1
        self.experiencia = 0
        self.municion = 6
        self.defendiendo = False
        self.vida = 100
        self.hambre = 0
        self.sed = 0
        self.moral = 100

        self.dia = 1
        self.hora = 8
        self.clima = "Soleado"
        self.localizacion="Refugio"
        self.inventario=[]
        self.almacen = []

        self.capacidad_base = 25
        self.mochila = None

        self.companeros=[]

    def comprobar_nivel(self):

        necesario = self.nivel * 100

        if self.experiencia >= necesario:
            self.nivel += 1

            self.experiencia = 0

            self.vida += 20

            print(
                "\n🎉 Has subido al nivel",
                self.nivel
            )





    def avanzar_tiempo(self,horas):
        import random


        self.hora += horas


        while self.hora >= 24:

            self.hora -= 24

            self.dia += 1

            print(f"\n🌅 Comienza el día {self.dia}")

            self.consumir_diario()


        self.hambre += horas * 2

        self.sed += horas * 3


        self.control_supervivencia()
        self.limitar_estadisticas()

        if random.randint(1, 5) == 1:
            self.clima = random.choice(
                [
                    "Soleado",
                    "Lluvia",
                    "Tormenta",
                    "Niebla"
                ]
            )

    def control_supervivencia(self):

        self.hambre = min(self.hambre, 100)
        self.sed = min(self.sed, 100)

        if self.hambre >= 80:

            daño = (self.hambre - 79) // 5

            self.vida -= daño

            print(
                f"\n🍖 El hambre te debilita (-{daño} vida)."
            )

            if self.hambre >= 100:
                self.moral -= 8

                print(
                    "\n😞 Estás completamente hambriento."
                )

                print(
                    "🧠 Has perdido 8 de moral."
                )

            input("\nPulsa ENTER para continuar...")

        if self.sed >= 80:

            daño = (self.sed - 79) // 4

            self.vida -= daño

            print(
                f"\n💧 La sed te debilita (-{daño} vida)."
            )

            if self.sed >= 100:
                self.moral -= 10

                print(
                    "\n😞 Estás completamente deshidratado."
                )

                print(
                    "🧠 Has perdido 10 de moral."
                )

            input("\nPulsa ENTER para continuar...")

        if self.vida < 0:
            self.vida = 0

        self.limitar_estadisticas()

    def limitar_estadisticas(self):

        self.vida = max(0, min(100, self.vida))
        self.moral = max(0, min(100, self.moral))
        self.hambre = max(0, min(100, self.hambre))
        self.sed = max(0, min(100, self.sed))

    def estado(self):


        print("\n==========================")

        print(self.nombre)

        print("==========================")

        print(f"❤️ Vida     [{barra(self.vida)}] {self.vida}/100")
        print(f"🍖 Hambre   [{barra(self.hambre)}] {self.hambre}/100")
        print(f"💧 Sed      [{barra(self.sed)}] {self.sed}/100")
        print(f"😊 Moral    [{barra(self.moral)}] {self.moral}/100")
        print("---")
        print(f"📅 Día {self.dia}")
        print(f"⏰ Hora {self.hora}:00")
        print(f"🌦️ Clima: {self.clima}")
        print(f" Munición: {self.municion}")
        print("🎒 Inventario:")
        print(
            f"⚖️ Peso: "
            f"{self.peso_total()} / "
            f"{self.capacidad_peso()} kg"
        )

        grupos = self.inventario_agrupado()

        if not grupos:

            print("- Vacío")

        else:

            for nombre, objetos in grupos.items():

                cantidad = sum(
                    objeto.cantidad
                    for objeto in objetos
                )

                primero = objetos[0]

                if primero.es_consumible():

                    usos_totales = sum(
                        objeto.usos_restantes
                        for objeto in objetos
                    )

                    print(
                        f"- {nombre} x{cantidad} : "
                        f"{usos_totales} usos"
                    )

                else:

                    print(
                        f"- {nombre} x{cantidad}"
                    )

    def consumir_diario(self):

        comida = None
        agua = None

        for objeto in self.inventario:

            if objeto.nombre == "Lata de comida" and comida is None:
                comida = objeto

            elif objeto.nombre == "Botella de agua" and agua is None:
                agua = objeto

        # ---------- COMIDA ----------

        if comida:

            comida.usar(self)

            print("\n🍖 Has comido una ración.")

            if comida.usos_restantes <= 0:
                self.inventario.remove(comida)

                print("La lata se ha terminado.")

        else:

            print("\n⚠️ No tienes comida.")
            self.vida -= 8
            self.moral -= 10

        # ---------- AGUA ----------

        if agua:

            agua.usar(self)

            print("💧 Has bebido agua.")

            if agua.usos_restantes <= 0:
                self.inventario.remove(agua)

                print("La botella está vacía.")

        else:

            print("⚠️ No tienes agua.")
            self.vida -= 12
            self.moral -= 15

        self.limitar_estadisticas()



    def datos_guardado(self):


        return {

            "nombre":self.nombre,

            "vida":self.vida,

            "hambre":self.hambre,

            "sed":self.sed,

            "moral":self.moral,

            "dia":self.dia,

            "hora":self.hora,

            "clima":self.clima,

            "localizacion":self.localizacion,

            "municion": self.municion,

            "inventario":
                [
                    objeto.datos()
                    for objeto in self.inventario
                ],

            "almacen":
                [
                    objeto.datos()
                    for objeto in self.almacen
                ],

            "companeros": self.companeros

        }




    def cargar_datos(self, datos):

        self.nombre = datos["nombre"]

        self.vida = datos["vida"]

        self.hambre = datos["hambre"]

        self.sed = datos["sed"]

        self.moral = datos["moral"]

        self.dia = datos["dia"]

        self.hora = datos["hora"]

        self.clima = datos.get(
            "clima",
            "Soleado"
        )

        self.localizacion = datos["localizacion"]

        self.inventario = []

        for datos_objeto in datos.get("inventario", []):
            objeto = Objeto(
                nombre=datos_objeto["nombre"],
                tipo=datos_objeto["tipo"],
                peso=datos_objeto["peso"],
                descripcion=datos_objeto["descripcion"],
                daño=datos_objeto.get("daño", 0),
                durabilidad=datos_objeto.get("durabilidad"),
                desgaste=datos_objeto.get("desgaste", 0),
                atasco=datos_objeto.get("atasco", 0),
                apilable=datos_objeto.get("apilable", True),
                cantidad=datos_objeto.get("cantidad", 1),
                usos=datos_objeto.get("usos"),
                reparable=datos_objeto.get("reparable", False),
                accion_principal=datos_objeto.get(
                    "accion_principal",
                    "Usar"
                )
            )

            objeto.usos_restantes = datos_objeto.get(
                "usos_restantes",
                objeto.usos_restantes
            )

            self.inventario.append(objeto)

        self.almacen = []

        for datos_objeto in datos.get("almacen", []):
            objeto = Objeto(
                nombre=datos_objeto["nombre"],
                tipo=datos_objeto["tipo"],
                peso=datos_objeto["peso"],
                descripcion=datos_objeto["descripcion"],
                daño=datos_objeto.get("daño", 0),
                durabilidad=datos_objeto.get("durabilidad"),
                desgaste=datos_objeto.get("desgaste", 0),
                atasco=datos_objeto.get("atasco", 0),
                apilable=datos_objeto.get("apilable", True),
                cantidad=datos_objeto.get("cantidad", 1),
                usos=datos_objeto.get("usos"),
                reparable=datos_objeto.get("reparable", False),
                accion_principal=datos_objeto.get(
                    "accion_principal",
                    "Usar"
                )
            )

            objeto.usos_restantes = datos_objeto.get(
                "usos_restantes",
                objeto.usos_restantes
            )

            self.almacen.append(objeto)

        self.companeros = datos.get(
            "companeros",
            []
        )

        self.municion = datos.get(
            "municion",
            0
        )

    def tiene_pistola(self):

        for objeto in self.inventario:

            if objeto.nombre == "Pistola":
                return objeto

        return None

    def arma_cuerpo_a_cuerpo(self):

        for objeto in self.inventario:

            if objeto.tipo == "arma" and objeto.nombre != "Pistola":
                return objeto

        return None

    def peso_total(self):

        return sum(
            objeto.peso * objeto.cantidad
            for objeto in self.inventario
        )

    def peso_almacen(self):

        return sum(
            objeto.peso * objeto.cantidad
            for objeto in self.almacen
        )

    def capacidad_peso(self):

        capacidad = self.capacidad_base

        if self.mochila is not None:
            capacidad += self.mochila.capacidad

        return capacidad

    def puede_viajar(self):
        return self.peso_total() <= self.capacidad_peso()



    def inventario_agrupado(self):

        grupos = defaultdict(list)

        for objeto in self.inventario:
            grupos[objeto.nombre].append(objeto)

        # Unificar cantidades del mismo objeto
        for nombre, objetos in grupos.items():

            if len(objetos) > 1:

                principal = objetos[0]

                for objeto in objetos[1:]:

                    principal.cantidad += objeto.cantidad

                    if principal.usos_restantes is not None:
                        principal.usos_restantes += (
                            objeto.usos_restantes
                        )

                grupos[nombre] = [principal]

        return grupos

    def inventario_agrupado_almacen(self):

        grupos = defaultdict(list)

        for objeto in self.almacen:
            grupos[objeto.nombre].append(objeto)

        # Unificar cantidades del mismo objeto
        for nombre, objetos in grupos.items():

            if len(objetos) > 1:

                principal = objetos[0]

                for objeto in objetos[1:]:

                    principal.cantidad += objeto.cantidad

                    if principal.usos_restantes is not None:
                        principal.usos_restantes += (
                            objeto.usos_restantes
                        )

                grupos[nombre] = [principal]

        return grupos


