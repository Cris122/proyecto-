import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import (
    mostrar_menu, mostrar_mensaje, mostrar_titulo, mostrar_tabla, mostrar_progreso,
    input_seguro, input_entero, input_flotante, confirmar_accion,
    buscar_en_lista, buscar_en_lista_por_parcial, solicitar_datos_generico,
    obtener_elemento_por_input, confirmar_accion_destructiva
)

# productos se pasa ahora desde main.py
# def generar_id():
#     return max((p["id"] for p in productos), default=0) + 1

# def buscar_producto_por_id(pid):
#     return buscar_en_lista(productos, "id", pid)

def menu_inventario(productos):
    opciones = [
        ("1", "📦 Ver inventario"),
        ("2", "➕ Agregar producto"), 
        ("3", "✏️ Editar producto"),
        ("4", "🔍 Buscar producto"),
        ("5", "🗑️ Eliminar producto"),
        ("6", "🧹 Restablecer inventario"),
        ("0", "🔙 Volver al menú principal")
    ]

    while True:
        opcion = mostrar_menu("MENÚ DE INVENTARIO", opciones, "🧾 GESTIÓN DE PRODUCTOS 🧾")
        
        match opcion:
            case "1": ver_inventario(productos)
            case "2": agregar_producto(productos)
            case "3": editar_producto(productos)
            case "4": buscar_producto(productos)
            case "5": eliminar_producto(productos)
            case "6": restablecer_inventario(productos)
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def ver_inventario(productos):
    mostrar_titulo("📦 INVENTARIO ACTUAL")
    
    if not productos:
        mostrar_mensaje("El inventario está vacío.", "info")
        return

    headers = [
        ("id", "ID", 5),
        ("nombre", "Nombre", 20),
        ("categoria", "Categoría", 12),
        ("material", "Material", 10),
        ("precio_compra", "Compra ($)", 12),
        ("precio_venta", "Venta ($)", 12),
        ("stock", "Stock", 6)
    ]

    # Formatear precios
    datos_formateados = []
    for p in productos:
        producto_formato = p.copy()
        producto_formato["precio_compra"] = f"${p['precio_compra']:.2f}"
        producto_formato["precio_venta"] = f"${p['precio_venta']:.2f}"
        datos_formateados.append(producto_formato)

    mostrar_tabla(datos_formateados, headers, f"Total de productos: {len(productos)}")
    mostrar_mensaje(f"Total de productos: {len(productos)}", "info", pausar_despues=True)

def agregar_producto(productos):
    # Definición de campos para solicitar_datos_generico
    campos_producto = [
        ("Nombre del producto", "nombre", "texto", None, None, None),
        ("Categoría (anillo, collar, etc.)", "categoria", "texto", None, None, None), 
        ("Material (oro, plata, etc.)", "material", "texto", None, None, None),
        ("Precio de compra", "precio_compra", "flotante", None, 0, None),
        ("Precio de venta", "precio_venta", "flotante", None, 0, None),
        ("Cantidad en stock", "stock", "entero", None, 0, None)
    ]

    datos = solicitar_datos_generico("➕ AGREGAR NUEVO PRODUCTO", campos_producto)
    
    if datos:
        # Generar ID aquí, ya que 'productos' está disponible
        new_id = max((p["id"] for p in productos), default=0) + 1
        datos["id"] = new_id
        productos.append(datos)
        mostrar_mensaje(f"Producto '{datos['nombre']}' (ID: {datos['id']}) agregado correctamente.", "success")
    else:
        mostrar_mensaje("Operación cancelada. No se agregó ningún producto.", "warn")

