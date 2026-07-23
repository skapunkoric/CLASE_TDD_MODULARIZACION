import re
import os
import sqlite3
from tabulate import tabulate

# ==================================================================
# 1. CONFIGURACIÓN
# ==================================================================
carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "ahorro.db")

mensaje_ahorro_error_numerico = "⚠️ Error: Por favor, ingresá un monto numérico entero y mayor a cero."
mensaje_ahorro = "\n🎯 Ingresá tu meta total de ahorro: $"
mensaje_deposito = "💵 Ingresá tu depósito: $"


# ==================================================================
# 2. CAPA DE BASE DE DATOS (DAO)
# ==================================================================
def conectar():
    return sqlite3.connect(DB_NAME)


def crear_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ahorro
                   (
                       id_meta
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       meta_total
                       INTEGER
                       NOT
                       NULL
                   );
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS registro_ahorro
                   (
                       id_transaccion
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       monto
                       INTEGER
                       NOT
                       NULL,
                       fecha
                       DATETIME
                       DEFAULT
                       CURRENT_TIMESTAMP
                       NOT
                       NULL
                   );
                   """)
    conexion.commit()
    conexion.close()
    print("✅ ¡Base de datos iniciada con éxito!")


def guardar_meta_inicial(monto_meta):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO ahorro(meta_total) VALUES(?)", (monto_meta,))
    conexion.commit()
    conexion.close()


def registrar_deposito(monto_ingresado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO registro_ahorro(monto) VALUES(?)", (monto_ingresado,))
    conexion.commit()
    conexion.close()


def obtener_total_ahorrado():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(monto) FROM registro_ahorro")
    total = cursor.fetchone()[0] or 0
    conexion.close()
    return total


def contabilizar_depositos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM registro_ahorro")
    total_depositos = cursor.fetchone()[0] or 0
    conexion.close()
    return total_depositos


# ==================================================================
# 3. CAPA DE LÓGICA Y CONTROL
# ==================================================================
def pedir_numero(mensaje):
    """Usa recursividad pura. Sin bucles while."""
    texto = input(mensaje).strip()
    if re.match(r"^[1-9][0-9]*$", texto):
        return int(texto)
    else:
        print(mensaje_ahorro_error_numerico)
        return pedir_numero(mensaje)  # Vuelve a intentarlo


def simulador_ahorro():
    crear_base_datos()

    # 1. CONFIGURAR LA META (Una sola vez)
    meta_objetivo = pedir_numero(mensaje_ahorro)
    guardar_meta_inicial(meta_objetivo)

    # 2. BANDERA DE ESTADO PARA EL BUCLE
    objetivo_alcanzado = False

    # 3. BUCLE PRINCIPAL CONTROLADO
    print("\n" + "=" * 50)
    print("🏦 INICIANDO SIMULADOR DE CAJERO".center(50))
    print("=" * 50)

    while not objetivo_alcanzado:
        # Pedimos plata y guardamos
        deposito = pedir_numero(mensaje_deposito)
        registrar_deposito(deposito)

        # Consultamos las estadísticas a la BBDD
        deposito_acumulado = obtener_total_ahorrado()
        depositos_contados = contabilizar_depositos()
        faltante = meta_objetivo - deposito_acumulado

        # Evitamos que el faltante muestre números negativos si se pasa
        if faltante < 0:
            faltante = 0

        # Reporte visual
        historial = [[depositos_contados, f"${deposito}", f"${deposito_acumulado}", f"${faltante}"]]
        headers = ["Nro Depósito", "Monto Ingresado", "Acumulado Total", "Faltante"]
        print(tabulate(historial, headers=headers, tablefmt="grid"))
        print("")  # Espacio en blanco

        # Evaluación de la regla de negocio
        if deposito_acumulado >= meta_objetivo:
            print("🎉 ¡OBJETIVO ALCANZADO! ✅")
            print(f"📊 Estadísticas finales: Se realizaron {depositos_contados} depósitos válidos.")
            objetivo_alcanzado = True  # 🛑 APAGA EL BUCLE AUTOMÁTICAMENTE


# ==================================================================
# 🔥 EJECUCIÓN
# ==================================================================
if __name__ == "__main__":
    simulador_ahorro()