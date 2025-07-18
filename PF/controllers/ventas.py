from utils import pantalla
from controllers.inventario import productos, buscar_producto_por_id, input_centrado
from controllers.clientes import lista_clientes, buscar_cliente_por_correo

ventas_realizadas = []

def menu_ventas():
    while True:
        try:
            pantalla.limpiar_pantalla()
            opciones = [
                "🛒 MENÚ DE VENTAS",
                "1. Registrar nueva venta",
                "2. Ver historial de ventas",
                "0. Volver al menú principal",
                pantalla.linea("-")
            ]
            list(map(pantalla.imprimir_centrado, opciones))
            print()

            opcion = input_centrado("Seleccione una opción")
            match opcion:
                case "1": registrar_venta()
                case "2": ver_historial_ventas()
                case "0": break
                case _: mensaje("❌ Opción no válida.")

        except KeyboardInterrupt:
            mensaje("⚠️ Operación cancelada por el usuario.")
            break
        except Exception as e:
            mensaje(f"❌ Error inesperado: {e}")

def registrar_venta():
    try:
        pantalla.limpiar_pantalla()
        pantalla.imprimir_centrado("🧾 REGISTRAR VENTA")

        correo = input_centrado("Correo del cliente").strip().lower()
        if not correo:
            raise ValueError("El correo no puede estar vacío")

        cliente = buscar_cliente_por_correo(correo)

        if cliente:
            pantalla.imprimir_centrado(f"🙋 Cliente frecuente: {cliente['nombre']}")
        else:
            nombre = input_centrado("Nombre del nuevo cliente").strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            cliente = {"nombre": nombre, "correo": correo, "compras": []}
            lista_clientes.append(cliente)
            pantalla.imprimir_centrado(f"🆕 Cliente '{nombre}' registrado.")

        try:
            prod_id = int(input_centrado("ID del producto a vender"))
        except ValueError:
            return mensaje("❌ ID inválido.")

        producto = buscar_producto_por_id(prod_id)
        if not producto:
            return mensaje("❌ Producto no encontrado.")
        if producto["stock"] <= 0:
            return mensaje("❌ Producto sin stock.")

        producto["stock"] -= 1
        cliente["compras"].append(producto["precio_venta"])
        ventas_realizadas.append({
            "cliente": cliente["nombre"],
            "correo": cliente["correo"],
            "producto": producto["nombre"],
            "precio": producto["precio_venta"]
        })

        pantalla.imprimir_centrado(
            f"✅ {cliente['nombre']} compró '{producto['nombre']}' por ${producto['precio_venta']:.2f}"
        )
        pantalla.pausar()

    except (ValueError, KeyError, AttributeError) as e:
        mensaje(f"❌ Error de datos: {e}")
    except KeyboardInterrupt:
        mensaje("⚠️ Venta cancelada por el usuario.")
    except Exception as e:
        mensaje(f"❌ Error inesperado: {e}")

def ver_historial_ventas():
    try:
        pantalla.limpiar_pantalla()
        pantalla.imprimir_centrado("📜 HISTORIAL DE VENTAS")

        if not ventas_realizadas:
            pantalla.imprimir_centrado("No hay ventas registradas.")
        else:
            for i, v in enumerate(ventas_realizadas, 1):
                pantalla.imprimir_centrado(
                    f"{i}. {v['cliente']} ({v['correo']}) - {v['producto']} - ${v['precio']:.2f}"
                )
        pantalla.pausar()

    except KeyError as e:
        mensaje(f"❌ Error al mostrar venta: {e}")
    except Exception as e:
        mensaje(f"❌ Error inesperado: {e}")

def mensaje(texto):
    try:
        pantalla.imprimir_centrado(texto)
        pantalla.pausar()
    except Exception as e:
        print(f"Error al mostrar mensaje: {e}")
        input("Presione Enter para continuar...")