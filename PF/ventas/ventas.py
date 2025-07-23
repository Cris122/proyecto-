import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import *
from conexionBD import conexion, cursor
# Importar funciones de búsqueda de productos y clientes desde sus módulos
from inventario.inventario import buscar_producto_por_id_db, obtener_todos_los_productos_db
from clientes.clientes import buscar_cliente_por_correo_db

# Funciones de interacción con la base de datos para ventas
def obtener_todas_las_ventas_db():
    try:
        sql = """
        SELECT v.id, v.fecha, c.nombre AS cliente_nombre, c.correo AS cliente_correo,
               p.nombre AS producto_nombre, v.cantidad, v.precio_unitario, v.total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
        """
        cursor.execute(sql)
        ventas_data = cursor.fetchall()
        lista_ventas = []
        for venta_row in ventas_data:
            lista_ventas.append({
                "id": venta_row[0],
                "fecha": venta_row[1].strftime("%d/%m/%Y %H:%M:%S"), # Formatear datetime
                "cliente": venta_row[2],
                "correo": venta_row[3],
                "producto": venta_row[4],
                "cantidad": venta_row[5],
                "precio_unitario": float(venta_row[6]),
                "total": float(venta_row[7])
            })
        return lista_ventas
    except Exception as e:
        mostrar_mensaje(f"Error al obtener ventas: {e}", "error")
        return []

def buscar_venta_por_id_db(vid):
    try:
        sql = """
        SELECT v.id, v.fecha, c.nombre AS cliente_nombre, c.correo AS cliente_correo,
               p.nombre AS producto_nombre, v.cantidad, v.precio_unitario, v.total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN productos p ON v.producto_id = p.id
        WHERE v.id = %s
        """
        cursor.execute(sql, (vid,))
        venta_data = cursor.fetchone()
        if venta_data:
            return {
                "id": venta_data[0],
                "fecha": venta_data[1].strftime("%d/%m/%Y %H:%M:%S"),
                "cliente": venta_data[2],
                "correo": venta_data[3],
                "producto": venta_data[4],
                "cantidad": venta_data[5],
                "precio_unitario": float(venta_data[6]),
                "total": float(venta_data[7])
            }
        return None
    except Exception as e:
        mostrar_mensaje(f"Error al buscar venta por ID: {e}", "error")
        return None

def buscar_ventas_por_cliente_parcial_db(termino):
    try:
        sql = """
        SELECT v.id, v.fecha, c.nombre AS cliente_nombre, c.correo AS cliente_correo,
               p.nombre AS producto_nombre, v.cantidad, v.precio_unitario, v.total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN productos p ON v.producto_id = p.id
        WHERE c.nombre LIKE %s
        ORDER BY v.fecha DESC
        """
        cursor.execute(sql, (f"%{termino}%",))
        ventas_data = cursor.fetchall()
        lista_ventas = []
        for venta_row in ventas_data:
            lista_ventas.append({
                "id": venta_row[0],
                "fecha": venta_row[1].strftime("%d/%m/%Y %H:%M:%S"),
                "cliente": venta_row[2],
                "correo": venta_row[3],
                "producto": venta_row[4],
                "cantidad": venta_row[5],
                "precio_unitario": float(venta_row[6]),
                "total": float(venta_row[7])
            })
        return lista_ventas
    except Exception as e:
        mostrar_mensaje(f"Error al buscar ventas por cliente: {e}", "error")
        return []

def menu_ventas(): # Ya no necesita productos, lista_clientes, ventas_realizadas como parámetros
    opciones = [
        ("1", "🛒 Registrar venta"),
        ("2", "📜 Ver historial"),
        ("3", "📊 Ver estadísticas"),
        ("4", "🔍 Buscar venta"),
        ("0", "🔙 Volver al menú principal")
    ]
    
    while True:
        opcion = mostrar_menu("MENÚ DE VENTAS", opciones, "💰 GESTIÓN DE VENTAS 💰")
        
        match opcion:
            case "1": registrar_venta()
            case "2": ver_historial()
            case "3": ver_estadisticas()
            case "4": buscar_venta()
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def obtener_productos_disponibles(): # Obtiene de la DB
    return [p for p in obtener_todos_los_productos_db() if p["stock"] > 0]

