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
            "Taller Mecanico",
            "Centro Ciudad",
            "Bar",
            "Iglesia",
            "Comisaría",
            "Hospital",
            "Laboratorio",
            "Centro Comercial",
            "Escuela",
            "Supermercado",
            "Estación Bomberos",
            "Camping",
            "Torre Radio",
            "Desguace",
            "Montaña",
            "Cueva Montaña"

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
            ("Gasolinera","Taller Mecanico"),
            ("Taller Mecanico", "Desguace"),

            ("Centro Ciudad","Comisaría"),
            ("Centro Ciudad","Centro Comercial"),
            ("Centro Ciudad", "Bar"),
            ("Bar","Centro Comercial"),

            ("Comisaría","Hospital"),

            ("Hospital","Laboratorio"),

            ("Centro Comercial","Supermercado"),
            ("Centro Ciudad","Escuela"),
            ("Centro Ciudad","Iglesia"),

            ("Escuela","Estación Bomberos"),

            ("Camping","Bosque"),
            ("Camping","Montaña"),

            ("Montaña","Torre Radio"),
            ("Montaña","Cueva Montaña"),

            ("Torre Radio","Cueva Montaña")

        ]


        for a,b in conexiones:

            self.lugares[a].conectar(b)
            self.lugares[b].conectar(a)



    def obtener(self,nombre):

        return self.lugares[nombre]