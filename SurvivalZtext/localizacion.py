class Localizacion:


    def __init__(self, nombre, descripcion):

        self.nombre = nombre

        self.descripcion = descripcion

        self.conexiones = []


    def conectar(self, lugar):

        self.conexiones.append(lugar)


    def mostrar(self):

        print("\n📍", self.nombre)

        print(self.descripcion)

        print("\nPuedes ir a:")

        for lugar in self.conexiones:

            print("-", lugar)