from utils import pantalla

productos = []

# ─────────────────────────────────────────────
# Funciones utilitarias
# ─────────────────────────────────────────────

def generar_id():
    return max([p["id"] for p in productos], default=0) + 1

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

def input_texto_requerido(label, predeterminado=""):
    while True:
        entrada = input_centrado(label)
        if entrada:
            return entrada
        elif predeterminado:
            return predeterminado
        pantalla.imprimir_centrado("❌ Campo obligatorio. Intente de nuevo.")

def input_numerico_centrado(label, tipo=float, predeterminado=0):
    while True:
        entrada = input_centrado(label)
        if entrada == "" and predeterminado is not None:
            return predeterminado
        try:
            valor = tipo(entrada)
            if valor < 0:
                pantalla.imprimir_centrado("❌ No se permiten valores negativos.")
            else:
                return valor
        except ValueError:
            pantalla.imprimir_centrado("❌ Entrada inválida. Intente de nuevo.")

def mensaje_resultado(mensaje, exito=True):
    icono = "✅" if exito else "❌"
    pantalla.imprimir_centrado(f"{icono} {mensaje}")

# ─────────────────────────────────────────────
# Captura de datos
# ─────────────────────────────────────────────

def solicitar_datos_producto(predefinido=None):
    p = {}
    p["nombre"] = input_texto_requerido("Nombre del producto", predefinido["nombre"] if predefinido else "")
    p["categoria"] = input_texto_requerido("Categoría (anillo, collar, etc.)", predefinido["categoria"] if predefinido else "")
    p["material"] = input_texto_requerido("Material (oro, plata, etc.)", predefinido["material"] if predefinido else "")
    p["precio_compra"] = input_numerico_centrado("Precio de compra", float, predefinido["precio_compra"] if predefinido else 0)
    p["precio_venta"] = input_numerico_centrado("Precio de venta", float, predefinido["precio_venta"] if predefinido else 0)
    p["stock"] = input_numerico_centrado("Cantidad en stock", int, predefinido["stock"] if predefinido else 0)
    return p

# ─────────────────────────────────────────────
# Menú principal del módulo Inventario
# ─────────────────────────────────────────────

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
                mensaje_resultado("Opción no válida.", exito=False)
                pantalla.pausar()

# ─────────────────────────────────────────────
# Funciones principales del Inventario
# ─────────────────────────────────────────────

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
        pantalla.imprimir_centrado("-" * len(header))
        pantalla.imprimir_centrado(f"📦 Total de productos: {len(productos)}")
    pantalla.pausar()

def agregar_producto():
    mostrar_titulo("Agregar nuevo producto", "➕")
    datos = solicitar_datos_producto()
    if datos:
        datos["id"] = generar_id()
        productos.append(datos)
        mensaje_resultado(f"Producto '{datos['nombre']}' ID {datos['id']} agregado correctamente.")
    pantalla.pausar()

def editar_producto():
    mostrar_titulo("Editar producto", "✏️")
    try:
        prod_id = int(input_centrado("Ingrese el ID del producto a editar"))
    except ValueError:
        mensaje_resultado("ID inválido.", exito=False)
        pantalla.pausar()
        return

    producto = buscar_producto_por_id(prod_id)
    if not producto:
        mensaje_resultado("Producto no encontrado.", exito=False)
        pantalla.pausar()
        return

    datos = solicitar_datos_producto(predefinido=producto)
    if datos:
        producto.update(datos)
        mensaje_resultado("Producto actualizado correctamente.")
    pantalla.pausar()

def buscar_producto():
    mostrar_titulo("Buscar producto", "🔍")
    termino = input_centrado("Ingrese ID o parte del nombre").lower()
    
    if termino.isdigit():
        encontrado = buscar_producto_por_id(int(termino))
        if encontrado:
            linea = f"ID: {encontrado['id']} | Nombre: {encontrado['nombre']} | Precio: ${encontrado['precio_venta']:.2f} | Stock: {encontrado['stock']}"
            pantalla.imprimir_centrado(linea)
        else:
            mensaje_resultado("Producto no encontrado.", exito=False)
    else:
        encontrados = [p for p in productos if termino in p['nombre'].lower()]
        if encontrados:
            for p in encontrados:
                linea = f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio_venta']:.2f} | Stock: {p['stock']}"
                pantalla.imprimir_centrado(linea)
        else:
            mensaje_resultado("No se encontraron productos.", exito=False)
    pantalla.pausar()

def eliminar_producto():
    mostrar_titulo("Eliminar producto", "🗑️")
    try:
        prod_id = int(input_centrado("Ingrese el ID del producto a eliminar"))
    except ValueError:
        mensaje_resultado("ID inválido.", exito=False)
        pantalla.pausar()
        return

    producto = buscar_producto_por_id(prod_id)
    if producto:
        productos.remove(producto)
        mensaje_resultado(f"Producto '{producto['nombre']}' eliminado.")
    else:
        mensaje_resultado("Producto no encontrado.", exito=False)
    pantalla.pausar()

def restablecer_inventario():
    mostrar_titulo("Restablecer inventario", "🧹")
    confirm = input_centrado("¿Está seguro que desea eliminar todo? (s/n)").lower()
    if confirm == 's':
        productos.clear()
        mensaje_resultado("Inventario restablecido.")
    else:
        mensaje_resultado("Operación cancelada.")
    pantalla.pausar()
