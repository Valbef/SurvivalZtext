import sys
from efectos import write, writefast

def comprobar_final(estado):

    if estado["vida"] <= 0:

        print("\nHas muerto.")
        write("FINAL 1 - Fin del camino.")
        sys.exit()

    if estado["hambre"] >= 100:

        print("\nMueres de hambre.")
        write("FINAL 2 - Sin alimentos.")
        sys.exit()

    if estado["sed"] >= 100:

        print("\nNo encuentras agua.")
        write("FINAL 3 - La sed pudo contigo.")
        sys.exit()

    if estado["moral"] <= 0:

        writefast("\nPierdes completamente la esperanza.")
        write("FINAL 4 - Suicidio.")
        sys.exit()

    if len(estado["companeros"]) >= 3:

        print("\nHabéis construido un nuevo refugio.")
        print("FINAL 5 - Nuevo comienzo.")
        sys.exit()