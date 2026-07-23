import re
import bd.database as db 
from tabulate import tabulate
import validador as v


    
def reporte(mensaje, titulo_reporte="REPORTE DE CONTROL DE STOCK"):
    print("\n" + "=" * 40)
    print(f"== {titulo_reporte} ==")
    print("=" * 40)
    print(tabulate(mensaje, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))


def mostra_producto_segun_input_usuario():
    cantidad_numerica = v.cantidad_usuario()
    if cantidad_numerica is None:
      cantidad_numerica = v.cantidad_usuario()
    else:
        datos = db.mostrar_stock_con_numero_definido(cantidad_numerica)
        reporte(datos)




    
    