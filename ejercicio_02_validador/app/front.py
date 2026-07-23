#capa front 
import re
import bd.database as db 
from tabulate import tabulate

mensaje_gasto = "💵 Ingresá el importe del gasto (0 para terminar):"
mensaje_error =  "⚠️ Error: El importe no puede ser un número negativo. Volvé a intentar."

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

def reporte_encabezado(mensaje):        
    "mostra el reporte en consola"
    print("\n" + "=" * 24)
    print(mensaje)
    print("=" * 24)

def reporte_dashoboard():
    "mostra el reporte de/los ingreso/s cargados"
    db.consultas_bd()
    reporte_encabezado("📊 DASHBOARD GLOBAL DE GASTOS")
    resumen = [
        [f"💰 Total gastado:$",total],
        [f" ⚖️ Promedio por gasto: $", promedio],
        [f"📋 Cantidad de gastos cargados:", gasto_valido]
            ]
    print(tabulate(resumen,headers=["Metica", "Valor"], tablefmt='grid'))