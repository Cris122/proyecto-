import mysql.connector
try:
    conexion=mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_proyecto"
    )
    cursor=conexion.cursor(buffered=True)
except mysql.connector.Error as err: # Captura el error específico de MySQL
    print(f"Error al conectar con la base de datos: {err}")
    print(f"Asegúrate de que MySQL esté corriendo en XAMPP y la base de datos 'bd_proyecto' exista.")
    # Puedes agregar sys.exit(1) aquí si la conexión es crítica para la aplicación



