import getpass
from funciones import *

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = {
            "admin": {
                "nombre": "Administrador",
                "password_hash": hashear_password("admin123"),
                "rol": "admin"
            }
        }

    def _validar_usuario_unico(self, username):
        """Valida que el usuario no exista"""
        if username in self.usuarios:
            mostrar_mensaje("Este usuario ya existe", "error")
            pausar("Presiona Enter para reintentar...")
            return False
        return True

    def _validar_usuario_existente(self, username):
        """Valida que el usuario exista"""
        if username not in self.usuarios:
            mostrar_mensaje("Usuario no encontrado", "error")
            pausar("Presiona Enter para reintentar...")
            return False
        return True

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
        """Maneja los intentos de login con contraseña"""
        for intento in range(max_intentos, 0, -1):
            try:
                password = getpass.getpass("Contraseña: ")
                if self.usuarios[username]["password_hash"] == hashear_password(password):
                    return self.usuarios[username]
                
                if intento > 1:
                    mostrar_mensaje(f"Contraseña incorrecta. Intentos restantes: {intento-1}", "error")
                    pausar("Presiona Enter para reintentar...")
            except Exception:
                continue
        
        mostrar_mensaje("Cuenta bloqueada temporalmente", "warn")
        pausar()
        return None

    def registrar_usuario(self):
        """Registro de usuario optimizado"""
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

        # Crear usuario
        self.usuarios[username] = {
            "nombre": datos["nombre"],
            "password_hash": hashear_password(password),
            "rol": datos["rol"]
        }
        
        mostrar_mensaje("Usuario registrado exitosamente!", "success")
        pausar()
        return True

    def autenticar_usuario(self):
        """Autenticación de usuario optimizada"""
        username = input_seguro(
            "Usuario",
            validador=self._validar_usuario_existente,
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