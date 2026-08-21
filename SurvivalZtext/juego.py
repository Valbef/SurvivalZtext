from jugador import Jugador
from mapa import Mapa
from objetos import lista_objetos
from enemigos import crear_enemigos
from enemigos import enemigo_aleatorio
from combate import iniciar_combate
from eventos import evento_aleatorio
from saqueo import saquear
from motor_escenas import ejecutar_escena,comprobar_escena
from efectos import write, writefast
from copy import deepcopy
import random

import guardar



class Juego:


    def __init__(self):

        self.objetos = lista_objetos()

        self.jugador = None

        self.mapa = Mapa()

        self.enemigos = crear_enemigos()

    def introduccion(self):

        print("""
    =========================================================
                        SURVIVAL Z 2030
    =========================================================""")
        write("""
    Año 2030.

    Todo comenzó hace apenas una semana.

    Una extraña enfermedad apareció en varias ciudades del
    mundo. Al principio parecía una gripe especialmente
    agresiva, pero los hospitales pronto quedaron desbordados.
    
    Las carreteras quedaron bloqueadas, las comunicaciones
    dejaron de funcionar, el gobierno declaró el estado de
    emergencia y ordenó un confinamiento hasta nueva orden. 
    Nadie ha vuelto a saber nada de las autoridades.

    Ahora los supermercados están vacíos, las calles son un
    cementerio y cada superviviente lucha únicamente por seguir
    con vida un día más.
    """)

        input("\nPulsa ENTER para continuar...")

        write("""
    Has conseguido refugiarte en una pequeña casa a las
    afueras de la ciudad.

    No sabes si existen zonas seguras.
    No sabes si queda algún ejército organizado.
    No sabes cuánto tiempo podrás sobrevivir.

    Solo sabes una cosa...

    Si quieres vivir, tendrás que salir ahí fuera.
    """)
        writefast("""  =========================================================""")
        write("""                Comienza tu historia...""")
        writefast("""  =========================================================
    """)
        write("   Cuanto tiempo crees que sobrevivirás?")

        input("\nPulsa ENTER para comenzar...")



    def menu(self):

        while True:

            print("""
============================
       SURVIVAL Z
============================

1. Nueva partida
2. Cargar partida
3. Salir
""")

            opcion=input("> ")


            if opcion=="1":

                self.nueva_partida()


            elif opcion=="2":

                self.cargar_partida()


            elif opcion=="3":

                break

    def muerte(self):

        print("""
    ============================
            HAS MUERTO
    ============================

    Tu historia termina aquí.

    ¿Qué quieres hacer?

    1. Cargar partida
    2. Nueva partida
    3. Salir

    """)

        while True:

            opcion = input("> ")

            if opcion == "1":

                self.cargar_partida()

                return


            elif opcion == "2":

                self.nueva_partida()

                return


            elif opcion == "3":

                exit()

    def nueva_partida(self):

        nombre=input("\nNombre del superviviente: ")

        self.jugador=Jugador(nombre)

        self.introduccion()

        self.jugador.inventario.append(
            self.objetos["Cuchillo"]
        )

        self.jugador.inventario.append(
            self.objetos["Pistola"]
        )

        self.jugador.inventario.append(
            deepcopy(self.objetos["Botella de agua"])
        )

        self.jugador.inventario.append(
            deepcopy(self.objetos["Lata de comida"])
        )

        self.jugador.inventario.append(
            deepcopy(self.objetos["Caja de munición"])
        )
        guardar.guardar(
            self.jugador.nombre,
            self.jugador.datos_guardado()
        )

        self.jugar()



    def cargar_partida(self):

        lista=guardar.partidas()


        if not lista:

            print("No hay partidas.")

            return


        print("\nPartidas:")

        for p in lista:

            print("-",p)


        nombre=input("> ")


        datos=guardar.cargar(nombre)


        if datos:

            self.jugador=Jugador(datos["nombre"])

            self.jugador.cargar_datos(datos)

            self.jugar()

    def menu_objetos(self, nombre, objetos):

        while True:

            print("\n====================")
            print(nombre.upper())
            print("====================")

            for i, objeto in enumerate(objetos, start=1):

                if objeto.tiene_durabilidad():

                    if objeto.tiene_durabilidad():
                        print(
                            f"{i}. {objeto.nombre} | "
                            f"{objeto.estado()} | "
                            f"Durabilidad: {objeto.durabilidad}/100"
                        )

                elif objeto.es_consumible():

                    print(
                        f"{i}. {objeto.nombre} ({objeto.usos_restantes} usos)"
                    )

                else:

                    print(
                        f"{i}. {objeto.nombre}"
                    )

            print("\n0. Volver")

            try:

                opcion = int(input("\n> "))

                if opcion == 0:
                    return

                objeto = objetos[opcion - 1]

                self.menu_acciones(objeto)

                if objeto not in self.jugador.inventario:
                    return

            except (ValueError, IndexError):

                print("\n❌ Opción no válida.")



    def menu_acciones(self, objeto):

        while True:

            print("\n====================")
            print(objeto.nombre.upper())
            print("====================")

            if objeto.tiene_durabilidad():
                print(
                    f"Durabilidad: {objeto.durabilidad}/100"
                )

            if objeto.es_consumible():
                print(
                    f"Usos restantes: {objeto.usos_restantes}"
                )

            print()
            print(f"1. {objeto.accion_principal}")

            opcion_reparar = None

            if objeto.reparable and objeto.durabilidad is not None:
                opcion_reparar = 2
                print("2. Reparar")
                print("3. Examinar")
                print("4. Tirar")
            else:
                print("2. Examinar")
                print("3. Tirar")

            print("0. Volver")

            try:

                opcion = int(input("\n> "))

                if opcion == 0:
                    return

                # Acción principal
                if opcion == 1:

                    if objeto.tipo == "municion":

                        from objetos import abrir_caja_municion

                        if abrir_caja_municion(self.jugador, objeto):
                            return

                    elif objeto.efecto:

                        resultado = objeto.usar(
                            self.jugador
                        )

                        if resultado:
                            self.jugador.inventario.remove(objeto)

                        return


                    else:

                        print(
                            f"\nNo puedes usar {objeto.nombre} ahora."
                        )

                # Reparar
                elif opcion_reparar == 2 and opcion == 2:

                    from objetos import reparar_objeto

                    reparar_objeto(self.jugador, objeto)

                # Examinar
                elif (opcion == 3 and opcion_reparar == 2) or \
                        (opcion == 2 and opcion_reparar is None):

                    print("\n" + objeto.descripcion)

                # Tirar
                elif (opcion == 4 and opcion_reparar == 2) or \
                        (opcion == 3 and opcion_reparar is None):

                    confirmar = input(
                        "\n¿Seguro que quieres tirarlo? (s/n): "
                    ).lower()

                    if confirmar == "s":
                        self.jugador.inventario.remove(objeto)

                        print("Has tirado el objeto.")

                        return

            except ValueError:

                pass

    def jugar(self):

        while True:

            if self.jugador.vida <= 0:
                self.muerte()

                return

            self.jugador.estado()


            lugar=self.mapa.obtener(
                self.jugador.localizacion
            )


            lugar.mostrar()


            print("""
1. Moverse
2. Saquear
3. Inventario
4. Guardar
5. Salir
""")


            opcion=input("> ")

            if opcion == "1":

                print("\n==========================")
                writefast("¿A dónde quieres viajar?")
                print("==========================\n")

                for i, destino in enumerate(lugar.conexiones, start=1):
                    print(f"{i}. {destino}")

                print("0. Cancelar")

                try:

                    eleccion = int(input("\n> "))

                    if eleccion == 0:
                        continue

                    destino = lugar.conexiones[eleccion - 1]

                except (ValueError, IndexError):

                    print("\n❌ Opción no válida.")

                    continue

                print(f"\n🚶 Viajas hacia {destino}...")

                self.jugador.localizacion = destino

                self.jugador.avanzar_tiempo(2)

                # Escena aleatoria de la zona
                comprobar_escena(
                    self.jugador,
                    self.objetos
                )

                input("\nPulsa ENTER para continuar...")

                # Eventos
                if random.randint(1, 100) <= 35:
                    evento_aleatorio(
                        self.jugador,
                        self.objetos
                    )

                # Combate
                if random.randint(1, 100) <= 25:

                    enemigo = enemigo_aleatorio()

                    resultado = iniciar_combate(
                        self.jugador,
                        enemigo
                    )

                    if not resultado and self.jugador.vida <= 0:
                        self.muerte()

                        return

                    self.jugador.comprobar_nivel()

            elif opcion == "2":

                saquear(
                    self.jugador,
                    self.objetos
                )

            elif opcion == "3":

                print("\n====================")
                print("    INVENTARIO")
                print("====================")

                grupos = self.jugador.inventario_agrupado()

                lista_grupos = list(grupos.items())

                for i, (nombre, objetos) in enumerate(lista_grupos, start=1):

                    primero = objetos[0]

                    # Objetos con usos
                    # Objetos consumibles con varios usos
                    if primero.usos is not None and primero.usos > 1:

                        usos_totales = sum(obj.usos_restantes for obj in objetos)

                        print(
                            f"{i}. {nombre} x{len(objetos)} : {usos_totales} usos"
                        )

                    # Caja de munición
                    elif nombre == "Caja de munición":

                        print(
                            f"{i}. {nombre} x{len(objetos)}"
                        )

                    # Objetos con durabilidad
                    elif primero.durabilidad is not None:

                        print(
                            f"{i}. {nombre} x{len(objetos)}"
                        )

                    # Objetos normales
                    else:

                        print(
                            f"{i}. {nombre} x{len(objetos)}"
                        )

                print("\n0. Volver")

                try:

                    eleccion = int(input("\n> "))

                    if eleccion == 0:
                        continue

                    nombre, objetos = lista_grupos[eleccion - 1]

                    self.menu_objetos(nombre, objetos)


                except (ValueError, IndexError):

                    pass

                input("\nPulsa ENTER para continuar...")



            elif opcion=="4":

                guardar.guardar(
                    self.jugador.nombre,
                    self.jugador.datos_guardado()
                )


            elif opcion=="5":

                break