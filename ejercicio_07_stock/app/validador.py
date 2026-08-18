

def cantidad_usuario(msg):
    """patovica que permite numeros positivos o string vacio (enter)"""
    while True:
        entrada = input(msg).strip()
        if entrada == "":
            return ""

        if entrada.isdigit():
            return int(entrada)
    
        print("⚠️ Error: Debe ingresar un número entero positivo válido o presione enter para omitir.")
        


def determinar_estado_stock(cantidad):
    "funcion pura que recibe un numero y devuelve un string"    
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa") # ¡Acá explota para que el test lo atrape!
    if cantidad == 0:
        return "❌ [SIN STOCK]"
    elif cantidad <= 3:
        return "⚠️ [STOCK BAJO]"
    else:
        return "✅ [STOCK OK]"

def updatear_productos(nombre_antiguo, cantidad_antigua, estado_antiguo):
    "cambiar datos de los productos del inventario para actualizar, Devuelve strings vacíos si el usuario da Enter."""
    print("\n--- MODIFICAR PRODUCTO ---")
    print("(Presioná Enter sin escribir nada para mantener el valor actual)")
    nombre_act = input(f"Nombre Anterior[{nombre_antiguo}],Nuevo Nombre del producto: ").strip()
    cantidad_act = cantidad_usuario(f"Cantidad anterior [{cantidad_antigua}]Ingrese Nueva cantidad: ")
    estado_stock_act = input(f"Estado Anterio [{estado_antiguo}],Nuevo Estado de Stock: ").strip()

    return nombre_act, cantidad_act, estado_stock_act
