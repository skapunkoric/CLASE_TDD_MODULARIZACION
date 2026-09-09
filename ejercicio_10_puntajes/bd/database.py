import sqlite3
import os
carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "puntajes.db")

def conectar():
    "crea la bd"
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    "crea la table"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranking(
    id_jugador INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nombre_jugador TEXT NOT NULL,
    puntaje INTEGER NOT NULL
                   )
    """)
    conexion.commit()
    conexion.close()

def cargar_datos():
    "carga los datos si existen los carga"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM ranking")
    cantidad_registros = cursor.fetchone()[0]
    if cantidad_registros > 0:
        print("  La base de datos ya tiene información. Se cancela la carga inicial.")
        conexion.close()
        return 

    lista_jugadores = [
        ("Anys", 450),
        ("Babul", 900),
        ("Caro", 1200),
        ("Deftones", 300), 
        ("Emi Martinez", 750),
        ("Fear",1200), 
        ("Gabriela",100)
    ]
    # Como ya pasamos el escudo, insertamos directo sin miedo
    cursor.executemany("""
    INSERT INTO ranking(nombre_jugador, puntaje )
    VALUES (?, ?)""", lista_jugadores)
    conexion.commit()
    print("  Jugadores y Puntajes iniciales cargados con éxito.")
    conexion.close()

def obtener_jugadores_top_max():
    "mostra los reportes de puntajes MAX top"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" SELECT nombre_jugador, puntaje from ranking WHERE puntaje = (SELECT MAX (puntaje) FROM ranking) """)
    top_max_players = cursor.fetchall()
    conexion.close()
    return top_max_players

def obtener_jugadores_top_min():
    "mostra los reportes de puntajes MIN top"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" SELECT nombre_jugador, puntaje from ranking WHERE puntaje = (SELECT MIN (puntaje) FROM ranking) """)
    cantidad_min = cursor.fetchall()
    conexion.close()
    return cantidad_min


def obtener_promedio_general():
    "mostra los reportes de promedios puntajes"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(" SELECT AVG(puntaje) from ranking ")
    promedios = cursor.fetchone()
    conexion.close()
    return promedios

def obtener_cantidades_empates_top():
    "mostra los reportes de empates tops"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" SELECT COUNT(*) FROM ranking WHERE puntaje=(SELECT MAX(puntaje) FROM ranking) """)
    ranking_max = cursor.fetchall()
    conexion.close()
    return ranking_max

def obtener_reporte_de_mas_800_top():
    "mostra los reportes de tops 800 o mas"
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" SELECT nombre_jugador,puntaje FROM ranking WHERE puntaje >= 800 """)
    cantidad_top_800 = cursor.fetchall()
    conexion.close()
    return cantidad_top_800
