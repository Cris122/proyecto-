import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import (
    mostrar_menu, mostrar_mensaje, mostrar_titulo, mostrar_tabla, mostrar_progreso,
    input_seguro, input_entero, confirmar_accion, validar_email,
    buscar_en_lista, buscar_en_lista_por_parcial, obtener_elemento_por_input
)

# Las listas se pasan ahora desde main.py
# from inventario.inventario import productos, buscar_producto_por_id
# from clientes.clientes import lista_clientes

# ventas_realizadas se pasa ahora desde main.py

# def buscar_cliente_por_correo(correo):
#     return buscar_en_lista(lista_clientes, "correo", correo.lower())

def menu_ventas(productos, lista_clientes, ventas_realizadas):
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
            case "1": registrar_venta(productos, lista_clientes, ventas_realizadas)
            case "2": ver_historial(ventas_realizadas)
            case "3": ver_estadisticas(ventas_realizadas)
            case "4": buscar_venta(ventas_realizadas)
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def obtener_productos_disponibles(productos):
    return [p for p in productos if p["stock"] > 0]

def mostrar_productos_disponibles(productos):
    productos_stock = obtener_productos_disponibles(productos)
    
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

def obtener_cliente(correo, lista_clientes):
    cliente = buscar_en_lista(lista_clientes, "correo", correo.lower())
    
    if cliente:
        mostrar_mensaje(f"Cliente encontrado: {cliente['nombre']}", "success", pausar_despues=False)
        return cliente
    
    # Cliente no existe, crear uno nuevo
    mostrar_titulo("🆕 NUEVO CLIENTE")
    nombre = input_seguro("Nombre del cliente")
    if not nombre:
        return None
    
    cliente = {
        "nombre": nombre,
        "correo": correo.lower(),
        "compras": []
    }
    lista_clientes.append(cliente)
    mostrar_mensaje(f"Cliente '{nombre}' registrado correctamente.", "success")
    return cliente

def registrar_venta(productos, lista_clientes, ventas_realizadas):
    mostrar_titulo("🛒 REGISTRAR NUEVA VENTA")
    
    # Verificar productos disponibles
    if not mostrar_productos_disponibles(productos):
        return
    
    # Obtener correo del cliente
    correo = input_seguro("Correo electrónico del cliente", validar_email)
    if not correo:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Obtener o crear cliente
    cliente = obtener_cliente(correo, lista_clientes)
    if not cliente:
        mostrar_mensaje("Venta cancelada.", "warn")
        return
    
    # Seleccionar producto
    producto = obtener_elemento_por_input(
        productos,
        "producto",
        lambda: input_entero("ID del producto a vender"),
        lambda pid: buscar_en_lista(productos, "id", pid),
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
    
    # Procesar venta
    producto["stock"] -= cantidad
    cliente["compras"].append(total)
    
    venta = {
        "id": len(ventas_realizadas) + 1,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cliente": cliente["nombre"],
        "correo": cliente["correo"],
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio_venta"],
        "total": total
    }
    
    ventas_realizadas.append(venta)
    
    mostrar_titulo("✅ VENTA EXITOSA")
    resultado = {
        "ID de venta": f"#{venta['id']}",
        "Total cobrado": f"${total:.2f}",
        "Stock restante": f"{producto['stock']} unidades"
    }
    mostrar_progreso(resultado)
    mostrar_mensaje("¡Venta registrada correctamente!", "success")

def ver_historial(ventas_realizadas):
    mostrar_titulo("📜 HISTORIAL DE VENTAS")
    
    if not ventas_realizadas:
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
    for v in ventas_realizadas:
        venta_formato = v.copy()
        venta_formato["total"] = f"${v['total']:.2f}"
        datos_formateados.append(venta_formato)
    
    total_ventas = sum(v['total'] for v in ventas_realizadas)
    mostrar_tabla(datos_formateados, headers, 
                 f"Total recaudado: ${total_ventas:.2f} | Ventas realizadas: {len(ventas_realizadas)}")
    mostrar_mensaje(f"Total recaudado: ${total_ventas:.2f} | Ventas realizadas: {len(ventas_realizadas)}", "info", pausar_despues=True)

def ver_estadisticas(ventas_realizadas):
    mostrar_titulo("📊 ESTADÍSTICAS DE VENTAS")
    
    if not ventas_realizadas:
        mostrar_mensaje("No hay ventas registradas para mostrar estadísticas.", "info")
        return
    
    # Cálculos generales
    total_recaudado = sum(v['total'] for v in ventas_realizadas)
    promedio_venta = total_recaudado / len(ventas_realizadas) if ventas_realizadas else 0
    total_productos_vendidos = sum(v['cantidad'] for v in ventas_realizadas)
    
    # Producto más vendido
    productos_cantidad = {}
    for v in ventas_realizadas:
        productos_cantidad[v['producto']] = productos_cantidad.get(v['producto'], 0) + v['cantidad']
    
    producto_estrella = max(productos_cantidad.items(), key=lambda x: x[1]) if productos_cantidad else ("N/A", 0)
    
    # Mejor cliente
    clientes_total = {}
    for v in ventas_realizadas:
        clientes_total[v['cliente']] = clientes_total.get(v['cliente'], 0) + v['total']
    
    mejor_cliente = max(clientes_total.items(), key=lambda x: x[1]) if clientes_total else ("N/A", 0)
    
    # Mostrar estadísticas
    estadisticas = {
        "💰 RESUMEN FINANCIERO": "",
        "Total recaudado": f"${total_recaudado:.2f}",
        "Ventas realizadas": len(ventas_realizadas),
        "Promedio por venta": f"${promedio_venta:.2f}",
        "Productos vendidos": f"{total_productos_vendidos} unidades",
        "": "",
        "🏆 RANKINGS": "",
        "Producto más vendido": f"{producto_estrella[0]} ({producto_estrella[1]} unidades)",
        "Mejor cliente": f"{mejor_cliente[0]} (${mejor_cliente[1]:.2f})"
    }
    
    mostrar_progreso(estadisticas)
    mostrar_mensaje("Estadísticas mostradas.", "info", pausar_despues=True)

def buscar_venta(ventas_realizadas):
    mostrar_titulo("🔍 BUSCAR VENTAS")
    
    if not ventas_realizadas:
        mostrar_mensaje("No hay ventas registradas.", "info")
        return
    
    termino = input_seguro("Ingrese ID de venta o nombre de cliente")
    if not termino:
        return
    
    # Buscar por ID si es número
    if termino.isdigit():
        encontradas = [v for v in ventas_realizadas if v['id'] == int(termino)]
    else:
        # Buscar por nombre de cliente
        encontradas = buscar_en_lista_por_parcial(ventas_realizadas, "cliente", termino)
    
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

