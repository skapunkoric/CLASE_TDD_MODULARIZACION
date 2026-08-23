import pytest
import sqlite3
import bd.database as db

@pytest.fixture(autouse=True)
def db_temporal(tmp_path):
    "crea la ruta y la base temporal"
    ruta_temporal = tmp_path /"test_inventario.db"
    db.DB_NAME = str(ruta_temporal)
    db.limpiar_historial_viejo()
    db.crear_base_datos()
    yield
def test_la_tabla_inventario_se_crea_correctamente_y_no_en_sqlmaster_negative_path():
    conexion = db.conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name='inventario'")
    tabla_encontrada = cursor.fetchone()
    conexion.close()
    assert tabla_encontrada is not None

def test_la_tabla_inventario_se_crea_correctamente_y_happy_path():
    conexion = db.conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventario WHERE id_producto = 1")
    tabla_encontrada = cursor.fetchone()
    conexion.close()
    assert tabla_encontrada[0] == 1


def test_de_stock_bd_completo():
    "Prueba que los inserts automaticos en la tabla existan"
    # 2. Obtenemos el resultado
    productos = db.mostrar_estado_stock_completo()
    # 3. Verificamos (Asserts)
    assert productos[0][1] == "A"
    assert productos[1] == (2, "B", 0, None), "El producto no se encuentra"

def test_obtener_cantidades_stock_trae_todos_los_productos():
    "obtiene cantidades de stock y compara "
    resultados = db.obtener_cantidades_stock()
    assert len(resultados) == 6
    assert resultados[0][1] == 5

def test_que_muestra_stock_con_numero_de_id():
    "obtiene cantidades con el id de producto"
    resultado = db.mostrar_stock_con_numero_de_id(2)
    assert resultado[0][2] == 0

def test_que_muestra_stock_con_numero_de_cantidad_definido():
    "obtiene cantidades con segun la cantidad que tiene el producto"
    resultado = db.mostrar_stock_con_numero_definido(12)
    assert resultado[0][2] == 12

def test_actualizar_estado_producto_funciona_correctamente():
    "verifica que actualiza el stock de un producto"
    db.actualizar_estado_producto(1,"✅ [STOCK OK]")
    producto_modificado = db.obtener_un_producto(1)
    assert producto_modificado[2] == "✅ [STOCK OK]"

def test_actualizar_un_producto_actualiza_correctamente():
    "verifica que actualiza el stock de un producto"
    db.actualizar_producto(2,"",99,"")
    producto_modificado = db.obtener_un_producto(2)
    assert producto_modificado[1] == 99



