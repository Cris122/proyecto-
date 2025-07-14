import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def ancho_consola():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Valor por defecto si no se puede obtener el tamaño

def centrar(texto):
    ancho = ancho_consola()
    return texto.center(ancho)

def imprimir_centrado(texto):
    print(centrar(texto))

def linea(char="=", longitud=56):
    return (char * longitud).center(ancho_consola())

def pausar(mensaje="Presiona una tecla para continuar..."):
    print()
    input(mensaje.center(ancho_consola()))

def mostrar_titulo(texto):
    limpiar_pantalla()
    imprimir_centrado(linea("="))
    imprimir_centrado(texto)
    imprimir_centrado(linea("="))
    print()

def input_centrado(texto):
    espacio = " " * ((ancho_consola() - len(texto)) // 2)
    return input(f"{espacio}{texto}")
