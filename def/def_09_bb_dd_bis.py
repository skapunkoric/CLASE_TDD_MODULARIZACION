import re
import sqlite3
from tabulate import tabulate

def conectar():
    # Usamos base temporal en memoria para testear rápido
    return sqlite3.connect(":memory:")

def crear_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    # Separamos con punto y coma (;) las dos instrucciones SQL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ahorro(
        id_meta INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ahorro INTEGER NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro_ahorro(
        id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        monto INTEGER NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    """)                
    conexion.commit()
    conexion.close()
    print("✅ ¡Base de datos en memoria creada con éxito!\n")

def guardar_meta_inicial(monto_meta):
    """Guarda la meta en la tabla de configuración"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO ahorro (ahorro) VALUES (?)", (monto_meta,))
    conexion.commit()
    conexion.close()

def registrar_deposito(monto_ingresado):
    """Guarda el depósito en el historial"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO registro_ahorro (monto) VALUES (?)", (monto_ingresado,))
    conexion.commit()
    conexion.close()

def obtener_total_ahorrado():
    """Le pide a SQLite que sume todo el historial"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(monto) FROM registro_ahorro")
    # Si la tabla está vacía, fetchone()[0] devuelve None. Le decimos que si es None, use 0.
    total = cursor.fetchone()[0] or 0 
    conexion.close()
    return total

# =======================================================
# 🔥 EL MOTOR DEL PROGRAMA (Adiós while True)
# =======================================================
def iniciar_simulador():
    crear_base_datos()
    
    # 1. PEDIMOS LA META (Una sola vez)
    while True: # Usamos un while chiquito solo para validar el primer input
        ingreso_meta = input("🎯 Ingresa la Cantidad de DINERO que Deseas Ahorrar: $")
        if re.match(r"^[1-9][0-9]*$", ingreso_meta): 
            meta = int(ingreso_meta)
            guardar_meta_inicial(meta)
            break
        else:
            print("❌ Monto inicial no válido.")

    # 2. LA BANDERA DE ESTADO
    meta_alcanzada = False
    
    # 3. EL BUCLE CONTROLADO (Se repite mientras la meta_alcanzada sea Falsa)
    while not meta_alcanzada:
        
        deposito_input = input("\n💵 Ingresá dinero a la alcancía (o 'salir'): ")
        
        if deposito_input.lower() == 'salir':
            print("👋 Saliendo del simulador...")
            break
            
        if not re.match(r"^[1-9][0-9]*$", deposito_input):
            print("❌ Ingreso no válido. Solo números enteros positivos.")
            continue # Vuelve al principio del while
            
        # Si llegamos acá, el número es válido. Lo guardamos en SQLite.
        deposito = int(deposito_input)
        registrar_deposito(deposito)
        
        # 4. CALCULAMOS CÓMO VENIMOS
        total_acumulado = obtener_total_ahorrado()
        falta = meta - total_acumulado
        
        if total_acumulado >= meta:
            print(f"\n🎉 ¡OBJETIVO ALCANZADO! Ahorraste ${total_acumulado}")
            meta_alcanzada = True # 🛑 APAGA EL BUCLE PRINCIPAL
        else:
            print(f"✅ Depositaste ${deposito}. Llevás ${total_acumulado}. Te faltan ${falta} para la meta.")

iniciar_simulador()