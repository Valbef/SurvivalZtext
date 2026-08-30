import random
from copy import deepcopy


EVENTOS_POR_ZONA = {


    "Bosque": [

        {
            "texto": "\n📦 Encuentras una mochila entre los árboles.",
            "objeto": "Lata de comida",
            "moral": 2
        },

        {
            "texto": "\n💧 Encuentras una botella de agua junto a un campamento.",
            "objeto": "Botella de agua",
            "moral": 2
        },

        {
            "texto": "\n🐺 Un perro salvaje te ataca y se va corriendo.",
            "vida": -10,
            "moral": -10
        },

        {
            "texto": "\n🔥 Encuentras un lugar tranquilo y descansas.",
            "vida": 20,
            "moral": 15
        },

        {
            "texto": "\n🧍 Encuentras un superviviente perdido.",
            "companero": "Superviviente",
            "moral": 10
        }

    ],



    "Cabaña": [

        {
            "texto": "\n🏚️ Registras una vieja cabaña abandonada.",
            "objeto": "Herramientas"
        },

        {
            "texto": "\n📻 Encuentras una radio antigua funcionando.",
            "objeto": "Radio"
        },

        {
            "texto": "\n☠️ Un infectado estaba escondido dentro.",
            "vida": -20,
            "moral": -15
        }

    ],



    "Gasolinera": [

        {
            "texto": "\n🔧 Encuentras una caja de herramientas.",
            "objeto": "Herramientas"
        },

        {
            "texto": "\n💧 Encuentras agua almacenada.",
            "objeto": "Botella de agua",
            "moral": 2
        },

        {
            "texto": "\n💥 Un saqueador te dispara desde lejos.",
            "vida": -20,
            "moral": -15
        }

    ],



    "Centro Ciudad": [

        {
            "texto": "\n☠️ Un grupo de infectados te sorprende entre los coches, consigues escapar con algunos daños.",
            "vida": -25,
            "moral": -15
        },

        {
            "texto": "\n🔫 Encuentras munición abandonada.",
            "municion": 4,
            "moral": 2
        },

        {
            "texto": "\n📦 Registras un coche abandonado.",
            "objeto": "Botiquín",
            "moral": 2
        }

    ],



    "Comisaría": [

        {
            "texto": "\n🔫 Encuentras munición en una taquilla policial.",
            "municion": 6,
            "moral": 2
        },

        {
            "texto": "\n🗺️ Encuentras un mapa de la ciudad.",
            "objeto": "Mapa"
        },

        {
            "texto": "\n👮 Un policía infectado te sorprende, huyes con daños.",
            "vida": -20,
            "moral": -15
        }

    ],



    "Hospital": [

        {
            "texto": "\n💊 Encuentras material médico.",
            "objeto": "Botiquín"
        },

        {
            "texto": "\n🧑‍⚕️ Una enfermera superviviente te ayuda.",
            "companero": "Laura"
        },

        {
            "texto": "\n☠️ te atacan unos infectados antes de conseguir huir.",
            "vida": -30,
            "moral": -15
        }

    ],



    "Laboratorio": [

        {
            "texto": "\n🧪 Encuentras información sobre la infección.",
            "moral": 10
        },

        {
            "texto": "\n📻 Encuentras una radio vieja.",
            "objeto": "Radio"
        }

    ],



    "Centro Comercial": [

        {
            "texto": "\n🥫 Encuentras comida entre los almacenes.",
            "objeto": "Lata de comida"
        },

        {
            "texto": "\n☠️ Los ruidos atraen infectados.",
            "vida": -25,
            "moral": -10
        }

    ],



    "Escuela": [

        {
            "texto": "\n🎒 Encuentras algunos suministros.",
            "objeto": "Botella de agua",
            "moral": 2
        },

        {
            "texto": "\n🔦 Encuentras una linterna.",
            "objeto": "Linterna"
        }

    ],



    "Estación Bomberos": [

        {
            "texto": "\n🔧 Encuentras una caja de herramientas.",
            "objeto": "Herramientas"
        },

        {
            "texto": "\n🧯 El edificio parece seguro.",
            "moral": 5
        }

    ],



    "Camping": [

        {
            "texto": "\n🏕️ Encuentras un campamento abandonado.",
            "objeto": "Lata de comida",
            "moral": 2
        },

        {
            "texto": "\n💧 Encuentras algo de agua almacenada.",
            "objeto": "Botella de agua",
            "moral": 2
        }

    ],



    "Torre Radio": [

        {
            "texto": "\n📻 Encuentras una señal de radio activa.",
            "moral": 15
        },

        {
            "texto": "\n📡 Encuentras una radio, la antena está doblada pero funciona.",
            "objeto": "Radio"
        }

    ]

}



def evento_aleatorio(jugador, objetos):


    zona = jugador.localizacion


    if zona not in EVENTOS_POR_ZONA:

        return


    # Probabilidad de evento

    if random.randint(1,100) > 35:

        return


    evento = random.choice(
        EVENTOS_POR_ZONA[zona]
    )


    print(evento["texto"])



    jugador.vida += evento.get("vida",0)

    jugador.moral += evento.get("moral",0)

    jugador.hambre += evento.get("hambre",0)

    jugador.sed += evento.get("sed",0)

    jugador.municion += evento.get("municion",0)



    if "objeto" in evento:

        nombre = evento["objeto"]


        if nombre in objetos:

            jugador.inventario.append(
                deepcopy(objetos[nombre])
            )


            print(
                f"🎒 Obtienes: {nombre}"
            )



    if "companero" in evento:

        if evento["companero"] not in jugador.companeros:

            jugador.companeros.append(
                evento["companero"]
            )

    jugador.limitar_estadisticas()