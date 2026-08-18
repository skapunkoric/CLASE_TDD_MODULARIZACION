import bd.database as db
import app.validador as valid
from tabulate import tabulate
    
def reporte(mensaje, titulo_reporte="REPORTE DE CONTROL DE STOCK"):
    "mostra reporte"
    print("\n" + "=" * 40)
    print(f"== {titulo_reporte} ==")
    print("=" * 40)
    print(tabulate(mensaje, headers=["ID", "NOMBRE", "CANTIDAD", "ESTADO STOCK"], tablefmt="grid"))

def mostrar_estado_stock_completo():
    "mostra reporte completo"
    stock_prod = db.mostrar_estado_stock_completo()
    reporte(stock_prod, "REPORTE DE CONTROL DE STOCK")
    
def mostrar_producto_segun_id():
    "mostra producto por id con datos completo"
    if db.hay_productos():
        mostrar_estado_stock_completo()
    else:
        print("No hay productos en la base de datos.")
        return None
        
    id_product = valid.cantidad_usuario("ingrese el numero de id de producto: ")
    if id_product == "":
        return
        
    stock_por_id = db.mostrar_stock_con_numero_de_id(id_product)
    reporte(stock_por_id, "MUESTRA POR ID EL PRODUCTO COMPLETO")

def mostra_cantidad_producto_segun_input_usuario():
    "mostra reporte segun cantidad"
    cantidad_numerica = valid.cantidad_usuario("ingrese la cantidad a filtrar: ")
    if cantidad_numerica == "":
        return
    datos = db.mostrar_stock_con_numero_definido(cantidad_numerica)
    reporte(datos, "FILTRADO POR CANTIDAD:")

def sincronizar_estados_inventario():
    "sincronizar inventarios con en bbdd y la logico de negocio"
    stock_crudos = db.obtener_cantidades_stock()
    for id_prod, cantidad in stock_crudos:
        nuevo_estado = valid.determinar_estado_stock(cantidad)
        db.actualizar_estado_producto(id_prod, nuevo_estado)

    print("✅ Estados sincronizados con éxito.")

def actualizar_productos():
    "actualiza nombre,cantidad,estado del producto del inventario"
    db.mostrar_estado_stock_completo()
    id_producto = valid.cantidad_usuario("ingrese id de producto valido: ")
    
    if id_producto == "":
        print("⚠️ Operación cancelada.")
        return
        
    # Usamos la función nueva para evitar el ValueError del desempaquetado
    producto_old = db.obtener_un_producto(id_producto)  
    
    if producto_old is None:
        print(f"❌ Error: No se encontró el producto con ID {id_producto}.")
        return

    nombre_v, cantidad_v, estado_v = producto_old

    nombre_n, cantidad_n, estado_n = valid.updatear_productos(nombre_v, cantidad_v, estado_v)
    exito = db.actualizar_producto(id_producto, nombre_n, cantidad_n, estado_n)
    if exito:
        print(f"✅ ¡Producto ID {id_producto} actualizado con éxito!")
    else:
        print(f"❌ Error: No se encontró el producto o el inventario está vacío.")

def inventario():
    "crea la bb.dd. , carga productos "
    print("Iniciando sistema de inventario...")
    db.limpiar_historial_viejo()
    db.crear_base_datos()
    
    mostrar_estado_stock_completo()
    sincronizar_estados_inventario()
    mostrar_estado_stock_completo()
    
    mostra_cantidad_producto_segun_input_usuario()
    mostrar_producto_segun_id()
    actualizar_productos()
    mostrar_producto_segun_id()

if __name__ == "__main__":
    inventario()