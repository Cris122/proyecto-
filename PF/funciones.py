import os
import shutil
import re
from datetime import datetime
import hashlib
import sys # Importar sys para sys.exit

# ------------------------ Consola ------------------------

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def ancho_consola():
    try:
        return shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        return 80

def centrar(texto):
    return str(texto).center(ancho_consola())

def imprimir_centrado(texto):
    print(centrar(str(texto)))

def linea(char="=", longitud=60):
    return (char * min(ancho_consola(), longitud)).center(ancho_consola())

def pausar(mensaje="Presiona Enter para continuar..."):
    print()
    input(mensaje.center(ancho_consola()))

# ------------------------ Fecha y Hora ------------------------

def mostrar_fecha_hora():
    ahora = datetime.now()
    fecha_str = ahora.strftime("%d/%m/%Y")
    hora_str = ahora.strftime("%H:%M:%S")
    imprimir_centrado(f"🗓️ Fecha: {fecha_str}   ⏰ Hora: {hora_str}")
    print()

# ------------------------ Títulos y visuales ------------------------

def mostrar_titulo(texto, emoji=""):
    limpiar_pantalla()
    imprimir_centrado(linea("="))
    imprimir_centrado(f"{emoji} {texto.upper()} {emoji}")
    imprimir_centrado(linea("="))
    print()

def mostrar_menu(titulo, opciones, subtitulo=""):
    limpiar_pantalla()
    imprimir_centrado(linea("="))
    imprimir_centrado(titulo)
    imprimir_centrado(linea("="))

    mostrar_fecha_hora()

    if subtitulo:
        imprimir_centrado(subtitulo)
        imprimir_centrado(linea("-"))

    for clave, texto in opciones:
        imprimir_centrado(f"{clave}. {texto}")

    imprimir_centrado(linea("-"))
    print()

    opcion = input_centrado("Seleccione una opción: ")
    return opcion

def mostrar_tabla(datos, headers, titulo=""):
    if titulo:
        imprimir_centrado(f"📋 {titulo}")
        imprimir_centrado(linea("-"))
    
    header_line = " | ".join(f"{h[1]:<{h[2]}}" for h in headers)
    imprimir_centrado(header_line)
    imprimir_centrado(linea("-"))
    
    for fila in datos:
        linea_dato = " | ".join(f"{str(fila.get(h[0], '')):<{h[2]}}" for h in headers)
        imprimir_centrado(linea_dato)
    
    imprimir_centrado(linea("-"))
    print()

def mostrar_progreso(diccionario):
    if diccionario:
        imprimir_centrado("📝 Datos ingresados:")
        for campo, valor in diccionario.items():
            nombre = campo.replace("_", " ").capitalize()
            imprimir_centrado(f"   {nombre}: {valor}")
        print()

def mostrar_mensaje(texto, tipo="info", pausar_despues=False):
    prefijos = {"info": "", "error": "❌ ", "success": "✅ ", "warn": "⚠️ "}
    prefijo = prefijos.get(tipo, '')
    
    if prefijo and not texto.startswith(prefijo):
        texto = f"{prefijo}{texto}"
    
    imprimir_centrado(texto)
    if pausar_despues:
        pausar()

# ------------------------ Inputs optimizados ------------------------