def mostrar_productos_disponibles_para_venta(): # Adaptado para la DB
    productos_stock = obtener_productos_disponibles()
    
    if not productos_stock:
        mostrar_mensaje("No hay productos disponibles en stock.", "error")
        return False
    
    headers = [
        ("id", "ID", 5),
        ("nombre", "Nombre", 25),
        ("precio_venta", "Precio ($)", 12),
        ("stock", "Stock", 8)
    ]
    
    # Formatear precios
    datos_formateados = []
    for p in productos_stock:
        producto_formato = p.copy()
        producto_formato["precio_venta"] = f"${p['precio_venta']:.2f}"
        datos_formateados.append(producto_formato)
    
    mostrar_tabla(datos_formateados, headers, "PRODUCTOS DISPONIBLES")
    return True

def obtener_o_crear_cliente(correo): # Adaptado para la DB
    cliente = buscar_cliente_por_correo_db(correo)
    
    if cliente:
        mostrar_mensaje(f"Cliente encontrado: {cliente['nombre']}", "success", pausar_despues=False)
        return cliente
    
    # Cliente no existe, crear uno nuevo
    mostrar_titulo("🆕 NUEVO CLIENTE")
    nombre = input_seguro("Nombre del cliente")
    if not nombre:
        return None
    
    try:
        sql = "INSERT INTO clientes (nombre, correo) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, correo.lower()))
        conexion.commit()
        # Obtener el ID del cliente recién insertado
        cliente_id = cursor.lastrowid
        mostrar_mensaje(f"Cliente '{nombre}' registrado correctamente.", "success")
        return {"id": cliente_id, "nombre": nombre, "correo": correo.lower()}
    except Exception as e:
        conexion.rollback()
        mostrar_mensaje(f"Error al registrar nuevo cliente: {e}", "error")
        return None

