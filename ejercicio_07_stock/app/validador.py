
def cantidad_usuario():
    cantidad_pedida = input("🔍 Ingrese la cantidad de stock a filtrar: ").strip()
    if cantidad_pedida.isdigit():
        return int(cantidad_pedida)
    else:
        print("⚠️ Error: Debe ingresar un número entero válido.")
        return None