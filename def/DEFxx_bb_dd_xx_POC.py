import sqlite3
from tabulate import tabulate

DB_NAME = "inventario.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario(
        id_producto INTEGER PRIMARY KEY NOT NULL,
        nombre_producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()

def crear_productos_iniciales():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. IDs numéricos para cumplir con el INTEGER PRIMARY KEY
    datos_productos = [
        (1, "Producto A", 5),
        (2, "Producto B", 0),
        (3, "Producto C", 12),
        (4, "Producto D", 3),
        (5, "Producto E", 0),
        (6, "Producto F", 8)
    ]
    
    # El try/except acá evita que el programa explote si volvés a correr el script
    # y los IDs ya fueron creados previamente (Violación de Primary Key)
    try:
        # 2. Uso de executemany para cargar toda la lista en un solo viaje
        cursor.executemany("""
        INSERT INTO inventario(id_producto, nombre_producto, cantidad)
        VALUES (?, ?, ?)""", datos_productos)
        conexion.commit()
        print("✅ Productos de prueba cargados en la base de datos.")
    except sqlite3.IntegrityError:
        print("ℹ️ Los productos ya existen en la base de datos, omitiendo carga inicial.")
        
    conexion.close()  

def reporte_encabezado():
    print("\n" + "=" * 34)
    print("== REPORTE DE CONTROL DE STOCK ==")
    print("=" * 34)

def mostrar_sin_stock():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Traemos de la base de datos únicamente los que tengan stock cero
    cursor.execute("SELECT id_producto, nombre_producto, cantidad FROM inventario WHERE cantidad = ?", (0,))
    stock_productos = cursor.fetchall()
    
    reporte_encabezado()
    
    # 3. Headers con 3 elementos exactos coordinados con el SELECT
    headers = ["ID PRODUCTO", "NOMBRE", "CANTIDAD"]
    print(tabulate(stock_productos, headers=headers, tablefmt="grid"))
    
    conexion.close()

# ==========================================
# 🔥 LAS LLAMADAS DE CONTROL (Para probar)
# ==========================================
# Ejecutamos el flujo completo en orden:
crear_tabla()                 # Crea el archivo inventario.db y la estructura
crear_productos_iniciales()   # Guarda los 6 productos de prueba
mostrar_sin_stock()           # Consulta la base de datos y dibuja el "taburete"