def input_centrado(texto):
    espacio = " " * ((ancho_consola() - len(texto)) // 2)
    return input(f"{espacio}{texto}").strip()

def _validar_entrada(entrada, validador, tipo_error):
    """Función auxiliar para validar entradas"""
    if not entrada:
        return "Campo requerido"
    if validador and not validador(entrada):
        return tipo_error
    return None

def input_con_validacion(label, validador=None, convertidor=None, tipo_error="Formato inválido", 
                        min_val=None, max_val=None, cancelable=True, titulo_contexto="", 
                        datos_progreso=None):
    """Función unificada para todos los tipos de input con validación"""
    
    def mostrar_contexto():
        if titulo_contexto:
            mostrar_titulo(titulo_contexto)
            if datos_progreso:
                mostrar_progreso(datos_progreso)
        if cancelable:
            imprimir_centrado("(Escriba '0' para cancelar)")
    
    while True:
        mostrar_contexto()
        entrada = input_centrado(f"{label}:")
        
        if cancelable and entrada == '0':
            return None
        
        # Validación básica
        error = _validar_entrada(entrada, validador, tipo_error)
        if error:
            mostrar_mensaje(error, "error")
            pausar("Presiona Enter para reintentar...")
            continue
        
        # Conversión si es necesaria
        if convertidor:
            try:
                valor = convertidor(entrada)
            except ValueError:
                mostrar_mensaje(tipo_error, "error")
                pausar("Presiona Enter para reintentar...")
                continue
        else:
            valor = entrada
        
        # Validación de rango para números
        if min_val is not None and valor < min_val:
            mostrar_mensaje(f"Debe ser mayor o igual a {min_val}", "error")
            pausar("Presiona Enter para reintentar...")
            continue
        if max_val is not None and valor > max_val:
            mostrar_mensaje(f"Debe ser menor o igual a {max_val}", "error")
            pausar("Presiona Enter para reintentar...")
            continue
        
        return valor

def input_seguro(label, validador=None, cancelable=True, titulo_contexto="", datos_progreso=None):
    """Input para texto con validación"""
    return input_con_validacion(label, validador, None, "Formato inválido", 
                               cancelable=cancelable, titulo_contexto=titulo_contexto,
                               datos_progreso=datos_progreso)

def input_entero(label, min_val=None, max_val=None, cancelable=True, titulo_contexto="", datos_progreso=None):
    """Input para números enteros"""
    def es_entero(x):
        return x.isdigit()
    
    return input_con_validacion(label, es_entero, int, "Debe ser un número entero válido",
                               min_val, max_val, cancelable, titulo_contexto, datos_progreso)

def input_flotante(label, min_val=None, max_val=None, cancelable=True, titulo_contexto="", datos_progreso=None):
    """Input para números flotantes"""
    return input_con_validacion(label, None, float, "Debe ser un número válido",
                               min_val, max_val, cancelable, titulo_contexto, datos_progreso)

# ------------------------ Validaciones ------------------------

def validar_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()) is not None

def confirmar_accion(mensaje="¿Desea continuar? (s/n): "):
    while True:
        respuesta = input_centrado(mensaje).lower()
        if respuesta in ('s', 'n'):
            return respuesta == 's'
        mostrar_mensaje("Respuesta inválida, ingrese 's' o 'n'", "error")
        pausar("Presiona Enter para reintentar...")

def confirmar_accion_destructiva(mensaje_advertencia, palabra_clave_confirmacion):
    mostrar_mensaje(mensaje_advertencia, "warn")
    imprimir_centrado(f"Para confirmar, escriba '{palabra_clave_confirmacion}':")
    respuesta = input_centrado("Confirmación: ")
    return respuesta == palabra_clave_confirmacion

# ------------------------ Búsquedas (Adaptadas para DB) ------------------------
# Estas funciones ahora son más genéricas y se usarán con funciones de búsqueda de DB
# en los módulos específicos (usuarios, clientes, inventario, ventas)

def obtener_elemento_por_input(tipo_elemento, input_label_func, buscar_func, mensaje_no_encontrado):
    """Función plantilla para obtener un elemento mediante input del usuario y una función de búsqueda de DB"""
    while True:
        identificador = input_label_func()
        if identificador is None:
            return None
        
        elemento = buscar_func(identificador)
        if not elemento:
            mostrar_mensaje(mensaje_no_encontrado, "error", pausar_despues=False)
            continue
        return elemento

# ------------------------ Hashing ------------------------

def hashear_password(password):
    """Hashea una contraseña usando SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_password(password_ingresada, password_hasheada):
    """Verifica si una contraseña ingresada coincide con una hasheada."""
    return hashear_password(password_ingresada) == password_hasheada

# ------------------------ Solicitud de Datos Genérica ------------------------

def solicitar_datos_generico(titulo_principal, campos, datos_existentes=None):
    """Solicita datos al usuario de forma interactiva para múltiples campos"""
    datos = datos_existentes.copy() if datos_existentes else {}
    
    for label, clave, tipo, validador, min_val, max_val in campos:
        predeterminado = datos.get(clave)
        label_con_default = f"{label} (actual: {predeterminado})" if predeterminado is not None else label

        # Seleccionar función de input según el tipo
        input_func = {
            "texto": lambda: input_seguro(label_con_default, validador, True, titulo_principal, datos),
            "entero": lambda: input_entero(label_con_default, min_val, max_val, True, titulo_principal, datos),
            "flotante": lambda: input_flotante(label_con_default, min_val, max_val, True, titulo_principal, datos)
        }.get(tipo)
        
        if not input_func:
            continue
            
        valor = input_func()
        if valor is None:  # Usuario canceló
            return None
        
        datos[clave] = valor

    return datos
