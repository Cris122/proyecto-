from auth.usuarios import SistemaUsuarios # Ajustar la importación si es necesario
from funciones import *
import inventario.inventario as inventario
import clientes.clientes as clientes
import ventas.ventas as ventas
from conexionBD import conexion, cursor # Importar para asegurar que la conexión se establezca al inicio

def menu_principal(usuario_logueado): # Ya no necesita productos, lista_clientes, ventas_realizadas
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
                inventario.menu_inventario() # Llamada sin parámetros
            case "2":
                ventas.menu_ventas() # Llamada sin parámetros
            case "3":
                clientes.menu_clientes() # Llamada sin parámetros
            case "0":
                mostrar_mensaje(f"¡Hasta luego, {usuario_logueado['nombre']}!")
                return
            case _:
                mostrar_mensaje("❌ Opción inválida", "error")
                pausar()

def main():
    # Asegurarse de que la conexión a la base de datos se intente al inicio
    # La conexión se maneja en conexionBD.py, si falla, el programa podría salir o mostrar un error.
    if not conexion or not cursor:
        print("No se pudo establecer conexión con la base de datos. Saliendo...")
        sys.exit(1) # Salir si no hay conexión

    auth_system = SistemaUsuarios()
    # Las listas en memoria se eliminan
    # productos = []
    # lista_clientes = []
    # ventas_realizadas = []

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
        
        menu_principal(usuario_logueado) # Llamada sin las listas

    # Cerrar la conexión a la base de datos al finalizar la aplicación
    if conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    main()
