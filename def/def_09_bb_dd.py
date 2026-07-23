"""
**Ejercicio 9** | Simulador de Ahorro | 🟨 *Siguiente candidato* | Eliminar `while True`, Historial de Transacciones. |
"""
### 🟨 2. Simulador de Ahorro / Cajero Automático (Ejercicio 9) - **PRÓXIMO PASO**
#* **Objetivo de Refactorización:** Eliminar por completo el bucle infinito `while True` utilizando banderas de control (`flags`) o menús modulares más limpios.
#* **Desafío Base de Datos:** * Crear una tabla `historial_ahorro` o `transacciones`.
#* Cada depósito o extracción no solo debe cambiar el saldo total, sino registrar una fila histórica con la fecha, el tipo de movimiento y el monto.

# ------------------------------------------------------------
# Ejercicio complejo 9: Simulador de ahorro
# ------------------------------------------------------------
"""
Consigna:
Crear un programa que simule un objetivo de ahorro.

Requisitos:
- Pedir al usuario un objetivo de ahorro, por ejemplo 50000.
- Luego pedir depósitos uno por uno.
- No aceptar depósitos negativos ni vacíos.
- Acumular los depósitos válidos.
- Mostrar después de cada depósito cuánto falta para llegar al objetivo.
- Cuando el ahorro acumulado llegue o supere el objetivo, mostrar "Objetivo alcanzado".
- Mostrar cuántos depósitos válidos se realizaron.
"""
import re
import os
import sqlite3
from tabulate import tabulate

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "ahorro.db")
mensaje_ahorro_error_numerico = "⚠️ Error: Por favor, ingresá un monto numérico entero y mayor a cero."
mensaje_ahorro = "\n🎯 Ingresá tu meta total de ahorro: $"
mensaje_deposito = "💵 Ingresá tu depósito: $"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ahorro(
    id_meta INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ahorro INTEGER NOT NULL);
    """)                
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro_ahorro(
    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    monto INTEGER NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);
    """)                
    conexion.commit()
    conexion.close()
print("¡Base de datos  creada con éxito!")

def ingreso_ahorro(ahorro_ingresado):
        
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO ahorro(ahorro)
        VALUES(?)""",(ahorro_ingresado,))
        conexion.commit()
        conexion.close()

def registrar_deposito(monto_ingresado):
      
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO registro_ahorro(monto)
        VALUES(?)""",(monto_ingresado,))
        conexion.commit()
        conexion.close()
    
def obtener_total_ahorrado():
      
      conexion = conectar()
      cursor = conexion.cursor()
      cursor.execute(" SELECT SUM(monto) FROM registro_ahorro")
      total = cursor.fetchone()[0] or 0
      conexion.close()
      return total

def contabilizar_depositos():
     
     conexion = conectar()
     cursor = conexion.cursor()
     cursor.execute("SELECT COUNT(*)FROM registro_ahorro")
     total_depositos = cursor.fetchone()[0] or 0
     conexion.close()
     return total_depositos

def mostrar_historial_completo():
    """Trae todos los registros históricos y los imprime en una tabla"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Le pedimos las 3 cosas exactas que querés mostrar
    cursor.execute("SELECT fecha, id_transaccion, monto FROM registro_ahorro")
    registros = cursor.fetchall()
    conexion.close()
    
    if registros:
        print("\n" + "="*55)
        print("🧾 HISTORIAL COMPLETO DE MOVIMIENTOS".center(55))
        print("="*55)
        # Tabulate hace la magia de armar la grilla
        print(tabulate(registros, headers=["Fecha y Hora", "Nro. Depósito", "Monto ($)"], tablefmt="grid"))
    else:
        print("\n⚠️ Todavía no hay movimientos registrados.")

def limpiar_historial_viejo():
    """Vacía las tablas y resetea los contadores de autoincremento"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. Borramos los datos reales
    cursor.execute("DELETE FROM registro_ahorro")
    cursor.execute("DELETE FROM ahorro")
    
    # 2. ⚡ LA MAGIA: Reseteamos los contadores internos del sistema
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='registro_ahorro'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='ahorro'")
    
    conexion.commit()
    conexion.close()
    print("🧹 ¡Historial viejo eliminado y contadores reseteados a 1!")

def pedir_numero(mensaje):
    
    texto =  input(mensaje).strip()
    if  re.match(r"^[1-9][0-9]*$",texto):
        return int(texto)
    else:
        print(mensaje_ahorro_error_numerico)
    
    return pedir_numero(mensaje)

   

def simulador_ahorro():
        
    crear_base_datos()
    limpiar_historial_viejo()
    ahorro = pedir_numero(mensaje_ahorro)
    ingreso_ahorro(ahorro)
         
    meta_ahorro = False
    print("\n" + "=" * 50)
    print("🏦 INICIANDO SIMULADOR DE CAJERO fintech babul".center(50))
    print("=" * 50)
        
    while not meta_ahorro:
        
        deposito = pedir_numero(mensaje_deposito)
        registrar_deposito(deposito)
        
        deposito_acumulado = obtener_total_ahorrado()
        deposito_contados =  contabilizar_depositos()
        faltante = ahorro - deposito_acumulado
        
        if faltante < 0:
            faltante = 0
        
        historial_depositos = [[deposito_contados,f'{deposito}' ,f'{deposito_acumulado}' , f'{faltante}']]
        headers = [ " # Nro deposito" ," Monto Ingresado ", "Deposito Acumulado" , "Faltante"]
        print(tabulate(historial_depositos, headers=headers , tablefmt = "grid"))
        print("")
        
        if deposito_acumulado >= ahorro:
            print("🎉 ¡OBJETIVO ALCANZADO! ✅")
            print(f"📊 Estadísticas finales: Se realizaron {deposito_contados} depósitos válidos.")
            mostrar_historial_completo()
            meta_ahorro = True  # 🛑 APAGA EL BUCLE AUTOMÁTICAMENTE

simulador_ahorro()
    
    
    



















