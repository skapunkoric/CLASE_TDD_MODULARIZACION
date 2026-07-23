import os
import sqlite3

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "gastos.db")


def conectar():
    """Conecta a la base de datos gastos.db de sqlite3"""
    return sqlite3.connect(DB_NAME)


def crear_base_datos():
    """Crea las tablas como gasto de la bd"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS gasto
                   (
                       id_gasto
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT
                       NOT
                       NULL,
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
                   )
                   """)
    conexion.commit()
    conexion.close()


def ingreso_gasto_bd(monto_ingresado):
    """Ingresa los datos por parametros a la bd"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
                   INSERT INTO gasto(monto)
                   VALUES (?)""", (monto_ingresado,))
    conexion.commit()
    conexion.close()


def consultas_bd():
    """Consulta y devuelve suma, cantidad y promedio del ingreso en un diccionario"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT SUM(monto) FROM gasto")
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM gasto")
    gasto_valido = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(monto) FROM gasto")
    promedio = round(cursor.fetchone()[0] or 0, 2)

    conexion.close()  # <-- Corregido: le faltaban los paréntesis

    # Devolvemos el diccionario para que el main.py lo pueda usar
    return {
        "total": total,
        "cantidad": gasto_valido,
        "promedio": promedio
    }


def limpiar_historial_viejo():
    """Vacía las tablas y resetea los contadores de autoincremento"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM gasto")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='gasto'")
    conexion.commit()
    conexion.close()