from localizacion import Localizacion


class Mapa:


    def __init__(self):

        self.lugares = {}

        self.crear_mapa()


    def crear_mapa(self):


        nombres = [

            "Refugio",
            "Bosque",
            "Cabaña",
            "Gasolinera",
            "Centro Ciudad",
            "Comisaría",
            "Hospital",
            "Laboratorio",
            "Centro Comercial",
            "Escuela",
            "Supermercado",
            "Estación Bomberos",
            "Camping",
            "Torre Radio"

        ]


        for nombre in nombres:

            self.lugares[nombre] = Localizacion(
                nombre,
                f"Zona: {nombre}"
            )


        conexiones = [

            ("Refugio","Bosque"),
            ("Bosque","Cabaña"),
            ("Bosque","Gasolinera"),

            ("Gasolinera","Centro Ciudad"),

            ("Centro Ciudad","Comisaría"),
            ("Centro Ciudad","Centro Comercial"),

            ("Comisaría","Hospital"),

            ("Hospital","Laboratorio"),

            ("Centro Comercial","Supermercado"),

            ("Centro Ciudad","Escuela"),

            ("Escuela","Estación Bomberos"),

            ("Camping","Bosque"),

            ("Camping","Torre Radio")

        ]


        for a,b in conexiones:

            self.lugares[a].conectar(b)
            self.lugares[b].conectar(a)



    def obtener(self,nombre):

        return self.lugares[nombre]