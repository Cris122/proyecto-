import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import *
from conexionBD import conexion, cursor

# Funciones de interacción con la base de datos para productos
def buscar_producto_por_id_db(pid):
    try:
        cursor.execute("SELECT id, nombre, categoria, material, precio_compra, precio_venta, stock FROM productos WHERE id = %s", (pid,))
        producto_data = cursor.fetchone()
        if producto_data:
            return {
                "id": producto_data[0],
                "nombre": producto_data[1],
                "categoria": producto_data[2],
                "material": producto_data[3],
                "precio_compra": float(producto_data[4]),
                "precio_venta": float(producto_data[5]),
                "stock": producto_data[6]
            }
        return None
    except Exception as e:
        mostrar_mensaje(f"Error al buscar producto por ID: {e}", "error")
        return None

def buscar_productos_por_nombre_parcial_db(termino):
    try:
        cursor.execute("SELECT id, nombre, categoria, material, precio_compra, precio_venta, stock FROM productos WHERE nombre LIKE %s", (f"%{termino}%",))
        productos_data = cursor.fetchall()
        lista_productos = []
        for prod_row in productos_data:
            lista_productos.append({
                "id": prod_row[0],
                "nombre": prod_row[1],
                "categoria": prod_row[2],
                "material": prod_row[3],
                "precio_compra": float(prod_row[4]),
                "precio_venta": float(prod_row[5]),
                "stock": prod_row[6]
            })
        return lista_productos
    except Exception as e:
        mostrar_mensaje(f"Error al buscar productos por nombre: {e}", "error")
        return []

def obtener_todos_los_productos_db():
    try:
        cursor.execute("SELECT id, nombre, categoria, material, precio_compra, precio_venta, stock FROM productos")
        productos_data = cursor.fetchall()
        lista_productos = []
        for prod_row in productos_data:
            lista_productos.append({
                "id": prod_row[0],
                "nombre": prod_row[1],
                "categoria": prod_row[2],
                "material": prod_row[3],
                "precio_compra": float(prod_row[4]),
                "precio_venta": float(prod_row[5]),
                "stock": prod_row[6]
            })
        return lista_productos
    except Exception as e:
        mostrar_mensaje(f"Error al obtener productos: {e}", "error")
        return []

def menu_inventario(): # Ya no necesita productos como parámetro
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
            case "1": ver_inventario()
            case "2": agregar_producto()
            case "3": editar_producto()
            case "4": buscar_producto()
            case "5": eliminar_producto()
            case "6": restablecer_inventario()
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def ver_inventario(): # Ya no necesita productos como parámetro
    mostrar_titulo("📦 INVENTARIO ACTUAL")
    
    productos_db = obtener_todos_los_productos_db() # Obtener productos de la DB
    
    if not productos_db:
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
    for p in productos_db:
        producto_formato = p.copy()
        producto_formato["precio_compra"] = f"${p['precio_compra']:.2f}"
        producto_formato["precio_venta"] = f"${p['precio_venta']:.2f}"
        datos_formateados.append(producto_formato)

    mostrar_tabla(datos_formateados, headers, f"Total de productos: {len(productos_db)}")
    mostrar_mensaje(f"Total de productos: {len(productos_db)}", "info", pausar_despues=True)

