import sys


def comprobar_final(estado):

    if estado["vida"] <= 0:

        print("\nHas muerto.")
        print("FINAL 1 - Fin del camino.")
        sys.exit()

    if estado["hambre"] >= 100:

        print("\nMuertes de hambre.")
        print("FINAL 2 - Sin alimentos.")
        sys.exit()

    if estado["sed"] >= 100:

        print("\nNo encuentras agua.")
        print("FINAL 3 - La sed pudo contigo.")
        sys.exit()

    if estado["moral"] <= 0:

        print("\nPierdes completamente la esperanza.")
        print("FINAL 4 - Rendición.")
        sys.exit()

    if len(estado["companeros"]) >= 3:

        print("\nHabéis construido un nuevo refugio.")
        print("FINAL 5 - Nuevo comienzo.")
        sys.exit()