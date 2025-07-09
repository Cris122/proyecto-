from utils import pantalla
from inventario import productos, buscar_producto_por_id, input_centrado
from clientes import lista_clientes, buscar_cliente_por_correo

ventas_realizadas = []

def menu_ventas():
    while True:
        pantalla.limpiar_pantalla()
        for linea in [
            "🛒 MENÚ DE VENTAS",
            "1. Registrar nueva venta",
            "2. Ver historial de ventas",
            "0. Volver al menú principal",
            pantalla.linea("-")
        ]:
            pantalla.imprimir_centrado(linea)
        print()
        opcion = input_centrado("Seleccione una opción")
        if opcion == "1": registrar_venta()
        elif opcion == "2": ver_historial_ventas()
        elif opcion == "0": break
        else: mensaje("❌ Opción no válida.")

def registrar_venta():
    pantalla.limpiar_pantalla()
    pantalla.imprimir_centrado("🧾 REGISTRAR VENTA")
    correo = input_centrado("Correo del cliente").lower()
    cliente = buscar_cliente_por_correo(correo)

    if cliente:
        pantalla.imprimir_centrado(f"🙋 Cliente frecuente: {cliente['nombre']}")
    else:
        nombre = input_centrado("Nombre del nuevo cliente")
        cliente = {"nombre": nombre, "correo": correo, "compras": []}
        lista_clientes.append(cliente)
        pantalla.imprimir_centrado(f"🆕 Cliente '{nombre}' registrado.")

    try: prod_id = int(input_centrado("ID del producto a vender"))
    except ValueError: return mensaje("❌ ID inválido.")

    producto = buscar_producto_por_id(prod_id)
    if not producto: return mensaje("❌ Producto no encontrado.")
    if producto["stock"] <= 0: return mensaje("❌ Producto sin stock.")

    producto["stock"] -= 1
    cliente["compras"].append(producto["precio_venta"])
    ventas_realizadas.append({
        "cliente": cliente["nombre"],
        "correo": cliente["correo"],
        "producto": producto["nombre"],
        "precio": producto["precio_venta"]
    })

    pantalla.imprimir_centrado(
        f"✅ {cliente['nombre']} compró '{producto['nombre']}' por ${producto['precio_venta']:.2f}")
    pantalla.pausar()

def ver_historial_ventas():
    pantalla.limpiar_pantalla()
    pantalla.imprimir_centrado("📜 HISTORIAL DE VENTAS")
    if not ventas_realizadas:
        pantalla.imprimir_centrado("No hay ventas registradas.")
    else:
        for i, v in enumerate(ventas_realizadas, 1):
            pantalla.imprimir_centrado(f"{i}. {v['cliente']} ({v['correo']}) - {v['producto']} - ${v['precio']:.2f}")
    pantalla.pausar()

def mensaje(texto):
    pantalla.imprimir_centrado(texto)
    pantalla.pausar()
