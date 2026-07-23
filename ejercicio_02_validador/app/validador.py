# ------------------------------------------------------------
# Ejercicio complejo 2: Registro de gastos
# ------------------------------------------------------------
"""
Consigna:
Crear un programa que registre gastos hasta que el usuario escriba 0.

Requisitos:
- Pedir importes de gastos uno por uno.
- Si el usuario ingresa 0, terminar la carga.
- Si ingresa un número negativo, mostrar un error y volver a pedir el dato.
- Acumular el total de gastos válidos.
- Contar cuántos gastos válidos se ingresaron.
- Al final, mostrar:
  - Total gastado.
  - Cantidad de gastos cargados.
  - Promedio de gasto, solo si se cargó al menos un gasto.
"""
import re

def es_gasto_valido(texto_ingresado):
  """
    Función PURA: Solo valida, no imprime ni pide datos.
    Si el string es un número positivo o cero, retorna el entero.
    Si es inválido o negativo, retorna None.
  """
  if re.match(r"^-?\d+$", texto_ingresado):
      gasto = int(texto_ingresado)
      if gasto >= 0:
          return gasto
          
  return None    







 

    
    

       

        


    
    
    



















