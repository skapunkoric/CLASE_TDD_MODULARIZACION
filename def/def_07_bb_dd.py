# ------------------------------------------------------------
# Ejercicio complejo 7: Control de stock
# ------------------------------------------------------------
"""
Consigna:
Dada la lista stock = [5, 0, 12, 3, 0, 8] y productos = ["A", "B", "C", "D", "E", "F"], generar un reporte.

Requisitos:
- Recorrer ambas listas usando el mismo índice.
- Mostrar cada producto con su cantidad disponible.
- Si el stock es 0, mostrar "Sin stock" y contar cuántos productos están agotados.
- Si el stock es menor o igual a 3 pero mayor que 0, mostrar "Stock bajo".
- Calcular el total de unidades disponibles.
- Mostrar al final:
  - Total de unidades.
  - Cantidad de productos sin stock.
"""
import sqlite3
import os
from tabulate import tabulate

# Configuración de ruta nivel Pro (para que VS Code no la esconda)
carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "inventario.db")

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
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

def crear_producto():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*)FROM inventario")
    cantidad_registros = cursor.fetchone()[0]
    if cantidad_registros > 0:
        ("ℹ️ La base de datos ya tiene información. Se cancela la carga inicial.")
        conexion.close()
        return # 👈
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
        print("✅ Productos iniciales cargados con éxito.")
    except sqlite3.IntegrityError:
        print("ℹ️ Los productos ya existen en la base de datos.")
        
    conexion.close()  

def reporte(mensaje, titulo_reporte="REPORTE DE CONTROL DE STOCK"):
    print("\n" + "=" * 40)
    print(f"== {titulo_reporte} ==")
    print("=" * 40)
    print(tabulate(mensaje, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))

def mostrar_estado_stock_completo():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre_producto, cantidad, estado_stock FROM inventario")
    stock_productos = cursor.fetchall()
    
    reporte(stock_productos, "STOCK COMPLETO")
    conexion.close()

def cantidad_usuario():
    cantidad_pedida = input("🔍 Ingrese la cantidad de stock a filtrar: ").strip()
    if cantidad_pedida.isdigit():
        return int(cantidad_pedida)
    else:
        print("⚠️ Error: Debe ingresar un número entero válido.")
        return None

def mostrar_stock_segun_input_usuario():
    cantidad_sol = cantidad_usuario()
    if cantidad_sol is None:
        return  # Cortamos la ejecución si el input fue basura
        
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre_producto, cantidad, estado_stock FROM inventario WHERE cantidad = ?", (cantidad_sol,))
    stock_filtrado = cursor.fetchall()
    
    reporte(stock_filtrado, f"FILTRADO POR CANTIDAD: {cantidad_sol}")
    conexion.close()

def mostrar_stock_con_numero_definido(numero):
    cantidad_num = int(numero)
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre_producto, cantidad, estado_stock FROM inventario WHERE cantidad = ?", (cantidad_num,))
    stock_dinamico = cursor.fetchall()
    
    reporte(stock_dinamico, f"FILTRADO FIJO (CANTIDAD: {numero})")
    conexion.close()

def actualizar_estado_producto():
    
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
    print("ESTADO CAMBIADO CON EXITO via python")
    mostrar_estado_stock_completo()

# =====================================================================
# 🔥 BLOQUE DE EJECUCIÓN PRINCIPAL
# =====================================================================
inicializar_base_de_datos = crear_tabla
inicializar_base_de_datos()
crear_producto()

# Mostramos los reportes de manera limpia, sin duplicar vistas
mostrar_stock_con_numero_definido(3)

# Descomentá la línea de abajo si querés probar el input interactivo por consola:
# mostrar_stock_segun_input_usuario()
# actualizar estado
actualizar_estado_producto()
mostrar_estado_stock_completo()
mostrar_stock_segun_input_usuario() # mostrar los SIN STOCK EN 0




  