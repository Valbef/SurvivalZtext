
escenas={
    "bosque_cabana": {

        "texto": """
Encuentras una vieja cabaña oculta entre los árboles.

La puerta está entreabierta.
Parece que alguien vivió aquí recientemente.
""",

        "opciones": {

            "1": {
                "texto": "Entrar y registrar",
                "destino": None,
                "objeto": "Herramientas",
                "moral": 2
            },

            "2": {
                "texto": "Alejarte",
                "destino": None,
                "moral": -2
            }
        }
    },


    "casa_abandonada": {

        "texto": """
Encuentras una pequeña casa abandonada.

Dentro todavía quedan algunos suministros.
""",

        "opciones": {

            "1": {
                "texto": "Buscar comida",
                "destino": None,
                "objeto": "Lata de comida",
                "moral": 2
            },

            "2": {
                "texto": "Salir",
                "destino": None,
                "moral": -2
            }
        }
    },


    "gasolinera_superviviente": {

        "texto": """
Una persona aparece detrás de los surtidores.

Parece un superviviente, pero no sabes si confiar.
""",

        "opciones": {

            "1": {
                "texto": "Ayudarle",
                "destino": None,
                "moral": 10
            },

            "2": {
                "texto": "Ignorarlo",
                "destino": None,
                "moral": -3
            }
        }
    },


    "gasolinera_recursos": {

        "texto": """
Registras el almacén de la gasolinera.

Encuentras herramientas y agua.
""",

        "opciones": {

            "1": {
                "texto": "Registrar almacén",
                "destino": None,
                "objeto": "Herramientas",
                "objeto": "Botella de agua",
                "moral": 3
            },

            "2": {
                "texto": "Marcharte",
                "destino": None,
                "moral": -2
            }
        }
    },


    "ciudad_infectados": {

        "texto": """
Los edificios abandonados esconden peligros.

Un grupo de infectados aparece en la calle.
""",

        "opciones": {

            "1": {
                "texto": "Huir",
                "destino": None,
                "vida": -15
            },

            "2": {
                "texto": "Buscar una ruta segura",
                "destino": None,
                "moral": -5
            }
        }
    },


    "ciudad_coche": {

        "texto": """
Encuentras un coche abandonado.

Todavía hay cosas útiles dentro.
""",

        "opciones": {

            "1": {
                "texto": "Abrir el maletero",
                "destino": None,
                "objeto": "Botiquín",
                "moral": 2
            },

            "2": {
                "texto": "Continuar",
                "destino": None,
                "moral": -2
            }
        }
    },


    "comisaria_armas": {

        "texto": """
Llegas a la zona de armamento de la comisaría.

Las taquillas siguen cerradas.
""",

        "opciones": {

            "1": {
                "texto": "Forzar una taquilla",
                "destino": None,
                "objeto": "Caja de munición",
                "moral": 2
            },

            "2": {
                "texto": "Salir",
                "destino": None,
                "moral": -2
            }
        }
    },


    "hospital_paciente": {

        "texto": """
Encuentras un médico encerrado en una habitación.

Necesita ayuda.
""",

        "opciones": {

            "1": {
                "texto": "Ayudarlo",
                "destino": None,
                "moral": 10
            },

            "2": {
                "texto": "Continuar",
                "destino": None,
                "moral": -3
            }
        }
    },


    "laboratorio_investigacion": {

        "texto": """
Encuentras documentos sobre el origen de la infección.

Quizá esta información sea importante.
""",

        "opciones": {

            "1": {
                "texto": "Guardar los documentos",
                "destino": None,
                "moral": 15
            }
        }
    },


    "centro_comercial": {

        "texto": """
Los almacenes del centro comercial están intactos.
""",

        "opciones": {

            "1": {
                "texto": "Buscar suministros",
                "destino": None,
                "objeto": "Lata de comida",
                "objeto": "Botella de agua",
                "moral": 2
            },

            "2": {
                "texto": "Marcharte",
                "destino": None,
                "moral": -2
            }
        }
    },


    "escuela": {

        "texto": """
Encuentras una escuela abandonada.

Algunas mochilas siguen en las aulas.
""",

        "opciones": {

            "1": {
                "texto": "Registrar mochilas",
                "destino": None,
                "objeto": "Botella de agua",
                "moral": 2
            }
        }
    },


    "bomberos": {

        "texto": """
La estación de bomberos no está vacía.

Todavía quedan herramientas útiles.
""",

        "opciones": {

            "1": {
                "texto": "Buscar equipo",
                "destino": None,
                "objeto": "Herramientas",
                "moral": 2
            }
        }
    },


    "camping_recursos": {

        "texto": """
Encuentras un antiguo campamento.

Alguien dejó suministros atrás.
""",

        "opciones": {

            "1": {
                "texto": "Registrar tiendas",
                "destino": None,
                "objeto": "Lata de comida",
                "moral": 2
            }
        }
    },


    "torre_radio": {

        "texto": """
Subes a la torre de radio.

Una señal débil llega desde algún lugar.
""",

        "opciones": {

            "1": {
                "texto": "Intentar comunicarse",
                "destino": None,
                "objeto": "Radio",
                "moral": 1
            },

            "2": {
                "texto": "Bajar",
                "destino": None,
                "moral": -2
            }
        }
    },
}
ESCENAS_POR_ZONA = {

    "Bosque": [
        "bosque_superviviente",
        "bosque_cabana"
    ],

    "Cabaña": [
        "casa_abandonada"
    ],

    "Gasolinera": [
        "gasolinera_superviviente",
        "gasolinera_recursos"
    ],

    "Centro Ciudad": [
        "ciudad_infectados",
        "ciudad_coche"
    ],

    "Comisaría": [
        "comisaria_armas"
    ],

    "Hospital": [
        "hospital_paciente",
        "hospital_suministros"
    ],

    "Laboratorio": [
        "laboratorio_investigacion"
    ],

    "Centro Comercial": [
        "centro_comercial"
    ],

    "Escuela": [
        "escuela"
    ],

    "Estación Bomberos": [
        "bomberos"
    ],

    "Camping": [
        "camping_recursos"
    ],

    "Torre Radio": [
        "torre_radio"
    ]
}