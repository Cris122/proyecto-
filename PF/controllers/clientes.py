from utils import pantalla

lista_clientes = []

def menu_clientes():
    acciones = {
        "1": ver_clientes,
        "2": agregar_cliente,
        "3": ver_historial_compras
    }
    while True:
        pantalla.limpiar_pantalla()
        pantalla.mostrar_titulo("👥 MENÚ DE CLIENTES")
        for linea in [
            "1. Ver clientes registrados",
            "2. Agregar nuevo cliente",
            "3. Ver historial de compras",
            "0. Volver al menú principal"
        ]:
            pantalla.imprimir_centrado(linea)
        pantalla.imprimir_centrado(pantalla.linea("-"))
        print()
        opcion = pantalla.input_centrado("Seleccione una opción: ")
        if opcion == "0": break
        accion = acciones.get(opcion)
        if accion: accion()
        else:
            pantalla.imprimir_centrado("❌ Opción no válida.")
            pantalla.pausar()

def buscar_cliente_por_correo(correo):
    return next((c for c in lista_clientes if c["correo"].lower() == correo.lower()), None)

def agregar_cliente():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("➕ AGREGAR CLIENTE")
    nombre = pantalla.input_centrado("Nombre del cliente: ")
    correo = pantalla.input_centrado("Correo electrónico: ")
    if buscar_cliente_por_correo(correo):
        pantalla.imprimir_centrado("❌ Ese correo ya está registrado.")
    else:
        lista_clientes.append({"nombre": nombre, "correo": correo.lower(), "compras": []})
        pantalla.imprimir_centrado(f"✅ Cliente '{nombre}' registrado correctamente.")
    pantalla.pausar()

def ver_clientes():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("📋 CLIENTES REGISTRADOS")
    if not lista_clientes:
        pantalla.imprimir_centrado("No hay clientes registrados.")
    else:
        for i, c in enumerate(lista_clientes, 1):
            pantalla.imprimir_centrado(f"{i}. {c['nombre']} - {c['correo']}")
    pantalla.pausar()

def ver_historial_compras():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("🧾 HISTORIAL DE COMPRAS")
    cliente = buscar_cliente_por_correo(pantalla.input_centrado("Correo del cliente: "))
    if not cliente:
        pantalla.imprimir_centrado("❌ Cliente no encontrado.")
    else:
        compras = cliente["compras"]
        pantalla.imprimir_centrado(f"👤 Nombre: {cliente['nombre']}")
        pantalla.imprimir_centrado(f"🛍️ Compras realizadas: {len(compras)}")
        pantalla.imprimir_centrado(f"💵 Total gastado: ${sum(compras):.2f}")
        pantalla.imprimir_centrado("📦 Listado de compras:")
        if not compras:
            pantalla.imprimir_centrado("Sin compras registradas.")
        else:
            for i, monto in enumerate(compras, 1):
                pantalla.imprimir_centrado(f"{i}. ${monto:.2f}")
    pantalla.pausar()