def agregar_producto(): # Ya no necesita productos como parámetro
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
        try:
            sql = """
            INSERT INTO productos (nombre, categoria, material, precio_compra, precio_venta, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                datos["nombre"], datos["categoria"], datos["material"],
                datos["precio_compra"], datos["precio_venta"], datos["stock"]
            ))
            conexion.commit()
            mostrar_mensaje(f"Producto '{datos['nombre']}' agregado correctamente.", "success")
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al agregar producto: {e}", "error")
        finally:
            pausar()
    else:
        mostrar_mensaje("Operación cancelada. No se agregó ningún producto.", "warn")
        pausar()

def editar_producto(): # Ya no necesita productos como parámetro
    mostrar_titulo("✏️ EDITAR PRODUCTO")
    
    # Usar la función plantilla para obtener el producto de la DB
    producto = obtener_elemento_por_input(
        "producto",
        lambda: input_entero("Ingrese el ID del producto a editar"),
        buscar_producto_por_id_db, # Función de búsqueda en DB
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
        try:
            sql = """
            UPDATE productos SET
                nombre = %s, categoria = %s, material = %s,
                precio_compra = %s, precio_venta = %s, stock = %s
            WHERE id = %s
            """
            cursor.execute(sql, (
                datos_actualizados["nombre"], datos_actualizados["categoria"], datos_actualizados["material"],
                datos_actualizados["precio_compra"], datos_actualizados["precio_venta"], datos_actualizados["stock"],
                producto["id"]
            ))
            conexion.commit()
            mostrar_mensaje("Producto actualizado correctamente.", "success")
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al actualizar producto: {e}", "error")
        finally:
            pausar()
    else:
        mostrar_mensaje("Operación cancelada. No se realizaron cambios.", "warn")
        pausar()

def buscar_producto(): # Ya no necesita productos como parámetro
    mostrar_titulo("🔍 BUSCAR PRODUCTO")
    
    termino = input_seguro("Ingrese ID o parte del nombre del producto")
    if termino is None:
        return

    encontrados = []
    # Buscar por ID si es número
    if termino.isdigit():
        producto_encontrado = buscar_producto_por_id_db(int(termino))
        if producto_encontrado:
            encontrados.append(producto_encontrado)
    else:
        # Buscar por nombre parcial
        encontrados = buscar_productos_por_nombre_parcial_db(termino)

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
    pausar()

def eliminar_producto(): # Ya no necesita productos como parámetro
    mostrar_titulo("🗑️ ELIMINAR PRODUCTO")
    
    # Usar la función plantilla para obtener el producto de la DB
    producto = obtener_elemento_por_input(
        "producto",
        lambda: input_entero("Ingrese el ID del producto a eliminar"),
        buscar_producto_por_id_db, # Función de búsqueda en DB
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
        try:
            # Primero, verificar si el producto tiene ventas asociadas
            cursor.execute("SELECT COUNT(*) FROM ventas WHERE producto_id = %s", (producto['id'],))
            if cursor.fetchone()[0] > 0:
                mostrar_mensaje("No se puede eliminar el producto porque tiene ventas registradas.", "error")
                pausar()
                return

            sql = "DELETE FROM productos WHERE id = %s"
            cursor.execute(sql, (producto["id"],))
            conexion.commit()
            mostrar_mensaje(f"Producto '{producto['nombre']}' eliminado correctamente.", "success")
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al eliminar producto: {e}", "error")
        finally:
            pausar()
    else:
        mostrar_mensaje("Operación cancelada.", "warn")
        pausar()

def restablecer_inventario(): # Ya no necesita productos como parámetro
    mostrar_titulo("🧹 RESTABLECER INVENTARIO")
    
    productos_db = obtener_todos_los_productos_db()
    if not productos_db:
        mostrar_mensaje("El inventario ya está vacío.", "info")
        return
        
    if confirmar_accion_destructiva(
        "⚠️ ADVERTENCIA: Esta acción eliminará TODOS los productos del inventario. ¡Esta acción es irreversible!",
        "ELIMINAR TODO"
    ):
        try:
            # Verificar si hay ventas asociadas a algún producto
            cursor.execute("SELECT COUNT(*) FROM ventas")
            if cursor.fetchone()[0] > 0:
                mostrar_mensaje("No se puede restablecer el inventario porque hay ventas registradas.", "error")
                mostrar_mensaje("Elimine las ventas primero si desea restablecer el inventario.", "info")
                pausar()
                return

            cursor.execute("DELETE FROM productos")
            conexion.commit()
            mostrar_mensaje(f"Inventario restablecido. Se eliminaron {len(productos_db)} productos.", "success")
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al restablecer inventario: {e}", "error")
        finally:
            pausar()
    else:
        mostrar_mensaje("Operación cancelada.", "warn")
        pausar()
