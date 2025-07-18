from utils import pantalla
import re

lista_clientes = []

def menu_clientes():
    acciones = {
        "1": ver_clientes,
        "2": agregar_cliente,
        "3": ver_historial_compras
    }
    while True:
        try:
            pantalla.limpiar_pantalla()
            pantalla.mostrar_titulo("👥 MENÚ DE CLIENTES")
            opciones = [
                "1. Ver clientes registrados",
                "2. Agregar nuevo cliente",
                "3. Ver historial de compras",
                "0. Volver al menú principal",
                pantalla.linea("-")
            ]
            list(map(pantalla.imprimir_centrado, opciones))
            print()

            opcion = pantalla.input_centrado("Seleccione una opción: ")
            if opcion == "0":
                break

            accion = acciones.get(opcion)
            if accion:
                accion()
            else:
                pantalla.imprimir_centrado("❌ Opción no válida.")
                pantalla.pausar()

        except KeyboardInterrupt:
            pantalla.imprimir_centrado("\n⚠️ Operación cancelada por el usuario.")
            pantalla.pausar()
        except Exception as e:
            pantalla.imprimir_centrado(f"❌ Error inesperado: {e}")
            pantalla.pausar()

def buscar_cliente_por_correo(correo):
    try:
        return next((c for c in lista_clientes if c["correo"].lower() == correo.lower()), None)
    except Exception as e:
        pantalla.imprimir_centrado(f"❌ Error al buscar cliente: {e}")
        return None

def agregar_cliente():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("➕ AGREGAR CLIENTE")
    
    try:
        nombre = pantalla.input_centrado("Nombre del cliente: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not (2 <= len(nombre) <= 50):
            raise ValueError("El nombre debe tener entre 2 y 50 caracteres")

        correo = pantalla.input_centrado("Correo electrónico: ").strip().lower()
        if not correo:
            raise ValueError("El correo no puede estar vacío")
        if "@" not in correo or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', correo):
            raise ValueError("Formato de correo inválido")

        if buscar_cliente_por_correo(correo):
            raise ValueError("Ese correo ya está registrado")

        lista_clientes.append({
            "nombre": nombre,
            "correo": correo,
            "compras": []
        })

        pantalla.imprimir_centrado(f"✅ Cliente '{nombre}' registrado correctamente.")

    except ValueError as e:
        pantalla.imprimir_centrado(f"❌ Error: {e}")
    except KeyboardInterrupt:
        pantalla.imprimir_centrado("\n⚠️ Operación cancelada.")
    except Exception as e:
        pantalla.imprimir_centrado(f"❌ Error inesperado: {e}")

    pantalla.pausar()

def ver_clientes():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("📋 CLIENTES REGISTRADOS")
    
    try:
        if not lista_clientes:
            pantalla.imprimir_centrado("No hay clientes registrados.")
        else:
            if len(lista_clientes) > 1000:
                raise OverflowError("Demasiados clientes para mostrar")

            for i, c in enumerate(lista_clientes, 1):
                try:
                    pantalla.imprimir_centrado(f"{i}. {c['nombre']} - {c['correo']}")
                except KeyError:
                    pantalla.imprimir_centrado(f"{i}. Cliente con datos incompletos")
                except Exception:
                    pantalla.imprimir_centrado(f"{i}. Error al mostrar cliente")

    except OverflowError as e:
        pantalla.imprimir_centrado(f"❌ {e}")
    except MemoryError:
        pantalla.imprimir_centrado("❌ No hay suficiente memoria para mostrar todos los clientes")
    except Exception as e:
        pantalla.imprimir_centrado(f"❌ Error al mostrar clientes: {e}")

    pantalla.pausar()

def ver_historial_compras():
    pantalla.limpiar_pantalla()
    pantalla.mostrar_titulo("🧾 HISTORIAL DE COMPRAS")
    
    try:
        correo = pantalla.input_centrado("Correo del cliente: ").strip().lower()
        if not correo:
            raise ValueError("El correo no puede estar vacío")

        cliente = buscar_cliente_por_correo(correo)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        compras = cliente["compras"]
        pantalla.imprimir_centrado(f"👤 Nombre: {cliente['nombre']}")
        pantalla.imprimir_centrado(f"🛍️ Compras realizadas: {len(compras)}")

        try:
            total_gastado = sum(compras)
            pantalla.imprimir_centrado(f"💵 Total gastado: ${total_gastado:.2f}")
        except (TypeError, ValueError):
            pantalla.imprimir_centrado("💵 Error al calcular total gastado")

        pantalla.imprimir_centrado("📦 Listado de compras:")
        if not compras:
            pantalla.imprimir_centrado("Sin compras registradas.")
        else:
            for i, monto in enumerate(compras, 1):
                try:
                    pantalla.imprimir_centrado(f"{i}. ${monto:.2f}")
                except (TypeError, ValueError):
                    pantalla.imprimir_centrado(f"{i}. Monto inválido")

    except ValueError as e:
        pantalla.imprimir_centrado(f"❌ Error: {e}")
    except KeyboardInterrupt:
        pantalla.imprimir_centrado("\n⚠️ Operación cancelada.")
    except Exception as e:
        pantalla.imprimir_centrado(f"❌ Error inesperado: {e}")

    pantalla.pausar()