import unittest
import tempfile
import os
import bd.database as db


class TestBaseDeDatos(unittest.TestCase):

    def setUp(self):
        "se ejecuta antes de cada test"
        self.directorio_temp = tempfile.TemporaryDirectory()

        ruta_falsa = os.path.join(self.directorio_temp.name, "test_inventario.db")
        ruta_falsa = db.DB_NAME
        db.DB_NAME = ruta_falsa

        db.limpiar_historial_viejo()
        db.crear_base_datos()

    def tearDown(self):
        "se ejecuta antes de cada test"
        self.directorio_temp.cleanup()

    def test_la_tabla_inventario_se_crea_correctamente_y_no_en_sqlmaster_negative_path(self):
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name='inventario'")
        tabla_encontrada = cursor.fetchone()
        conexion.close()
        self.assertIsNotNone(tabla_encontrada,"¡Error! La tabla 'inventario' no fue creada.")

    def test_la_tabla_inventario_se_crea_correctamente_y_happy_path(self):
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM inventario WHERE id_producto = 1")
        tabla_encontrada = cursor.fetchone()
        conexion.close()
        self.assertEqual(tabla_encontrada[0],1, "el producto con id 1 no existe en la base de datos")

    def test_de_stock_bd_completo(self):
        "Prueba que los inserts automaticos en la tabla existan"
        # 2. Obtenemos el resultado
        productos = db.mostrar_estado_stock_completo()
        # 3. Verificamos (Asserts)
        self.assertEqual(productos[3][1], "D")
    def test_obtener_cantidades_stock_trae_todos_los_productos(self):
        "obtiene cantidades de stock y compara "
        resultados = db.obtener_cantidades_stock()
        self.assertEqual(len(resultados), 6)
        self.assertEqual(resultados[2][1], 12)

    def test_que_muestra_stock_con_numero_de_id(self):
        "obtiene cantidades con el id de producto"
        resultado = db.mostrar_stock_con_numero_de_id(6)
        self.assertEqual(resultado[0][2], 8)

    def test_que_muestra_stock_con_numero_de_cantidad_definido(self):
        "obtiene cantidades con segun la cantidad que tiene el producto"
        resultado = db.mostrar_stock_con_numero_definido(0)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0][2], 0)
        self.assertEqual(resultado[1][2], 0)

    def test_actualizar_estado_producto_funciona_correctamente(self):
        "verifica que actualiza el stock de un producto"
        db.actualizar_estado_producto(5,"✅ [STOCK OK]")
        producto_modificado = db.obtener_un_producto(5)
        self.assertEqual(producto_modificado[2],"✅ [STOCK OK]")

    def test_actualizar_un_producto_actualiza_correctamente(self):
        "verifica que actualiza el stock de un producto"
        db.actualizar_producto(5,"",99,"")
        producto_modificado = db.obtener_un_producto(5)
        self.assertEqual(producto_modificado[1],99)



if __name__ == "__main__":
    unittest.main()