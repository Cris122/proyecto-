import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funciones import (
    mostrar_menu, mostrar_mensaje, mostrar_titulo, 
    input_seguro, validar_email, confirmar_accion, buscar_en_lista,
    obtener_elemento_por_input, mostrar_tabla
)

# lista_clientes se pasa ahora desde main.py
# def buscar_cliente_por_correo(correo):
#     return buscar_en_lista(lista_clientes, "correo", correo.lower())

def menu_clientes(lista_clientes):
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
            case "1": ver_clientes(lista_clientes)
            case "2": agregar_cliente(lista_clientes)
            case "3": editar_cliente(lista_clientes)
            case "4": eliminar_cliente(lista_clientes)
            case "0": break
            case _: mostrar_mensaje("Opción no válida.", "error")

def ver_clientes(lista_clientes):
    mostrar_titulo("📋 CLIENTES REGISTRADOS")
    
    if not lista_clientes:
        mostrar_mensaje("No hay clientes registrados.", "info")
        return

    # Preparar datos para mostrar en tabla
    datos_clientes = []
    for i, cliente in enumerate(lista_clientes, 1):
        total_compras = sum(cliente.get("compras", []))
        datos_clientes.append({
            "num": i,
            "nombre": cliente['nombre'],
            "correo": cliente['correo'],
            "total_compras": f"${total_compras:.2f}"
        })

    headers = [
        ("num", "#", 3),
        ("nombre", "Nombre", 25),
        ("correo", "Correo", 30),
        ("total_compras", "Compras", 10)
    ]
    mostrar_tabla(datos_clientes, headers, f"Total: {len(lista_clientes)} clientes")
    mostrar_mensaje(f"Total: {len(lista_clientes)} clientes", "info", pausar_despues=True)


def agregar_cliente(lista_clientes):
    mostrar_titulo("➕ AGREGAR CLIENTE")
    
    nombre = input_seguro("Nombre del cliente")
    if not nombre:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
        
    correo = input_seguro("Correo electrónico", validador=validar_email)
    if not correo:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
    
    if buscar_en_lista(lista_clientes, "correo", correo.lower()):
        mostrar_mensaje("Ya existe un cliente con ese correo.", "error")
        return
    
    lista_clientes.append({"nombre": nombre, "correo": correo.lower(), "compras": []})
    mostrar_mensaje(f"Cliente '{nombre}' registrado correctamente.", "success")

def editar_cliente(lista_clientes):
    mostrar_titulo("✏️ EDITAR CLIENTE")
    
    # Usar la función plantilla para obtener el cliente
    cliente = obtener_elemento_por_input(
        lista_clientes,
        "cliente",
        lambda: input_seguro("Correo del cliente a editar", validador=validar_email),
        lambda c: buscar_en_lista(lista_clientes, "correo", c.lower()),
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
        if buscar_en_lista(lista_clientes, "correo", nuevo_correo.lower()):
            mostrar_mensaje("Ya existe un cliente con ese correo.", "error")
            return
        cliente["correo"] = nuevo_correo.lower()
    
    mostrar_mensaje("Cliente actualizado correctamente.", "success")

def eliminar_cliente(lista_clientes):
    mostrar_titulo("🗑️ ELIMINAR CLIENTE")
    
    # Usar la función plantilla para obtener el cliente
    cliente = obtener_elemento_por_input(
        lista_clientes,
        "cliente",
        lambda: input_seguro("Correo del cliente a eliminar", validador=validar_email),
        lambda c: buscar_en_lista(lista_clientes, "correo", c.lower()),
        "Cliente no encontrado."
    )
    if not cliente:
        mostrar_mensaje("Operación cancelada.", "warn")
        return
    
    if confirmar_accion(f"¿Eliminar cliente '{cliente['nombre']}'? (s/n): "):
        lista_clientes.remove(cliente)
        mostrar_mensaje(f"Cliente '{cliente['nombre']}' eliminado.", "success")
    else:
        mostrar_mensaje("Operación cancelada.", "warn")

