import os
import sqlite3

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "gastos.db")

def conectar():
    "conecta el nombre del base de datos llamada inventario.db de sqllite3"
    return sqlite3.connect(DB_NAME)

def limpiar_historial_viejo():
    """Vacía las tablas y resetea los contadores de autoincremento"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM inventario")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='inventario'")
    conexion.commit()
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
    
    
def actualizar_estado_producto():
    "actualiza a la bd los stocks segun cantidad de usuario muestra el reporte segun cantidad"  
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, cantidad FROM inventario")
    todos_los_stocks = cursor.fetchall()
    for id_prod,cantidad_actual in todos_los_stocks:
        if cantidad_actual == 0:
             nuevo_estado = "❌ [SIN STOCK]"
        
        elif cantidad_actual <= 3:
            nuevo_estado = "⚠️ [STOCK BAJO]"
         
        else:      
            nuevo_estado = "✅ [STOCK OK]"
        cursor.execute("""
        UPDATE inventario 
        SET estado_stock = ? 
        WHERE   id_producto = ?
    """, (nuevo_estado, id_prod))
    conexion.commit()
    conexion.close()
    
    

      