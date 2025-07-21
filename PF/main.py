from auth.usuarios import SistemaUsuarios
from funciones import *
import inventario.inventario as inventario
import clientes.clientes as clientes
import ventas.ventas as ventas

def menu_principal(usuario_logueado, productos, lista_clientes, ventas_realizadas):
    while True:
        opcion = mostrar_menu(
            f"💎 SISTEMA DE GESTIÓN - JOYERÍA ORO & PLATA 💎\n"
            f"Usuario: {usuario_logueado['nombre']} ({usuario_logueado['rol']})",
            [
                ("1", "📦 Gestión de Inventario"),
                ("2", "💰 Gestión de Ventas"),
                ("3", "👥 Gestión de Clientes"),
                ("0", "🚪 Cerrar sesión")
            ]
        )

        match opcion:
            case "1":
                inventario.menu_inventario(productos)
            case "2":
                ventas.menu_ventas(productos, lista_clientes, ventas_realizadas)
            case "3":
                clientes.menu_clientes(lista_clientes)
            case "0":
                mostrar_mensaje(f"¡Hasta luego, {usuario_logueado['nombre']}!")
                return
            case _:
                mostrar_mensaje("❌ Opción inválida", "error")
                pausar()

def main():
    auth_system = SistemaUsuarios()
    productos = []
    lista_clientes = []
    ventas_realizadas = []

    while True:
        usuario_logueado = auth_system.sistema_autenticacion()
        if not usuario_logueado:
            break

        mostrar_mensaje(
            f"¡Bienvenido/a {usuario_logueado['nombre']}! "
            f"Rol: {usuario_logueado['rol'].capitalize()}",
            "success"
        )
        pausar()
        
        menu_principal(usuario_logueado, productos, lista_clientes, ventas_realizadas)

if __name__ == "__main__":
    main()
