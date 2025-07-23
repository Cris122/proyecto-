import getpass
from funciones import *
from conexionBD import conexion, cursor
import sys

class SistemaUsuarios:
    def __init__(self):
        # La inicialización ya no carga usuarios en memoria, solo asegura la conexión
        pass

    def _validar_usuario_unico(self, username):
        """Valida que el usuario no exista en la base de datos"""
        try:
            cursor.execute("SELECT username FROM usuarios WHERE username = %s", (username,))
            if cursor.fetchone():
                mostrar_mensaje("Este usuario ya existe", "error")
                pausar("Presiona Enter para reintentar...")
                return False
            return True
        except Exception as e:
            mostrar_mensaje(f"Error al validar usuario: {e}", "error")
            pausar()
            return False

    def _validar_usuario_existente(self, username):
        """Valida que el usuario exista en la base de datos"""
        try:
            cursor.execute("SELECT username FROM usuarios WHERE username = %s", (username,))
            if not cursor.fetchone():
                mostrar_mensaje("Usuario no encontrado", "error")
                pausar("Presiona Enter para reintentar...")
                return False
            return True
        except Exception as e:
            mostrar_mensaje(f"Error al validar usuario: {e}", "error")
            pausar()
            return False

    def _solicitar_password_segura(self):
        """Solicita contraseña con confirmación"""
        while True:
            try:
                password = getpass.getpass("Contraseña (no visible): ")
                if len(password) < 6:
                    raise ValueError("La contraseña debe tener al menos 6 caracteres")
                
                confirm_pass = getpass.getpass("Confirmar contraseña: ")
                if password != confirm_pass:
                    raise ValueError("Las contraseñas no coinciden")
                return password
            except ValueError as e:
                mostrar_mensaje(str(e), "error")
                pausar("Presiona Enter para reintentar...")

    def _intentos_login(self, username, max_intentos=3):
        """Maneja los intentos de login con contraseña contra la base de datos"""
        try:
            cursor.execute("SELECT username, nombre, password_hash, rol FROM usuarios WHERE username = %s", (username,))
            usuario_db = cursor.fetchone()
            if not usuario_db:
                mostrar_mensaje("Usuario no encontrado", "error")
                pausar()
                return None
            
            # Convertir la tupla a un diccionario para facilitar el acceso
            usuario_info = {
                "username": usuario_db[0],
                "nombre": usuario_db[1],
                "password_hash": usuario_db[2],
                "rol": usuario_db[3]
            }

            for intento in range(max_intentos, 0, -1):
                password = getpass.getpass("Contraseña: ")
                if verificar_password(password, usuario_info["password_hash"]):
                    return usuario_info
                
                if intento > 1:
                    mostrar_mensaje(f"Contraseña incorrecta. Intentos restantes: {intento-1}", "error")
                    pausar("Presiona Enter para reintentar...")
            
            mostrar_mensaje("Cuenta bloqueada temporalmente", "warn")
            pausar()
            return None
        except Exception as e:
            mostrar_mensaje(f"Error durante el intento de login: {e}", "error")
            pausar()
            return None

    def registrar_usuario(self):
        """Registro de usuario optimizado en la base de datos"""
        datos = {}
        
        # Solicitar username único
        username = input_seguro(
            "Nombre de usuario (min. 4 caracteres)",
            validador=lambda u: len(u) >= 4 and self._validar_usuario_unico(u),
            titulo_contexto="📝 REGISTRO DE USUARIO",
            datos_progreso=datos
        )
        if not username:
            return None
        datos["usuario"] = username

        # Solicitar contraseña
        password = self._solicitar_password_segura()
        if not password:
            return None
        password_hash = hashear_password(password)

        # Solicitar datos restantes
        campos_adicionales = [
            ("Nombre completo", "nombre", "texto", None, None, None),
            ("Rol (admin/vendedor)", "rol", "texto", lambda r: r.lower() in ["admin", "vendedor"], None, None)
        ]
        
        for label, clave, tipo, validador, _, _ in campos_adicionales:
            valor = input_seguro(
                label, validador, True,
                titulo_contexto="📝 REGISTRO DE USUARIO",
                datos_progreso=datos
            )
            if not valor:
                return None
            datos[clave] = valor.lower() if clave == "rol" else valor

        # Insertar usuario en la base de datos
        try:
            sql = "INSERT INTO usuarios (username, nombre, password_hash, rol) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, datos["nombre"], password_hash, datos["rol"]))
            conexion.commit()
            mostrar_mensaje("Usuario registrado exitosamente!", "success")
            pausar()
            return True
        except Exception as e:
            conexion.rollback()
            mostrar_mensaje(f"Error al registrar usuario: {e}", "error")
            pausar()
            return False

    def autenticar_usuario(self):
        """Autenticación de usuario optimizada"""
        username = input_seguro(
            "Usuario",
            validador=self._validar_usuario_existente, # Esta validación ya consulta la DB
            titulo_contexto="🔐 INICIO DE SESIÓN"
        )
        
        return self._intentos_login(username) if username else None

    def sistema_autenticacion(self):
        """Sistema principal de autenticación"""
        opciones_menu = [
            ("1", "Iniciar sesión"),
            ("2", "Registrarse"), 
            ("0", "Salir")
        ]
        
        acciones = {
            "1": self.autenticar_usuario,
            "2": self.registrar_usuario,
            "0": lambda: None
        }

        while True:
            opcion = mostrar_menu(
                "💎 SISTEMA DE GESTIÓN - JOYERÍA ORO & PLATA 💎",
                opciones_menu,
                "SISTEMA DE AUTENTICACIÓN"
            )

            if opcion in acciones:
                resultado = acciones[opcion]()
                if opcion == "1" and resultado:  # Login exitoso
                    return resultado
                elif opcion == "0":  # Salir
                    return None
            else:
                mostrar_mensaje("Opción inválida", "error")
                pausar()
