# import funciones y correr como main.py

import bd.database as db
from app.validador import es_gasto_valido
from tabulate import tabulate

mensaje_gasto = "💵 Ingresá el importe del gasto (0 para terminar): "
mensaje_error = "⚠️ Error: El importe no puede ser un número negativo o letras. Volvé a intentar."

def reporte_encabezado(mensaje):        
    print("\n" + "=" * 24)
    print(mensaje)
    print("=" * 24)

def reporte_dashboard():
    # 1. Atrapamos el diccionario que escupe database.py
    metricas = db.consultas_bd()
    
    reporte_encabezado("📊 DASHBOARD GLOBAL DE GASTOS")
    
    # 2. Inyectamos los datos del diccionario en la lista
    resumen = [
        ["💰 Total gastado: $", metricas["total"]],
        ["⚖️ Promedio por gasto: $", metricas["promedio"]],
        ["📋 Cantidad de gastos cargados:", metricas["cantidad"]]
    ]
    print(tabulate(resumen, headers=["Métrica", "Valor"], tablefmt='grid'))

def simulador_gasto():
    print("Iniciando sistema de gastos...")
    db.crear_base_datos()
    db.limpiar_historial_viejo()
    print("🧹 ¡Historial viejo eliminado y contadores reseteados a 1!")
    
    while True:
        # Pide el input
        texto = input(mensaje_gasto).strip()
        
        # Manda a validar a la capa app
        gasto_limpio = es_gasto_valido(texto)
        
        # Evalúa la respuesta
        if gasto_limpio is not None:
            if gasto_limpio == 0:
                break # Corta el bucle si es 0
            
            # Guarda en la capa bd si es mayor a 0
            db.ingreso_gasto_bd(gasto_limpio)
            print(f"✅ Gasto de ${gasto_limpio} guardado con éxito.")
        else:
            print(mensaje_error)

    print("🛑 Finalizando la carga de gastos...")    
    reporte_dashboard()

if __name__ == "__main__":
    simulador_gasto()