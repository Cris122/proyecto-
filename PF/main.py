from utils import pantalla
from datetime import datetime
import inventario
import clientes
import ventas

while True:
    pantalla.limpiar_pantalla()
    pantalla.imprimir_centrado(pantalla.linea("="))
    pantalla.imprimir_centrado("💎 SISTEMA DE GESTIÓN - JOYERÍA ORO & PLATA 💎")
    pantalla.imprimir_centrado(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    pantalla.imprimir_centrado(pantalla.linea("="))
    print()
    pantalla.imprimir_centrado("📋 MENÚ PRINCIPAL")
    pantalla.imprimir_centrado(pantalla.linea("-"))
    pantalla.imprimir_centrado("1. 🧾 Inventario")
    pantalla.imprimir_centrado("2. 💰 Ventas")
    pantalla.imprimir_centrado("3. 👥 Clientes")
    pantalla.imprimir_centrado("0. ❌ Salir del sistema")
    pantalla.imprimir_centrado(pantalla.linea("-"))
    print()

    prompt = "Seleccione una opción: "
    espacio = " " * ((pantalla.ancho_consola() - len(prompt)) // 2)
    opcion = input(f"{espacio}{prompt}").strip()

    match opcion:
        case "1":
            inventario.menu_inventario()
        case "2":
            ventas.menu_ventas()
            pantalla.pausar()
        case "3":
            clientes.menu_clientes()
            pantalla.pausar()
        case "0":
            pantalla.imprimir_centrado("👋 Gracias por usar el sistema. ¡Hasta pronto!")
            pantalla.pausar()
            break
        case _:
            print("")
            pantalla.imprimir_centrado("❌ Opción no válida. Intente de nuevo.")
            pantalla.pausar()
