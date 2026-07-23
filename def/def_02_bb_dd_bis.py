# ------------------------------------------------------------
# Ejercicio complejo 2: Registro de gastos
# ------------------------------------------------------------
"""
Consigna:
Crear un programa que registre gastos hasta que el usuario escriba 0.

Requisitos:
- Pedir importes de gastos uno por uno.
- Si el usuario ingresa 0, terminar la carga.
- Si ingresa un número negativo, mostrar un error y volver a pedir el dato.
- Acumular el total de gastos válidos.
- Contar cuántos gastos válidos se ingresaron.
- Al final, mostrar:
  - Total gastado.
  - Cantidad de gastos cargados.
  - Promedio de gasto, solo si se cargó al menos un gasto.
"""
import re
import os
import sqlite3
from tabulate import tabulate

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "gastos.db")
mensaje_gasto = "💵 Ingresá el importe del gasto (0 para terminar):"
mensaje_error =  "⚠️ Error: El importe no puede ser un número negativo. Volvé a intentar."


def conectar():
    return sqlite3.connect(DB_NAME)

def crear_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gasto(
    id_gasto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    monto INTEGER NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)               
    """)                
print("¡Base de datos  creada con éxito!")

def ingreso_gasto(monto_ingresado):
        
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO gasto(monto)
        VALUES(?)""",(monto_ingresado,))
        conexion.commit()
        conexion.close()

def reporte_encabezado(mensaje):        
    
    print("\n" + "=" * 24)
    print(mensaje)
    print("=" * 24)

def reporte_dashboard():
     
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(" SELECT SUM(monto) FROM gasto")
    total = cursor.fetchone()[0] or 0
      
    cursor.execute("SELECT COUNT(*) FROM gasto ")
    gasto_valido = cursor.fetchone()[0] or 0

    cursor.execute(" SELECT AVG(monto) FROM gasto")
    promedio = round(cursor.fetchone()[0] or 0,2)
    
    reporte_encabezado("📊 DASHBOARD GLOBAL DE GASTOS")
    resumen = [
     [f"💰 Total gastado:$",total],
     [f"⚖️ Promedio por gasto: $", promedio],
     [f"📋 Cantidad de gastos cargados:", gasto_valido]
    ]
    print(tabulate(resumen,headers=["Metica", "Valor"], tablefmt='grid'))

def limpiar_historial_viejo():
    """Vacía las tablas y resetea los contadores de autoincremento"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. Borramos los datos reales
    cursor.execute("DELETE FROM gasto")
    # 2. ⚡ LA MAGIA: Reseteamos los contadores internos del sistema
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='gasto'")
    conexion.commit()
    conexion.close()
    print("🧹 ¡Historial viejo eliminado y contadores reseteados a 1!")

def pedir_gasto(mensaje):
    
    while True:
        texto = input(mensaje).strip()
        if re.match(r"^-?\d+$", texto):
            gasto_ingresado = int(texto)
            if gasto_ingresado < 0:
                print(mensaje_error)
            else: 
                return gasto_ingresado
        
        else:
            print(mensaje_error)
       
def simulador_gasto():
    
    crear_base_datos()
    limpiar_historial_viejo()
    while True:
        monto_ingresado = pedir_gasto(mensaje_gasto)
        if monto_ingresado == 0:
            break
        ingreso_gasto(monto_ingresado)
    return reporte_dashboard()
        


simulador_gasto()
    
    
    



















