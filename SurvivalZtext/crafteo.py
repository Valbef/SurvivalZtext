from copy import deepcopy
from recetas import RECETAS


def obtener_cantidad(objetos, nombre):

    cantidad = 0

    for objeto in objetos:

        if objeto.nombre == nombre:
            cantidad += objeto.cantidad

    return cantidad


def mostrar_recetas(jugador, objetos):

    print("\n========================")
    print("       🔨 CRAFTEO")
    print("========================")

    recetas_disponibles = list(RECETAS.items())

    for i, (nombre, receta) in enumerate(recetas_disponibles, start=1):

        print(f"\n{i}. {nombre}")

        for material, cantidad_necesaria in receta["materiales"].items():

            cantidad_inventario = obtener_cantidad(
                jugador.inventario,
                material
            )

            cantidad_almacen = 0

            # El almacén solamente se puede utilizar en el refugio
            if jugador.localizacion == "Refugio":

                cantidad_almacen = obtener_cantidad(
                    jugador.almacen,
                    material
                )

            cantidad_total = (
                cantidad_inventario
                + cantidad_almacen
            )

            print(
                f"   {material}: "
                f"{cantidad_total}/{cantidad_necesaria}"
            )

    print("\n0. Volver")

    return recetas_disponibles


def tiene_materiales(jugador, receta):

    for material, cantidad_necesaria in receta["materiales"].items():

        cantidad = obtener_cantidad(
            jugador.inventario,
            material
        )

        if jugador.localizacion == "Refugio":

            cantidad += obtener_cantidad(
                jugador.almacen,
                material
            )

        if cantidad < cantidad_necesaria:

            return False

    return True


def quitar_materiales(lista, materiales):

    for nombre, cantidad_necesaria in materiales.items():

        cantidad_por_quitar = cantidad_necesaria

        for objeto in lista[:]:

            if objeto.nombre != nombre:
                continue

            cantidad_disponible = objeto.cantidad

            quitar = min(
                cantidad_disponible,
                cantidad_por_quitar
            )

            objeto.cantidad -= quitar

            if objeto.usos is not None:

                objeto.usos_restantes -= (
                    quitar * objeto.usos
                )

            cantidad_por_quitar -= quitar

            if objeto.cantidad <= 0:

                lista.remove(objeto)

            if cantidad_por_quitar <= 0:

                break


def consumir_materiales(jugador, receta):

    materiales = receta["materiales"]

    # Primero utilizamos los materiales del inventario
    materiales_restantes = {}

    for nombre, cantidad_necesaria in materiales.items():

        cantidad_inventario = obtener_cantidad(
            jugador.inventario,
            nombre
        )

        usado = min(
            cantidad_inventario,
            cantidad_necesaria
        )

        materiales_restantes[nombre] = (
            cantidad_necesaria - usado
        )

    quitar_materiales(
        jugador.inventario,
        {
            nombre: cantidad
            for nombre, cantidad in materiales.items()
        }
    )

    # Lo que falte se obtiene del almacén
    if jugador.localizacion == "Refugio":

        for nombre, cantidad in materiales_restantes.items():

            if cantidad > 0:

                quitar_materiales(
                    jugador.almacen,
                    {
                        nombre: cantidad
                    }
                )


def fabricar(jugador, objetos, nombre_receta):

    receta = RECETAS[nombre_receta]

    # =========================
    # COMPROBAR LUGAR
    # =========================

    if receta["tipo"] == "refugio":

        if jugador.localizacion != "Refugio":

            print(
                "\n❌ Este objeto solo puede fabricarse en el Refugio."
            )

            input("\nPulsa ENTER para continuar...")

            return

    # =========================
    # COMPROBAR MATERIALES
    # =========================

    if not tiene_materiales(jugador, receta):

        print(
            "\n❌ No tienes suficientes materiales."
        )

        input("\nPulsa ENTER para continuar...")

        return

    # =========================
    # COMPROBAR QUE EXISTE
    # =========================

    if nombre_receta not in objetos:

        print(
            "\n❌ Este objeto todavía no existe en objetos.py"
        )

        input("\nPulsa ENTER para continuar...")

        return

    # =========================
    # CONSUMIR MATERIALES
    # =========================

    consumir_materiales(
        jugador,
        receta
    )

    # =========================
    # CREAR OBJETO
    # =========================

    objeto_nuevo = deepcopy(
        objetos[nombre_receta]
    )

    # =========================
    # OBJETO APILABLE
    # =========================

    if objeto_nuevo.apilable:

        for objeto in jugador.inventario:

            if objeto.nombre == nombre_receta:

                objeto.cantidad += 1

                if objeto.usos is not None:

                    objeto.usos_restantes += objeto.usos

                print(
                    f"\n🔨 Has fabricado: {nombre_receta}"
                )

                input(
                    "\nPulsa ENTER para continuar..."
                )

                return

    # =========================
    # OBJETO NUEVO
    # =========================

    jugador.inventario.append(
        objeto_nuevo
    )

    print(
        f"\n🔨 Has fabricado: {nombre_receta}"
    )

    input(
        "\nPulsa ENTER para continuar..."
    )



def menu_crafteo(jugador, objetos):

    while True:

        recetas = mostrar_recetas(
            jugador,
            objetos
        )

        try:

            opcion = int(input("\n> "))

            if opcion == 0:

                return

            nombre_receta, receta = recetas[
                opcion - 1
            ]

            fabricar(
                jugador,
                objetos,
                nombre_receta
            )

        except (ValueError, IndexError):

            print(
                "\n❌ Opción no válida."
            )

            input(
                "\nPulsa ENTER para continuar..."
            )