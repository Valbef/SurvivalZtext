from jugador import Jugador
from mapa import Mapa
from objetos import lista_objetos, reparar_objeto
from enemigos import crear_enemigos
from enemigos import enemigo_aleatorio
from combate import iniciar_combate
from eventos import evento_aleatorio
from saqueo import saquear
from motor_escenas import comprobar_escena
from efectos import write, writefast
from copy import deepcopy
from crafteo import menu_crafteo
#from collections import defaultdict
import random
import guardar

RESET = "\033[0m"
LIGHT_RED = "\033[91m"
RED = "\033[91m"
WHITE = "\033[97m"

class Juego:


    def __init__(self):

        self.objetos = lista_objetos()

        self.jugador = None

        self.mapa = Mapa()

        self.enemigos = crear_enemigos()

    def introduccion(self):

        print(f"""{RED}
  ====================================================
                     SURVIVAL Z 2030
  ===================================================={RESET}""")
        write(f"""{WHITE}
  Año 2030.

  Todo comenzó hace apenas una semana.

  Una extraña enfermedad apareció en varias ciudades,
  algo se habia extendido por todo el mundo.
  Al principio parecía una gripe especialmente agresiva,
  pero los hospitales pronto quedaron desbordados.
    
  Las carreteras quedaron bloqueadas,
  las comunicaciones dejaron de funcionar,
  el gobierno declaró el estado de emergencia 
  y ordenó un confinamiento hasta nueva orden. 
  Nadie ha vuelto a saber nada de las autoridades...

  Ahora los supermercados están vacíos,
  las calles son un cementerio y cada superviviente
  lucha únicamente por seguir con vida un día más.
    {RESET}""")

        input("\nPulsa ENTER para continuar...")

        write(f"""{WHITE}
  Has conseguido refugiarte en una pequeña casa
  a las afueras de la ciudad.

  No sabes si existen zonas seguras.
  No sabes si queda algún ejército organizado.
  No sabes cuánto tiempo podrás sobrevivir.

     Solo sabes una cosa...

  Si quieres vivir, tendrás que salir ahí fuera.
    {RESET}""")
        writefast(f"""{RED}  ======================================================{RESET}""")
        write(f"""{WHITE}               Comienza tu historia...{RESET}""")
        writefast(f"""{RED}  ======================================================{RESET}
    """)
        write(f"{WHITE}   Cuanto tiempo crees que sobrevivirás?{RESET}")

        input("\nPulsa ENTER para comenzar...")



    def menu(self):

        while True:

            writefast(f"""
{WHITE}============================{RESET}
       {RED}Llámalo juego...{RESET}
{WHITE}============================{RESET}

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

        print(f"""{RED}
    ============================
            HAS MUERTO
    ============================{RESET}
    {LIGHT_RED}
    Tu historia termina aquí.{RESET}

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

            # =====================================
            # MOSTRAR OBJETOS INDIVIDUALES
            # =====================================

            for i, objeto in enumerate(objetos, start=1):

                # Objetos con durabilidad
                if objeto.tiene_durabilidad():

                    print(
                        f"{i}. {objeto.nombre} | "
                        f"{objeto.estado()} | "
                        f"Durabilidad: "
                        f"{objeto.durabilidad}/100"
                    )

                # Objetos con usos
                elif objeto.usos is not None:

                    print(
                        f"{i}. {objeto.nombre} : "
                        f"{objeto.usos_restantes} usos"
                    )

                # Objetos normales
                else:

                    print(
                        f"{i}. {objeto.nombre}"
                    )

            print("\n0. Volver")

            try:

                opcion = int(input("\n> "))

                if opcion == 0:
                    return

                # Seleccionar objeto INDIVIDUAL
                objeto = objetos[opcion - 1]

                self.menu_acciones(
                    objeto,
                    objeto.usos_restantes
                    if objeto.usos is not None
                    else None,
                    objetos
                )

                # =====================================
                # ACTUALIZAR LA LISTA
                # =====================================

                objetos = [
                    obj
                    for obj in objetos
                    if obj in self.jugador.inventario
                ]

                # Si ya no quedan objetos de este tipo
                if not objetos:
                    return

            except (ValueError, IndexError):

                print("\n❌ Opción no válida.")

    def menu_reparar(self):

        while True:

            print("\n====================")
            print("   REPARAR OBJETO")
            print("====================")

            objetos_reparables = []

            for objeto in self.jugador.inventario:

                if (
                        objeto.reparable
                        and objeto.durabilidad is not None
                        and objeto.durabilidad < 100
                ):
                    objetos_reparables.append(objeto)

            # =========================
            # NO HAY NADA QUE REPARAR
            # =========================

            if not objetos_reparables:
                print(
                    "\n❌ No tienes objetos que necesiten reparación."
                )

                input("\nPulsa ENTER para continuar...")

                return

            # =========================
            # BUSCAR RECURSOS
            # =========================

            kit = None
            herramientas = None

            for objeto in self.jugador.inventario:

                if (
                        objeto.nombre == "Kit de reparación"
                        and objeto.usos_restantes is not None
                        and objeto.usos_restantes > 0
                ):
                    kit = objeto

                elif (
                        objeto.nombre == "Herramientas"
                        and objeto.usos_restantes is not None
                        and objeto.usos_restantes > 0
                ):
                    herramientas = objeto

            # =========================
            # NO HAY RECURSOS
            # =========================

            if kit is None and herramientas is None:
                print(
                    "\n❌ No tienes Kits de reparación "
                    "ni Herramientas."
                )

                input("\nPulsa ENTER para continuar...")

                return

            # =========================
            # MOSTRAR RECURSOS
            # =========================

            print()

            if kit is not None:
                print(
                    f"🧰 Kits de reparación: "
                    f"{kit.cantidad}"
                )

            if herramientas is not None:
                print(
                    f"🔧 Herramientas: "
                    f"{herramientas.usos_restantes} usos"
                )

            print()

            # =========================
            # MOSTRAR OBJETOS
            # =========================

            for i, objeto in enumerate(
                    objetos_reparables,
                    start=1
            ):
                print(
                    f"{i}. {objeto.nombre} | "
                    f"{objeto.estado()} | "
                    f"{objeto.durabilidad}/100"
                )

            print("\n0. Volver")

            try:

                opcion = int(input("\n> "))

                if opcion == 0:
                    return

                objeto = objetos_reparables[opcion - 1]

                # =========================
                # REPARAR
                # =========================

                reparar_objeto(
                    self.jugador,
                    objeto
                )

                input("\nPulsa ENTER para continuar...")

                return

            except (ValueError, IndexError):

                print("\n❌ Opción no válida.")

    def menu_acciones(self, objeto, usos_totales=None, grupo=None):

        while True:

            print("\n====================")
            print(objeto.nombre.upper())
            print("====================")

            # =========================
            # DURABILIDAD
            # =========================

            if objeto.tiene_durabilidad():
                print(
                    f"Durabilidad: {objeto.durabilidad}/100"
                )

            # =========================
            # USOS
            # =========================

            if objeto.es_consumible():

                if usos_totales is not None:

                    print(
                        f"Usos restantes: {usos_totales}"
                    )

                else:

                    print(
                        f"Usos restantes: "
                        f"{objeto.usos_restantes}"
                    )

            print()
            print(f"1. {objeto.accion_principal}")

            opcion_reparar = None

            if (
                    objeto.reparable
                    and objeto.durabilidad is not None
            ):

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

                # ==================================================
                # ACCIÓN PRINCIPAL
                # ==================================================

                if opcion == 1:

                    # =========================
                    # CAJA DE MUNICIÓN
                    # =========================

                    if objeto.tipo == "municion":

                        from objetos import abrir_caja_municion

                        if abrir_caja_municion(
                                self.jugador,
                                objeto
                        ):
                            return

                    # =========================
                    # HERRAMIENTAS
                    # =========================

                    elif objeto.nombre in (
                            "Herramientas",
                            "Kit de reparación"
                    ):

                        self.menu_reparar()

                        return

                    # =========================
                    # OBJETOS CON EFECTO
                    # =========================

                    elif objeto.efecto:

                        resultado = objeto.usar(
                            self.jugador
                        )

                        if resultado and objeto.es_consumible():

                            # objeto.usar() YA ha restado 1 uso

                            if objeto.usos_restantes <= 0:

                                print(
                                    f"\n🔴 {objeto.nombre} se ha agotado."
                                )

                                if objeto in self.jugador.inventario:
                                    self.jugador.inventario.remove(
                                        objeto
                                    )

                        return



                    # =========================
                    # SIN ACCIÓN
                    # =========================

                    else:

                        print(
                            f"\nNo puedes usar "
                            f"{objeto.nombre} ahora."
                        )

                # ==================================================
                # REPARAR
                # ==================================================

                elif (
                        opcion_reparar == 2
                        and opcion == 2
                ):

                    from objetos import reparar_objeto

                    reparar_objeto(
                        self.jugador,
                        objeto
                    )

                # ==================================================
                # EXAMINAR
                # ==================================================

                elif (
                        (opcion == 3 and opcion_reparar == 2)
                        or
                        (opcion == 2 and opcion_reparar is None)
                ):

                    print(
                        "\n" + objeto.descripcion
                    )

                # ==================================================
                # TIRAR
                # ==================================================

                elif (
                        (opcion == 4 and opcion_reparar == 2)
                        or
                        (opcion == 3 and opcion_reparar is None)
                ):

                    # =============================================
                    # OBJETOS CON USOS
                    # =============================================

                    if objeto.usos is not None:

                        # Cada objeto seleccionado representa
                        # UNA unidad individual.
                        #
                        # Ejemplo:
                        #
                        # Botella A -> 3 usos
                        # Botella B -> 2 usos
                        #
                        # Si seleccionas la Botella A y la tiras,
                        # SOLO se elimina la Botella A.

                        confirmar = input(
                            f"\n¿Seguro que quieres tirar "
                            f"1 unidad(es) de {objeto.nombre} "
                            f"({objeto.usos_restantes} usos)? (s/n): "
                        ).lower()

                        if confirmar == "s":

                            if objeto in self.jugador.inventario:
                                self.jugador.inventario.remove(objeto)

                                print(
                                    f"Has tirado 1 unidad(es) "
                                    f"de {objeto.nombre}."
                                )

                            return

                        # Si responde "n", vuelve al menú
                        continue

                    # =============================================
                    # OBJETOS SIN USOS
                    # =============================================

                    else:

                        # Buscar todas las unidades del mismo objeto
                        objetos_iguales = [
                            obj
                            for obj in self.jugador.inventario
                            if obj.nombre == objeto.nombre
                        ]

                        cantidad_total = sum(
                            obj.cantidad
                            for obj in objetos_iguales
                        )

                        # =============================================
                        # ELEGIR CANTIDAD
                        # =============================================

                        if cantidad_total > 1:

                            while True:

                                try:

                                    cantidad_tirar = int(
                                        input(
                                            f"\n¿Cuántas unidades quieres "
                                            f"tirar? (1-{cantidad_total}): "
                                        )
                                    )

                                    if 1 <= cantidad_tirar <= cantidad_total:
                                        break

                                    print(
                                        f"Introduce un número entre "
                                        f"1 y {cantidad_total}."
                                    )

                                except ValueError:

                                    print(
                                        "Introduce un número válido."
                                    )

                        else:

                            cantidad_tirar = 1

                        # =============================================
                        # CONFIRMAR
                        # =============================================

                        confirmar = input(
                            f"\n¿Seguro que quieres tirar "
                            f"{cantidad_tirar} unidad(es) de "
                            f"{objeto.nombre}? (s/n): "
                        ).lower()

                        if confirmar != "s":
                            continue

                        # =============================================
                        # ELIMINAR UNIDADES
                        # =============================================

                        restante = cantidad_tirar

                        for obj in objetos_iguales:

                            if restante <= 0:
                                break

                            quitar = min(
                                obj.cantidad,
                                restante
                            )

                            obj.cantidad -= quitar

                            restante -= quitar

                            if obj.cantidad <= 0:
                                self.jugador.inventario.remove(obj)

                        print(
                            f"Has tirado "
                            f"{cantidad_tirar} unidad(es) "
                            f"de {objeto.nombre}."
                        )

                        return


            except ValueError:

                print(
                    "\n❌ Introduce una opción válida."
                )

    def menu_almacen(self):

      while True:

        print("\n====================")
        print("    🏠 ALMACÉN")
        print("====================")

        print(
            f"\n⚖️ Peso almacenado: "
            f"{self.jugador.peso_almacen()} kg"
        )

        if self.jugador.almacen:

            print("\nObjetos almacenados:")

            grupos = self.jugador.inventario_agrupado_almacen()

            for i, (nombre, objetos) in enumerate(grupos.items(), start=1):
                primero = objetos[0]

                print(
                    f"{i}. {nombre} x{primero.cantidad}"
                )

        else:

            print("\n📦 El almacén está vacío.")

        print("\n1. Guardar objetos")
        print("2. Sacar objetos")
        print("0. Volver")

        opcion = input("\n> ")

        if opcion == "1":

            self.guardar_en_almacen()

        elif opcion == "2":

            self.sacar_del_almacen()

        elif opcion == "0":

            return

        else:

            print("\n❌ Opción no válida.")

    def guardar_en_almacen(self):

        if not self.jugador.inventario:
            print("\n🎒 No llevas ningún objeto.")
            input("\nPulsa ENTER para continuar...")
            return

        grupos = self.jugador.inventario_agrupado()
        lista_grupos = list(grupos.items())

        print("\n====================")
        print("  GUARDAR OBJETOS")
        print("====================")

        for i, (nombre, objetos) in enumerate(lista_grupos, start=1):
            cantidad_total = sum(
                obj.cantidad
                for obj in objetos
            )

            print(
                f"{i}. {nombre} x{cantidad_total}"
            )

        print("\n0. Cancelar")

        try:

            eleccion = int(input("\n> "))

            if eleccion == 0:
                return

            nombre, objetos = lista_grupos[eleccion - 1]

            cantidad_total = sum(
                obj.cantidad
                for obj in objetos
            )

            # =====================================
            # ELEGIR CANTIDAD
            # =====================================

            if cantidad_total > 1:

                while True:

                    try:

                        cantidad = int(
                            input(
                                f"\nTienes {cantidad_total} unidades."
                                f"\n¿Cuántas quieres guardar? > "
                            )
                        )

                        if 1 <= cantidad <= cantidad_total:
                            break

                        print(
                            f"\n❌ Introduce una cantidad "
                            f"entre 1 y {cantidad_total}."
                        )

                    except ValueError:

                        print("\n❌ Introduce un número válido.")

            else:

                cantidad = 1

            # =====================================
            # OBJETOS CON USOS
            # =====================================

            if objetos[0].usos is not None:

                restantes = cantidad

                # Guardamos unidades completas.
                # Se empieza por las unidades con menos usos.
                objetos_ordenados = sorted(
                    objetos,
                    key=lambda obj: obj.usos_restantes
                )

                for objeto in objetos_ordenados:

                    if restantes <= 0:
                        break

                    unidades = min(
                        objeto.cantidad,
                        restantes
                    )

                    # Buscar objeto igual en almacén
                    objeto_almacen = None

                    for obj in self.jugador.almacen:

                        if obj.nombre == objeto.nombre:
                            objeto_almacen = obj
                            break

                    # =====================================
                    # CREAR / AÑADIR AL ALMACÉN
                    # =====================================

                    if objeto_almacen is None:

                        objeto_almacen = deepcopy(objeto)

                        objeto_almacen.cantidad = unidades

                        objeto_almacen.usos_restantes = (
                                objeto.usos_restantes
                                - (
                                        (objeto.cantidad - unidades)
                                        * objeto.usos
                                )
                        )

                        self.jugador.almacen.append(
                            objeto_almacen
                        )

                    else:

                        objeto_almacen.cantidad += unidades

                        objeto_almacen.usos_restantes += (
                                objeto.usos_restantes
                                - (
                                        (objeto.cantidad - unidades)
                                        * objeto.usos
                                )
                        )

                    # =====================================
                    # RESTAR DEL INVENTARIO
                    # =====================================

                    objeto.cantidad -= unidades

                    objeto.usos_restantes = (
                            objeto.cantidad * objeto.usos
                    )

                    restantes -= unidades

                    if objeto.cantidad <= 0:
                        self.jugador.inventario.remove(
                            objeto
                        )

            # =====================================
            # OBJETOS NORMALES
            # =====================================

            else:

                restantes = cantidad

                for objeto in objetos:

                    if restantes <= 0:
                        break

                    quitar = min(
                        objeto.cantidad,
                        restantes
                    )

                    # Buscar en almacén
                    objeto_almacen = None

                    for obj in self.jugador.almacen:

                        if obj.nombre == objeto.nombre:
                            objeto_almacen = obj
                            break

                    if objeto_almacen is None:

                        objeto_almacen = deepcopy(objeto)
                        objeto_almacen.cantidad = quitar

                        self.jugador.almacen.append(
                            objeto_almacen
                        )

                    else:

                        objeto_almacen.cantidad += quitar

                    objeto.cantidad -= quitar

                    restantes -= quitar

                    if objeto.cantidad <= 0:
                        self.jugador.inventario.remove(
                            objeto
                        )

            print(
                f"\n📦 Has guardado "
                f"{cantidad} x {nombre}."
            )

            input(
                "\nPulsa ENTER para continuar..."
            )

        except (ValueError, IndexError):

            print("\n❌ Opción no válida.")

            input(
                "\nPulsa ENTER para continuar..."
            )

    def sacar_del_almacen(self):

        if not self.jugador.almacen:
            print("\n📦 El almacén está vacío.")
            input("\nPulsa ENTER para continuar...")
            return

        grupos = self.jugador.inventario_agrupado_almacen()

        lista_grupos = list(grupos.items())

        print("\n====================")
        print("   SACAR OBJETOS")
        print("====================")

        for i, (nombre, objetos) in enumerate(lista_grupos, start=1):
            primero = objetos[0]

            print(
                f"{i}. {nombre} x{primero.cantidad}"
            )

        print("\n0. Cancelar")

        try:

            eleccion = int(input("\n> "))

            if eleccion == 0:
                return

            nombre, objetos = lista_grupos[eleccion - 1]

            objeto = objetos[0]

            # =========================
            # ELEGIR CANTIDAD
            # =========================

            if objeto.cantidad > 1:

                print(
                    f"\nTienes {objeto.cantidad} unidades."
                )

                cantidad = int(
                    input("¿Cuántas quieres sacar? > ")
                )

                if cantidad <= 0 or cantidad > objeto.cantidad:
                    print("\n❌ Cantidad no válida.")
                    input("\nPulsa ENTER para continuar...")
                    return

            else:

                cantidad = 1

            # =========================
            # COMPROBAR PESO
            # =========================

            peso_actual = self.jugador.peso_total()

            peso_nuevo = (
                    peso_actual
                    + objeto.peso * cantidad
            )

            if peso_nuevo > self.jugador.capacidad_peso():
                print("\n⚠️ No puedes llevar esos objetos.")

                print(
                    f"⚖️ Peso actual: "
                    f"{peso_actual} kg"
                )

                print(
                    f"⚖️ Peso que quieres sacar: "
                    f"{objeto.peso * cantidad} kg"
                )

                print(
                    f"⚖️ Capacidad máxima: "
                    f"{self.jugador.capacidad_peso()} kg"
                )

                input("\nPulsa ENTER para continuar...")
                return

            # =========================
            # BUSCAR EN INVENTARIO
            # =========================

            objeto_inventario = None

            for obj in self.jugador.inventario:

                if obj.nombre == objeto.nombre:
                    objeto_inventario = obj
                    break

            # =========================
            # YA EXISTE EN INVENTARIO
            # =========================

            if objeto_inventario:

                objeto_inventario.cantidad += cantidad

                if objeto_inventario.usos is not None:
                    objeto_inventario.usos_restantes += (
                            cantidad * objeto_inventario.usos
                    )

            # =========================
            # NO EXISTE EN INVENTARIO
            # =========================

            else:

                nuevo_objeto = deepcopy(objeto)

                nuevo_objeto.cantidad = cantidad

                if nuevo_objeto.usos is not None:
                    nuevo_objeto.usos_restantes = (
                            cantidad * nuevo_objeto.usos
                    )

                self.jugador.inventario.append(
                    nuevo_objeto
                )

            # =========================
            # RESTAR DEL ALMACÉN
            # =========================

            objeto.cantidad -= cantidad

            if objeto.usos_restantes is not None:
                objeto.usos_restantes -= (
                        cantidad * objeto.usos
                )

            if objeto.cantidad <= 0:
                self.jugador.almacen.remove(
                    objeto
                )

            print(
                f"\n🎒 Has sacado {cantidad} "
                f"x {objeto.nombre}."
            )

            input("\nPulsa ENTER para continuar...")

        except (ValueError, IndexError):

            print("\n❌ Opción no válida.")
            input("\nPulsa ENTER para continuar...")


    def jugar(self):

        while True:

            if self.jugador.vida <= 0:
                self.muerte()

                return

            self.jugador.estado()

            lugar = self.mapa.obtener(
                self.jugador.localizacion
            )

            lugar.mostrar()

            # =========================
            # MENÚ
            # =========================

            if self.jugador.localizacion == "Refugio":

                print("\n1. Moverse")
                print("2. Saquear")
                print("3. Inventario")
                print("4. Almacén")
                print("5. Crafteo")
                print("6. Guardar")
                print("7. Salir")

            else:

                print("\n1. Moverse")
                print("2. Saquear")
                print("3. Inventario")
                print("4. Guardar")
                print("5. Crafteo")
                print("6. Salir")

            opcion = input("> ")

            # =========================
            # MOVERSE
            # =========================

            if opcion == "1":

                print("\n==========================")
                writefast("¿A dónde quieres viajar?")
                print("==========================\n")

                for i, destino in enumerate(
                        lugar.conexiones,
                        start=1
                ):
                    print(f"{i}. {destino}")

                print("0. Cancelar")

                try:

                    eleccion = int(input("\n> "))

                    if eleccion == 0:
                        continue

                    destino = lugar.conexiones[
                        eleccion - 1
                        ]

                except (ValueError, IndexError):

                    print("\n❌ Opción no válida.")

                    continue

                # =========================
                # COMPROBAR PESO
                # =========================

                if not self.jugador.puede_viajar():
                    print(
                        "\n⚠️ Llevas demasiadas cosas."
                    )

                    print(
                        f"⚖️ Peso actual: "
                        f"{self.jugador.peso_total()} / "
                        f"{self.jugador.capacidad_peso()} kg"
                    )

                    print(
                        "\nNo puedes viajar hasta que "
                        "reduzcas el peso de tu inventario."
                    )

                    input(
                        "\nPulsa ENTER para continuar..."
                    )

                    continue

                # =========================
                # VIAJAR
                # =========================

                print(
                    f"\n🚶 Viajas hacia {destino}..."
                )

                self.jugador.localizacion = destino

                self.jugador.avanzar_tiempo(2)

                # =========================
                # ESCENA ALEATORIA
                # =========================

                comprobar_escena(
                    self.jugador,
                    self.objetos
                )

                input(
                    "\nPulsa ENTER para continuar..."
                )

                # =========================
                # EVENTOS
                # =========================

                if random.randint(1, 100) <= 25:
                    evento_aleatorio(
                        self.jugador,
                        self.objetos
                    )

                # =========================
                # COMBATE
                # =========================

                if random.randint(1, 100) <= 25:

                    enemigo = enemigo_aleatorio()

                    resultado = iniciar_combate(
                        self.jugador,
                       enemigo,
                               self.objetos
                    )

                    if (
                            not resultado
                            and self.jugador.vida <= 0
                    ):
                        self.muerte()

                        return

                    self.jugador.comprobar_nivel()

            # =========================
            # SAQUEAR
            # =========================

            elif opcion == "2":

                saquear(
                    self.jugador,
                    self.objetos
                )

            # =========================
            # INVENTARIO
            # =========================

            elif opcion == "3":

                print("\n====================")
                print("    INVENTARIO")
                print("====================")

                print(
                    f"⚖️ Peso: "
                    f"{self.jugador.peso_total()} / "
                    f"{self.jugador.capacidad_peso()} kg"
                )

                grupos = (
                    self.jugador.inventario_agrupado()
                )

                lista_grupos = list(
                    grupos.items()
                )

                for i, (
                        nombre,
                        objetos
                ) in enumerate(
                    lista_grupos,
                    start=1
                ):

                    primero = objetos[0]
                    cantidad_total = sum(
                        obj.cantidad
                        for obj in objetos
                    )

                    # =========================
                    # OBJETOS CON USOS
                    # =========================

                    if (
                            primero.usos is not None
                            and primero.usos > 1
                    ):

                        usos_totales = sum(
                            obj.usos_restantes
                            for obj in objetos
                        )

                        print(
                            f"{i}. {nombre} "
                            f"x{cantidad_total} : "
                            f"{usos_totales} usos"
                        )

                    # =========================
                    # CAJA DE MUNICIÓN
                    # =========================

                    elif nombre == "Caja de munición":

                        print(
                            f"{i}. {nombre} "
                            f"x{cantidad_total}"
                        )

                    # =========================
                    # OBJETOS CON DURABILIDAD
                    # =========================

                    elif (
                            primero.durabilidad is not None
                    ):

                        print(
                            f"{i}. {nombre} "
                            f"x{cantidad_total}"
                        )

                    # =========================
                    # OBJETOS NORMALES
                    # =========================

                    else:

                        print(
                            f"{i}. {nombre} "
                            f"x{cantidad_total}"
                        )

                print("\n0. Volver")

                try:

                    eleccion = int(
                        input("\n> ")
                    )

                    if eleccion == 0:
                        continue

                    nombre, objetos = (
                        lista_grupos[
                            eleccion - 1
                            ]
                    )

                    self.menu_objetos(
                        nombre,
                        objetos
                    )

                except (
                        ValueError,
                        IndexError
                ):

                    pass

                input(
                    "\nPulsa ENTER para continuar..."
                )

            # =========================
            # ALMACÉN / GUARDAR
            # =========================

            elif opcion == "4":

                if (
                        self.jugador.localizacion
                        == "Refugio"
                ):

                    self.menu_almacen()

                else:

                    guardar.guardar(
                        self.jugador.nombre,
                        self.jugador.datos_guardado()
                    )

            # =========================
            # CRAFTEO / SALIR
            # =========================

            elif opcion == "5":

                menu_crafteo(
                    self.jugador,
                    self.objetos
                )

            # =========================
            # GUARDAR / SALIR
            # =========================

            elif opcion == "6":

                if self.jugador.localizacion == "Refugio":

                    guardar.guardar(
                        self.jugador.nombre,
                        self.jugador.datos_guardado()
                    )

                else:

                    break

            # =========================
            # SALIR
            # =========================

            elif opcion == "7":

                if self.jugador.localizacion == "Refugio":
                    break