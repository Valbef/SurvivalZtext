import json
import os


CARPETA = "partidas"



def guardar(nombre, datos):

    if not os.path.exists(CARPETA):

        os.makedirs(CARPETA)


    ruta = f"{CARPETA}/{nombre}.json"


    with open(ruta,"w",encoding="utf8") as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )



def cargar(nombre):

    ruta = f"{CARPETA}/{nombre}.json"


    if not os.path.exists(ruta):

        return None


    with open(ruta,"r",encoding="utf8") as archivo:

        return json.load(archivo)



def partidas():

    if not os.path.exists(CARPETA):

        return []


    return [
        archivo[:-5]
        for archivo in os.listdir(CARPETA)
        if archivo.endswith(".json")
    ]