def registrar_venta(): # Ya no necesita productos, lista_clientes, ventas_realizadas como parámetros
    mostrar_titulo("🛒 REGISTRAR NUEVA VENTA")
    
    # Verificar productos disponibles
    if not mostrar_productos_disponibles_para_venta():
        return
    
    # Obtener correo del cliente
    correo = input_seguro("Correo electrónico del cliente", validar_email)
    if not correo:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Obtener o crear cliente
    cliente = obtener_o_crear_cliente(correo)
    if not cliente:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Seleccionar producto
    producto = obtener_elemento_por_input(
        "producto",
        lambda: input_entero("ID del producto a vender"),
        buscar_producto_por_id_db, # Función de búsqueda en DB
        "Producto no encontrado."
    )
    if not producto:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    if producto["stock"] <= 0:
        mostrar_mensaje("Producto sin stock disponible.", "error")
        return
    
    # Solicitar cantidad
    cantidad = input_entero(f"Cantidad a vender (Stock disponible: {producto['stock']})", 
                           min_val=1, max_val=producto["stock"])
    if cantidad is None:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Calcular total y mostrar resumen
    total = producto["precio_venta"] * cantidad
    
    mostrar_titulo("📋 RESUMEN DE VENTA")
    resumen = {
        "Cliente": cliente["nombre"],
        "Correo": cliente["correo"],
        "Producto": producto["nombre"],
        "Precio unitario": f"${producto['precio_venta']:.2f}",
        "Cantidad": cantidad,
        "Total a pagar": f"${total:.2f}"
    }
    mostrar_progreso(resumen)
    
    # Confirmar venta
    if not confirmar_accion("¿Confirmar la venta? (s/n): "):
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Procesar venta en la base de datos
    try:
        # 1. Registrar la venta
        sql_venta = """
        INSERT INTO ventas (fecha, cliente_id, producto_id, cantidad, precio_unitario, total)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_venta, (
            datetime.now(), cliente["id"], producto["id"], cantidad,
            producto["precio_venta"], total
        ))
        venta_id = cursor.lastrowid # Obtener el ID de la venta recién insertada

        # 2. Actualizar el stock del producto
        sql_update_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
        cursor.execute(sql_update_stock, (cantidad, producto["id"]))
        
        conexion.commit() # Confirmar ambas operaciones
        
        # Actualizar el stock en el objeto producto para mostrarlo
        producto["stock"] -= cantidad

        mostrar_titulo("✅ VENTA EXITOSA")
        resultado = {
            "ID de venta": f"#{venta_id}",
            "Total cobrado": f"${total:.2f}",
            "Stock restante": f"{producto['stock']} unidades"
        }
        mostrar_progreso(resultado)
        mostrar_mensaje("¡Venta registrada correctamente!", "success")

    except Exception as e:
        conexion.rollback() # Revertir si algo falla
        mostrar_mensaje(f"Error al registrar venta: {e}", "error")
    finally:
        pausar()

def ver_historial(): # Ya no necesita ventas_realizadas como parámetro
    mostrar_titulo("📜 HISTORIAL DE VENTAS")
    
    ventas_realizadas_db = obtener_todas_las_ventas_db()
    
    if not ventas_realizadas_db:
        mostrar_mensaje("No hay ventas registradas.", "info")
        return
    
    headers = [
        ("id", "ID", 4),
        ("fecha", "Fecha", 17),
        ("cliente", "Cliente", 20),
        ("producto", "Producto", 25),
        ("cantidad", "Cant.", 5),
        ("total", "Total ($)", 10)
    ]
    
    # Formatear datos
    datos_formateados = []
    for v in ventas_realizadas_db:
        venta_formato = v.copy()
        venta_formato["total"] = f"${v['total']:.2f}"
        datos_formateados.append(venta_formato)
    
    total_ventas = sum(v['total'] for v in ventas_realizadas_db)
    mostrar_tabla(datos_formateados, headers, 
                 f"Total recaudado: ${total_ventas:.2f} | Ventas realizadas: {len(ventas_realizadas_db)}")
    mostrar_mensaje(f"Total recaudado: ${total_ventas:.2f} | Ventas realizadas: {len(ventas_realizadas_db)}", "info", pausar_despues=True)

def ver_estadisticas(): # Ya no necesita ventas_realizadas como parámetro
    mostrar_titulo("📊 ESTADÍSTICAS DE VENTAS")
    
    ventas_realizadas_db = obtener_todas_las_ventas_db()
    
    if not ventas_realizadas_db:
        mostrar_mensaje("No hay ventas registradas para mostrar estadísticas.", "info")
        return
    
    # Cálculos generales
    total_recaudado = sum(v['total'] for v in ventas_realizadas_db)
    promedio_venta = total_recaudado / len(ventas_realizadas_db) if ventas_realizadas_db else 0
    total_productos_vendidos = sum(v['cantidad'] for v in ventas_realizadas_db)
    
    # Producto más vendido
    productos_cantidad = {}
    for v in ventas_realizadas_db:
        productos_cantidad[v['producto']] = productos_cantidad.get(v['producto'], 0) + v['cantidad']
    
    producto_estrella = max(productos_cantidad.items(), key=lambda x: x[1]) if productos_cantidad else ("N/A", 0)
    
    # Mejor cliente
    clientes_total = {}
    for v in ventas_realizadas_db:
        clientes_total[v['cliente']] = clientes_total.get(v['cliente'], 0) + v['total']
    
    mejor_cliente = max(clientes_total.items(), key=lambda x: x[1]) if clientes_total else ("N/A", 0)
    
    # Mostrar estadísticas
    estadisticas = {
        "💰 RESUMEN FINANCIERO": "",
        "Total recaudado": f"${total_recaudado:.2f}",
        "Ventas realizadas": len(ventas_realizadas_db),
        "Promedio por venta": f"${promedio_venta:.2f}",
        "Productos vendidos": f"{total_productos_vendidos} unidades",
        "": "",
        "🏆 RANKINGS": "",
        "Producto más vendido": f"{producto_estrella[0]} ({producto_estrella[1]} unidades)",
        "Mejor cliente": f"{mejor_cliente[0]} (${mejor_cliente[1]:.2f})"
    }
    
    mostrar_progreso(estadisticas)
    mostrar_mensaje("Estadísticas mostradas.", "info", pausar_despues=True)

def buscar_venta(): # Ya no necesita ventas_realizadas como parámetro
    mostrar_titulo("🔍 BUSCAR VENTAS")
    
    ventas_realizadas_db = obtener_todas_las_ventas_db()
    if not ventas_realizadas_db:
        mostrar_mensaje("No hay ventas registradas.", "info")
        return
    
    termino = input_seguro("Ingrese ID de venta o nombre de cliente")
    if not termino:
        return
    
    encontradas = []
    # Buscar por ID si es número
    if termino.isdigit():
        venta_encontrada = buscar_venta_por_id_db(int(termino))
        if venta_encontrada:
            encontradas.append(venta_encontrada)
    else:
        # Buscar por nombre de cliente
        encontradas = buscar_ventas_por_cliente_parcial_db(termino)
    
    if encontradas:
        headers = [
            ("id", "ID", 4),
            ("fecha", "Fecha", 17),
            ("cliente", "Cliente", 20),
            ("producto", "Producto", 25),
            ("total", "Total ($)", 10)
        ]
        
        # Formatear datos
        datos_formateados = []
        for v in encontradas:
            venta_formato = v.copy()
            venta_formato["total"] = f"${v['total']:.2f}"
            datos_formateados.append(venta_formato)
        
        mostrar_tabla(datos_formateados, headers, f"Ventas encontradas: {len(encontradas)}")
    else:
        mostrar_mensaje("No se encontraron ventas con ese criterio.", "error")
    pausar()
