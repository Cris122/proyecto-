from utils import pantalla

productos = []

# Funciones utilitarias
def generar_id():
    return productos[-1]["id"] + 1 if productos else 1

def buscar_producto_por_id(pid):
    for prod in productos:
        if prod["id"] == pid:
            return prod
    return None

def mostrar_titulo(texto, emoji=""):
    pantalla.limpiar_pantalla()
    pantalla.imprimir_centrado(pantalla.linea("="))
    pantalla.imprimir_centrado(f"{emoji} {texto.upper()} {emoji}")
    pantalla.imprimir_centrado(pantalla.linea("="))
    print()

def input_centrado(label):
    texto = f"{label}: "
    espacio = " " * ((pantalla.ancho_consola() - len(texto)) // 2)
    return input(f"{espacio}{texto}").strip()

def solicitar_datos_producto(predefinido=None):
    p = {}
    p["nombre"] = input_centrado("Nombre del producto") or (predefinido["nombre"] if predefinido else "")
    p["categoria"] = input_centrado("Categoría (anillo, collar, etc.)") or (predefinido["categoria"] if predefinido else "")
    p["material"] = input_centrado("Material (oro, plata, etc.)") or (predefinido["material"] if predefinido else "")
    try:
        p["precio_compra"] = float(input_centrado("Precio de compra")) or (predefinido["precio_compra"] if predefinido else 0)
        p["precio_venta"] = float(input_centrado("Precio de venta")) or (predefinido["precio_venta"] if predefinido else 0)
        p["stock"] = int(input_centrado("Cantidad en stock")) or (predefinido["stock"] if predefinido else 0)
    except ValueError:
        pantalla.imprimir_centrado("❌ Error: entrada no válida.")
        pantalla.pausar()
        return None
    return p

# Menú principal del módulo Inventario
def menu_inventario():
    while True:
        mostrar_titulo("MENÚ DE INVENTARIO", "🧾")
        pantalla.imprimir_centrado("1. Ver inventario")
        pantalla.imprimir_centrado("2. Agregar producto")
        pantalla.imprimir_centrado("3. Editar producto")
        pantalla.imprimir_centrado("4. Buscar producto")
        pantalla.imprimir_centrado("5. Eliminar producto")
        pantalla.imprimir_centrado("6. Restablecer inventario")
        pantalla.imprimir_centrado("0. Volver al menú principal")
        pantalla.imprimir_centrado(pantalla.linea("-"))
        print()

        opcion = input_centrado("Seleccione una opción")
        match opcion:
            case "1":
                ver_inventario()
            case "2":
                agregar_producto()
            case "3":
                editar_producto()
            case "4":
                buscar_producto()
            case "5":
                eliminar_producto()
            case "6":
                restablecer_inventario()
            case "0":
                break
            case _:
                pantalla.imprimir_centrado("❌ Opción no válida.")
                pantalla.pausar()

# Ver inventario
def ver_inventario():
    mostrar_titulo("Inventario actual", "📦")
    if not productos:
        pantalla.imprimir_centrado("El inventario está vacío.")
    else:
        header = f"{'ID':<5} {'Nombre':<20} {'Categoría':<12} {'Material':<10} {'Compra':<8} {'Venta':<8} {'Stock':<6}"
        pantalla.imprimir_centrado(header)
        pantalla.imprimir_centrado("-" * len(header))
        for p in productos:
            linea = f"{p['id']:<5} {p['nombre']:<20} {p['categoria']:<12} {p['material']:<10} ${p['precio_compra']:<8.2f} ${p['precio_venta']:<8.2f} {p['stock']:<6}"
            pantalla.imprimir_centrado(linea)
        pantalla.imprimir_centrado(f"📦 Total de productos: {len(productos)}")
    pantalla.pausar()

# Agregar producto
def agregar_producto():
    mostrar_titulo("Agregar nuevo producto", "➕")
    datos = solicitar_datos_producto()
    if datos:
        datos["id"] = generar_id()
        productos.append(datos)
        pantalla.imprimir_centrado(f"✅ Producto '{datos['nombre']}' ID {datos['id']} agregado correctamente.")
    pantalla.pausar()

# Buscar producto
def buscar_producto():
    mostrar_titulo("Buscar producto", "🔍")
    termino = input_centrado("Ingrese nombre o parte del nombre").lower()
    encontrados = [p for p in productos if termino in p['nombre'].lower()]
    if encontrados:
        for p in encontrados:
            linea = f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio_venta']:.2f} | Stock: {p['stock']}"
            pantalla.imprimir_centrado(linea)
    else:
        pantalla.imprimir_centrado("❌ No se encontraron productos.")
    pantalla.pausar()

#  Editar producto
def editar_producto():
    mostrar_titulo("Editar producto", "✏️")
    try:
        prod_id = int(input_centrado("Ingrese el ID del producto a editar"))
    except ValueError:
        pantalla.imprimir_centrado("❌ ID inválido.")
        pantalla.pausar()
        return

    producto = buscar_producto_por_id(prod_id)
    if not producto:
        pantalla.imprimir_centrado("❌ Producto no encontrado.")
        pantalla.pausar()
        return

    datos = solicitar_datos_producto(predefinido=producto)
    if datos:
        producto.update(datos)
        pantalla.imprimir_centrado("✅ Producto actualizado correctamente.")
    pantalla.pausar()

#  Eliminar producto
def eliminar_producto():
    mostrar_titulo("Eliminar producto", "🗑️")
    try:
        prod_id = int(input_centrado("Ingrese el ID del producto a eliminar"))
    except ValueError:
        pantalla.imprimir_centrado("❌ ID inválido.")
        pantalla.pausar()
        return

    producto = buscar_producto_por_id(prod_id)
    if producto:
        productos.remove(producto)
        pantalla.imprimir_centrado(f"✅ Producto '{producto['nombre']}' eliminado.")
    else:
        pantalla.imprimir_centrado("❌ Producto no encontrado.")
    pantalla.pausar()

# Restablecer inventario
def restablecer_inventario():
    mostrar_titulo("Restablecer inventario", "🧹")
    confirm = input_centrado("¿Está seguro que desea eliminar todo? (s/n)").lower()
    if confirm == 's':
        productos.clear()
        pantalla.imprimir_centrado("✅ Inventario restablecido.")
    else:
        pantalla.imprimir_centrado("⚠️ Operación cancelada.")
    pantalla.pausar()
