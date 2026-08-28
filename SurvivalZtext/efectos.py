import time
#import sys


def write(texto, velocidad=0.07):

    for letra in texto:

        print(letra, end="", flush=True)

        time.sleep(velocidad)

    print()

def writefast(texto, velocidad=0.03):

    for letra in texto:

        print(letra, end="", flush=True)

        time.sleep(velocidad)

    print()

def pausa():

    input("\n Pulsa ENTER para continuar...")