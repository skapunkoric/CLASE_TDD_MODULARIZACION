import os
import sqlite3

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "inventario.db")

def conectar():
    "conecta el nombre del base de datos llamada inventario.db de sqllite3"
    return sqlite3.connect(DB_NAME)

def limpiar_historial_viejo():
    """Vacía las tablas y resetea los contadores. Ignora el error si las tablas no existen."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:

        cursor.execute("DELETE FROM inventario")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='inventario'")
        conexion.commit()
        
    except sqlite3.OperationalError:
        pass 
        
    conexion.close()

def crear_base_datos():
    "crea las tablas como inventario de la bd"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario(
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        estado_stock TEXT NULL  
    )              
    """)                
    conexion.commit()
    conexion.close()

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*)FROM inventario")
    cantidad_registros = cursor.fetchone()[0]
    if cantidad_registros > 0:
        conexion.close()
        return 
    productos_a_cargar = [
        ("A", 5),
        ("B", 0),
        ("C", 12),
        ("D", 3),
        ("E", 0),
        ("F", 8)
    ]
    # Try/Except para evitar errores si ejecutas el script varias veces seguidas
    try:
        cursor.executemany("""
        INSERT INTO inventario(nombre_producto, cantidad)
        VALUES (?, ?)""", productos_a_cargar)
        conexion.commit()
    
    except sqlite3.IntegrityError:
        pass
    conexion.close()  
    
def mostrar_estado_stock_completo():
    "consulta a la bd los stocks muestra el reporte de todo"    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto,nombre_producto,cantidad, estado_stock FROM inventario")
    stock_productos = cursor.fetchall()
    conexion.close()
    return stock_productos
    
         
def mostrar_stock_con_numero_definido(numero):
    "consulta a la bd los stocks segun cantidad de usario muestra el reporte segun cantidad"  
    cantidad_num = int(numero)
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre_producto, cantidad, estado_stock FROM inventario WHERE cantidad = ?", (cantidad_num,))
    stock_dinamico = cursor.fetchall()    
    conexion.close()
    return stock_dinamico
    
def obtener_cantidades_stock():
    "solo trae el ID y la cantidad de todos los productos"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, cantidad FROM inventario")
    todos_los_stocks = cursor.fetchall()
    conexion.close()
    return todos_los_stocks
def mostrar_stock_con_numero_de_id(id_numero):
    "consulta a la bd los stocks segun el id de producto que escoja "
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre_producto, cantidad, estado_stock FROM inventario WHERE id_producto = ?", (int(id_numero),))
    stock_dinamico = cursor.fetchall()
    conexion.close()
    return stock_dinamico


def obtener_un_producto(id_numero):
    "consulta a la bd segun el id de producto especifico p None "
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre_producto, cantidad, estado_stock FROM inventario WHERE id_producto = ?", (id_numero,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_estado_producto(id_producto, nuevo_estado):
    "actualiza a la bd los stocks segun cantidad de usuario muestra el reporte segun cantidad"  
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" UPDATE inventario SET estado_stock = ? WHERE   id_producto = ?
    """, (nuevo_estado, id_producto))
    conexion.commit()
    conexion.close()

def hay_productos():
    """Verifica si existe al menos un producto registrado en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventario")
    cantidad = cursor.fetchone()[0]
    conexion.close()
    return cantidad > 0

def actualizar_producto(id_producto, nombre_nuevo, cantidad_nueva, estado_nuevo):
    """Permite modificar un producto existente mediante su ID, manteniendo datos si se deja vacío (UPDATE)."""  
    if not hay_productos():
        return False
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre_producto, cantidad, estado_stock FROM inventario WHERE id_producto=?",(id_producto,))
    producto_viejo = cursor.fetchone()
    if producto_viejo is None:
        conexion.close()
        return False

    nombre_viejo, cantidad_vieja , estado_viejo = producto_viejo

    nombre_final = nombre_nuevo if nombre_nuevo !="" else nombre_viejo
    cantidad_final = cantidad_nueva if cantidad_nueva !="" else cantidad_vieja
    estado_final = estado_nuevo if estado_nuevo !="" else estado_viejo

    cursor.execute(""" UPDATE inventario SET nombre_producto = ?, cantidad = ?, estado_stock = ? WHERE id_producto =? """,(nombre_final, cantidad_final, estado_final, id_producto))
    conexion.commit()
    conexion.close()
    return True
