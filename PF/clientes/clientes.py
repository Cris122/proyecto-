import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import *
from conexionBD import conexion, cursor

# Funciones de interacción con la base de datos para clientes
def buscar_cliente_por_correo_db(correo):
    try:
        cursor.execute("SELECT id, nombre, correo FROM clientes WHERE correo = %s", (correo.lower(),))
        cliente_data = cursor.fetchone()
        if cliente_data:
            # Recuperar compras del cliente (si las hubiera, de la tabla ventas)
            # Esto es un ejemplo, en un sistema real, las compras se sumarían de la tabla ventas
            # Para simplificar, aquí solo devolvemos los datos del cliente
            return {"id": cliente_data[0], "nombre": cliente_data[1], "correo": cliente_data[2], "compras": []}
        return None
    except Exception as e:
        mostrar_mensaje(f"Error al buscar cliente por correo: {e}", "error")
        return None

def obtener_todos_los_clientes_db():
    try:
        cursor.execute("SELECT id, nombre, correo FROM clientes")
        clientes_data = cursor.fetchall()
        lista_clientes = []
        for cliente_row in clientes_data:
            # Para cada cliente, obtener el total de compras de la tabla ventas
            cursor.execute("SELECT SUM(total) FROM ventas WHERE cliente_id = %s", (cliente_row[0],))
            total_compras = cursor.fetchone()[0] or 0.0
            lista_clientes.append({
                "id": cliente_row[0],
                "nombre": cliente_row[1],
                "correo": cliente_row[2],
                "total_compras": total_compras # Se usa para mostrar, no se guarda en el objeto cliente
            })
        return lista_clientes
    except Exception as e:
        mostrar_mensaje(f"Error al obtener clientes: {e}", "error")
        return []

def menu_clientes(): # Ya no necesita lista_clientes como parámetro
    opciones = [
        ("1", "📋 Ver clientes"),
        ("2", "➕ Agregar cliente"),
        ("3", "✏️ Editar cliente"),
        ("4", "🗑️ Eliminar cliente"),
        ("0", "🔙 Volver al menú principal")
    ]

    while True:
        opcion = mostrar_menu("MENÚ DE CLIENTES", opciones, "👥 GESTIÓN DE CLIENTES 👥")
        
        match opcion:
            case "1": ver_clientes()
            case "2": agregar_cliente()
            case "3": editar_cliente()
            case "4": eliminar_cliente()
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def ver_clientes(): # Ya no necesita lista_clientes como parámetro
    mostrar_titulo("📋 CLIENTES REGISTRADOS")
    
    lista_clientes_db = obtener_todos_los_clientes_db() # Obtener clientes de la DB
    
    if not lista_clientes_db:
        mostrar_mensaje("No hay clientes registrados.", "info")
        return

    # Preparar datos para mostrar en tabla
    datos_clientes = []
    for i, cliente in enumerate(lista_clientes_db, 1):
        datos_clientes.append({
            "num": i,
            "nombre": cliente['nombre'],
            "correo": cliente['correo'],
            "total_compras": f"${cliente['total_compras']:.2f}"
        })

    headers = [
        ("num", "#", 3),
        ("nombre", "Nombre", 25),
        ("correo", "Correo", 30),
        ("total_compras", "Compras", 10)
    ]
    mostrar_tabla(datos_clientes, headers, f"Total: {len(lista_clientes_db)} clientes")
    mostrar_mensaje(f"Total: {len(lista_clientes_db)} clientes", "info", pausar_despues=True)


def agregar_cliente(): # Ya no necesita lista_clientes como parámetro
    mostrar_titulo("➕ AGREGAR CLIENTE")
    
    nombre = input_seguro("Nombre del cliente")
    if not nombre:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
        
    correo = input_seguro("Correo electrónico", validador=validar_email)
    if not correo:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
    
    if buscar_cliente_por_correo_db(correo): # Usar la función de búsqueda en DB
        mostrar_mensaje("Ya existe un cliente con ese correo.", "error")
        return
    
    try:
        sql = "INSERT INTO clientes (nombre, correo) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, correo.lower()))
        conexion.commit()
        mostrar_mensaje(f"Cliente '{nombre}' registrado correctamente.", "success")
    except Exception as e:
        conexion.rollback()
        mostrar_mensaje(f"Error al agregar cliente: {e}", "error")
    finally:
        pausar()

def editar_cliente(): # Ya no necesita lista_clientes como parámetro
    mostrar_titulo("✏️ EDITAR CLIENTE")
    
    # Usar la función plantilla para obtener el cliente de la DB
    cliente = obtener_elemento_por_input(
        "cliente",
        lambda: input_seguro("Correo del cliente a editar", validador=validar_email),
        buscar_cliente_por_correo_db, # Función de búsqueda en DB
        "Cliente no encontrado."
    )
    if not cliente:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
    
    nuevo_nombre = input_seguro(f"Nuevo nombre (actual: {cliente['nombre']})")
    if nuevo_nombre:
        cliente["nombre"] = nuevo_nombre
    
    nuevo_correo = input_seguro(f"Nuevo correo (actual: {cliente['correo']})", validador=validar_email)
    if nuevo_correo and nuevo_correo.lower() != cliente["correo"]:
        if buscar_cliente_por_correo_db(nuevo_correo): # Usar la función de búsqueda en DB
            mostrar_mensaje("Ya existe un cliente con ese correo.", "error")
            return
        cliente["correo"] = nuevo_correo.lower()
    
    try:
        sql = "UPDATE clientes SET nombre = %s, correo = %s WHERE id = %s"
        cursor.execute(sql, (cliente["nombre"], cliente["correo"], cliente["id"]))
        conexion.commit()
        mostrar_mensaje("Cliente actualizado correctamente.", "success")
    except Exception as e:
        conexion.rollback()
        mostrar_mensaje(f"Error al actualizar cliente: {e}", "error")
    finally:
        pausar()

def eliminar_cliente(): # Ya no necesita lista_clientes como parámetro
    mostrar_titulo("🗑️ ELIMINAR CLIENTE")
    
    # Usar la función plantilla para obtener el cliente de la DB
    cliente = obtener_elemento_por_input(
        "cliente",
        lambda: input_seguro("Correo del cliente a eliminar", validador=validar_email),
        buscar_cliente_por_correo_db, # Función de búsqueda en DB
        "Cliente no encontrado."
    )
    if not cliente:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
    
    if confirmar_accion(f"¿Eliminar cliente '{cliente['nombre']}'? (s/n): "):
        try:
            # Primero, verificar si el cliente tiene ventas asociadas
            cursor.execute("SELECT COUNT(*) FROM ventas WHERE cliente_id = %s", (cliente['id'],))
            if cursor.fetchone()[0] > 0:
                mostrar_mensaje("No se puede eliminar el cliente porque tiene ventas registradas.", "error")
                pausar()
                return

            sql = "DELETE FROM clientes WHERE id = %s"
            cursor.execute(sql, (cliente["id"],))
            conexion.commit()
            mostrar_mensaje(f"Cliente '{cliente['nombre']}' eliminado.", "success")
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al eliminar cliente: {e}", "error")
        finally:
            pausar()
    else:
        mostrar_mensaje("Operación cancelada.", "warn")
        pausar()
