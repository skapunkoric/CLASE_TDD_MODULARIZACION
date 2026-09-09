# ------------------------------------------------------------
# Ejercicio complejo 10: Ranking de puntajes
# ------------------------------------------------------------
"""
Consigna:
Dada la lista puntajes = [450, 900, 1200, 300, 750, 1200, 100], analizar el ranking usando while.

Requisitos:
- Recorrer la lista con while.
- Encontrar el puntaje máximo.
- Encontrar el puntaje mínimo.
- Calcular el promedio de puntajes.
- Contar cuántos puntajes son mayores o iguales a 800.
- Contar cuántas veces aparece el puntaje máximo.
- Mostrar un resumen final con todos los datos.

Extra opcional:
- Crear una nueva lista llamada destacados con los puntajes mayores o iguales a 800.

Conceptos a practicar:
while, listas, índices, acumuladores, máximos, mínimos, contadores, append().

lista_jugadores = [(A, 450),
                   (B, 900),
                   (C, 1200),
                   (D, 300), 
                   (E, 750),
                   (F,1200), 
                   (G,100)]
Ejercicio 10 | Ranking de Puntajes (Edición SQL)
Objetivo Base:
Crear un programa que gestione una tabla de posiciones de un torneo o videojuego y devuelva estadísticas puras utilizando funciones de agregación de SQL.

Requisitos de la Base de Datos (La Estructura):
Crear una tabla llamada ranking con las columnas:

id_jugador (Autoincremental)
nombre_jugador (Texto)
puntaje (Entero)

Armar una función que inserte varios jugadores de prueba automáticamente. Tip de tester: Asegurate de cargar al menos dos jugadores distintos que compartan el mismo puntaje máximo para poner a prueba la lógica de duplicados.
La Magia (Los Reportes):
En lugar de traer toda la lista a Python y usar bucles for, tenés que armar funciones que usen consultas SQL directas para resolver la matemática e imprimir en consola:
El Top: Obtener el puntaje más alto de la tabla usando MAX().
El Fondo: Obtener el puntaje más bajo usando MIN().
La Media: Calcular el promedio general de todos los puntajes usando AVG().
El Desafío Picante: Armar una consulta que cuente exactamente cuántas personas empataron en el primer puesto (combinando COUNT() con el puntaje máximo).
Crear una nueva lista llamada destacados con los puntajes mayores o iguales a 800.
                
"""
import sqlite3
import os
from tabulate import tabulate
 
carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(carpeta_del_script, "puntajes.db")

def conectar():
    """ crea la bd """ 
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    """ crea la tabla  """ 
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
    """ carga los datos si existen no los carga """ 
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM ranking")
    cantidad_registros = cursor.fetchone()[0]
    if cantidad_registros > 0:
        print("ℹ️ La base de datos ya tiene información. Se cancela la carga inicial.")
        conexion.close()
        return # 👈
    lista_jugadores = [
        ("Anys", 450),
        ("Babul", 900),
        ("Caro", 1200),
        ("Defetones", 300), 
        ("Emi Martinez", 750),
        ("Fear",1200), 
        ("Gabriela",100)
        ]
    
    try:
        cursor.executemany("""
        INSERT INTO ranking(nombre_jugador, puntaje )
        VALUES (?, ?)""", lista_jugadores)
        conexion.commit()
        print("✅ Jugadores y Puntajes iniciales cargados con éxito.")
    except sqlite3.IntegrityError:
        print("ℹ️ Los Jugadores y Puntajes existen en la base de datos.")
    
    conexion.close()  


def visualizar_reportes():
    """crea la tabla y carga los datos y mostra los reportes de puntajes """
    """El Top: Obtener el puntaje más alto de la tabla usando MAX().
    El Fondo: Obtener el puntaje más bajo usando MIN().
    La Media: Calcular el promedio general de todos los puntajes usando AVG().
    El Desafío Picante: Armar una consulta que cuente exactamente cuántas personas empataron en el primer puesto (combinando COUNT() con el puntaje máximo).    
    Crear una nueva lista llamada destacados con los puntajes mayores o iguales a 800.
    """
    
    conexion = conectar()
    cursor = conexion.cursor()
    crear_tabla()
    cargar_datos()
    cursor.execute(""" SELECT nombre_jugador, puntaje from ranking WHERE puntaje = (SELECT MAX (puntaje) FROM ranking) """)
    cantidad_max = cursor.fetchall()
    reporte_encabezado("PUNTAJES JUGADORES TOP 🥇 MAXINOS")
    headers=("Jugador" ,"MAXIMO_PUNTAJES")
    print(tabulate (cantidad_max,headers=headers, tablefmt="grid"))
    
    cursor.execute(""" SELECT nombre_jugador, puntaje from ranking WHERE puntaje = (SELECT MIN (puntaje) FROM ranking) """)
    cantidad_min = cursor.fetchall()
    reporte_encabezado("PUNTAJES JUGADORES TOP 🥉 MIMIMOS")
    headers=("MINIMOS_PUNTAJES" ,"Jugador")
    print(tabulate (cantidad_min,headers=headers, tablefmt="grid"))
    
    cursor.execute(" SELECT AVG(puntaje) from ranking ")
    promedio = cursor.fetchone()
    reporte_encabezado("PUNTAJES JUGADORES PROMEDIO ")
    print(tabulate ([promedio], headers=["PROMEDIO"], tablefmt="grid"))
    
    cursor.execute(""" SELECT COUNT(*) FROM ranking WHERE puntaje=(SELECT MAX(puntaje) FROM ranking) """)
    cantidad_max = cursor.fetchall()
    reporte_encabezado("PUNTAJES CANTIDAES TOP 🥇 MAXINOS")
    headers=[("MAXIMO_PUNTAJES")]
    print(tabulate (cantidad_max,headers=headers, tablefmt="grid"))

    cursor.execute(""" SELECT nombre_jugador,puntaje FROM ranking WHERE puntaje >= 800 """)
    cantidad_top_800 = cursor.fetchall()
    reporte_encabezado("PUNTAJES TOP 800 🥇 MAXINOS")
    headers=("JUGADOR","PUNTAJE")
    print(tabulate (cantidad_top_800,headers=headers, tablefmt="grid"))
    conexion.close()

def reporte_encabezado(mensaje):
    "crear el encabezado de los repores"
    print("\n" + "=" * 24)
    print(mensaje)
    print("=" * 24)

visualizar_reportes()