def editar_producto(productos):
    mostrar_titulo("✏️ EDITAR PRODUCTO")
    
    # Usar la función plantilla para obtener el producto
    producto = obtener_elemento_por_input(
        productos,
        "producto",
        lambda: input_entero("Ingrese el ID del producto a editar"),
        lambda pid: buscar_en_lista(productos, "id", pid),
        "Producto no encontrado."
    )
    if not producto:
        mostrar_mensaje("Operación cancelada.", "warn")
        return

    # Definición de campos para solicitar_datos_generico
    campos_producto = [
        ("Nombre del producto", "nombre", "texto", None, None, None),
        ("Categoría (anillo, collar, etc.)", "categoria", "texto", None, None, None), 
        ("Material (oro, plata, etc.)", "material", "texto", None, None, None),
        ("Precio de compra", "precio_compra", "flotante", None, 0, None),
        ("Precio de venta", "precio_venta", "flotante", None, 0, None),
        ("Cantidad en stock", "stock", "entero", None, 0, None)
    ]

    datos_actualizados = solicitar_datos_generico("✏️ EDITAR PRODUCTO", campos_producto, datos_existentes=producto.copy())
    if datos_actualizados:
        producto.update(datos_actualizados)
        mostrar_mensaje("Producto actualizado correctamente.", "success")
    else:
        mostrar_mensaje("Operación cancelada. No se realizaron cambios.", "warn")

def buscar_producto(productos):
    mostrar_titulo("🔍 BUSCAR PRODUCTO")
    
    termino = input_seguro("Ingrese ID o parte del nombre del producto")
    if termino is None:
        return

    # Buscar por ID si es número
    if termino.isdigit():
        encontrados = [buscar_en_lista(productos, "id", int(termino))]
        encontrados = [p for p in encontrados if p is not None] # Filtrar None si no se encontró
    else:
        # Buscar por nombre parcial
        encontrados = buscar_en_lista_por_parcial(productos, "nombre", termino)

    if encontrados:
        headers = [
            ("id", "ID", 5),
            ("nombre", "Nombre", 25),
            ("precio_venta", "Precio ($)", 12),
            ("stock", "Stock", 6)
        ]
        
        datos_formateados = []
        for p in encontrados:
            producto_formato = p.copy()
            producto_formato["precio_venta"] = f"${p['precio_venta']:.2f}"
            datos_formateados.append(producto_formato)
            
        mostrar_tabla(datos_formateados, headers, f"Productos encontrados: {len(encontrados)}")
    else:
        mostrar_mensaje("No se encontraron productos con ese criterio.", "error")

def eliminar_producto(productos):
    mostrar_titulo("🗑️ ELIMINAR PRODUCTO")
    
    # Usar la función plantilla para obtener el producto
    producto = obtener_elemento_por_input(
        productos,
        "producto",
        lambda: input_entero("Ingrese el ID del producto a eliminar"),
        lambda pid: buscar_en_lista(productos, "id", pid),
        "Producto no encontrado."
    )
    if not producto:
        mostrar_mensaje("Operación cancelada.", "warn")
        return

    # Mostrar información del producto
    mostrar_titulo("⚠️ CONFIRMAR ELIMINACIÓN")
    datos_producto = {
        "ID": producto["id"],
        "Nombre": producto["nombre"],
        "Precio": f"${producto['precio_venta']:.2f}",
        "Stock": producto["stock"]
    }
    mostrar_progreso(datos_producto)

    if confirmar_accion(f"¿Está seguro que desea eliminar el producto '{producto['nombre']}'? (s/n): "):
        productos.remove(producto)
        mostrar_mensaje(f"Producto '{producto['nombre']}' eliminado correctamente.", "success")
    else:
        mostrar_mensaje("Operación cancelada.", "warn")

def restablecer_inventario(productos):
    mostrar_titulo("🧹 RESTABLECER INVENTARIO")
    
    if not productos:
        mostrar_mensaje("El inventario ya está vacío.", "info")
        return
        
    if confirmar_accion_destructiva(
        "⚠️ ADVERTENCIA: Esta acción eliminará TODOS los productos del inventario. ¡Esta acción es irreversible!",
        "ELIMINAR TODO"
    ):
        cantidad_eliminada = len(productos)
        productos.clear()
        mostrar_mensaje(f"Inventario restablecido. Se eliminaron {cantidad_eliminada} productos.", "success")
    else:
        mostrar_mensaje("Operación cancelada.", "warn")

