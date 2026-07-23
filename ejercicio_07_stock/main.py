# import funciones y correr como main.py

import bd.database as db
from app.validador as  import cantidad_usuario
from tabulate import tabulate
    
def reporte(mensaje, titulo_reporte="REPORTE DE CONTROL DE STOCK"):
    "mostra reporte"
    print("\n" + "=" * 40)
    print(f"== {titulo_reporte} ==")
    print("=" * 40)
    #print(tabulate(mensaje, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))

def mostrar_estado_stock_completo():
    ""
    stock_prod = db.mostrar_estado_stock_completo()
    reporte("REPORTE DE CONTROL DE STOCK")
    print(tabulate(stock_prod, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))


def mostra_producto_segun_input_usuario():
    ""
    cantidad_numerica = v.cantidad_usuario()
    if cantidad_numerica is None:
        cantidad_numerica = v.cantidad_usuario()
    else:
        datos = db.mostrar_stock_con_numero_definido(cantidad_numerica)
    return 
    reporte()
    tprint(tabulate(mensaje, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))



def inventario():
    ""
    print("Iniciando sistema de inventario...")
    db.crear_base_datos()    
    mostrar_estado_stock_completo()
    mostra_producto_segun_input_usuario()


if __name__ == "__main__":
    inventario()

































