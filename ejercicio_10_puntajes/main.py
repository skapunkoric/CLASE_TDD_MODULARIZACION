import sqlite3
from tabulate import tabulate
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bd.database as db


def reporte_encabezado(mensaje):
    "crear el encabezado de los repores"
    print("\n" + "=" * 24)
    print(mensaje)
    print("=" * 24)


def visualizar_reportes():
    "crea la bd , carga product,mostra los reportes"
    db.crear_tabla()
    db.cargar_datos()

    cantidad_max = db.obtener_jugadores_top_max()
    reporte_encabezado("PUNTAJES JUGADORES TOP 🥇 MAXINOS")
    headers=("Jugador" ,"MAXIMO_PUNTAJES")
    print(tabulate (cantidad_max,headers=headers, tablefmt="grid"))    

    cantidad_min = db.obtener_jugadores_top_min()
    reporte_encabezado("PUNTAJES JUGADORES TOP 🥉 MIMIMOS")
    headers=("MINIMOS_PUNTAJES" ,"Jugador")
    print(tabulate (cantidad_min,headers=headers, tablefmt="grid"))

    promedio = db.obtener_promedio_general()
    reporte_encabezado("PUNTAJES JUGADORES PROMEDIO ")
    print(tabulate ([promedio], headers=["PROMEDIO"], tablefmt="grid"))

    cantidad_max_players = db.obtener_cantidades_empates_top()    
    reporte_encabezado("PUNTAJES CANTIDAES TOP 🥇 MAXINOS")
    headers=[("MAXIMO_PUNTAJES")]
    print(tabulate (cantidad_max_players,headers=headers, tablefmt="grid"))


    cantidad_top_800 = db.obtener_reporte_de_mas_800_top()
    reporte_encabezado("PUNTAJES TOP 800 🥇 MAXINOS")
    headers=("JUGADOR","PUNTAJE")
    print(tabulate (cantidad_top_800,headers=headers, tablefmt="grid"))
    


if __name__ == "__main__":
   visualizar_reportes()

    

