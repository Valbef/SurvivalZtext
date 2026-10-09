from copy import deepcopy


def añadir_objeto_inventario(jugador, objetos, nombre):
    """
    Añade un objeto al inventario del jugador respetando
    las reglas de apilamiento del sistema de saqueo.

    Reglas:
    - Objeto no apilable → nueva instancia.
    - Objeto apilable sin usos → se acumula en una instancia existente.
    - Objeto apilable con usos → nueva instancia independiente.
    """

    # =========================
    # COMPROBAR QUE EXISTE
    # =========================

    if nombre not in objetos:

        print(
            f"\n❌ El objeto '{nombre}' no existe en objetos.py."
        )

        return False

    # =========================
    # CREAR COPIA DEL OBJETO
    # =========================

    objeto = deepcopy(
        objetos[nombre]
    )

    # =========================
    # OBJETOS APILABLES
    # =========================

    if objeto.apilable:

        # =====================================
        # OBJETOS CON USOS
        # =====================================
        # Cada unidad mantiene sus propios usos.
        # Por eso NO se fusionan con otro objeto
        # del mismo nombre.

        if objeto.usos is not None:

            jugador.inventario.append(
                objeto
            )

        # =====================================
        # OBJETOS SIN USOS
        # =====================================
        # Estos sí se pueden acumular.

        else:

            objeto_existente = None

            for obj in jugador.inventario:

                if obj.nombre == nombre:

                    objeto_existente = obj
                    break

            if objeto_existente:

                objeto_existente.cantidad += (
                    objeto.cantidad
                )

            else:

                jugador.inventario.append(
                    objeto
                )

    # =========================
    # OBJETOS NO APILABLES
    # =========================

    else:

        jugador.inventario.append(
            objeto
        )

    return True