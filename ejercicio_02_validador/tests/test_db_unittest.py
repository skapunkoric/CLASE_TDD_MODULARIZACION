import unittest
import sqlite3
# importamos tu bd
import bd.database as db
class TestBaseDeDatos(unittest.TestCase):
    # truco para que no toque .db real y use la RAM compartida
    def setUp(self):
        # open conexion master
        self.conexion_maestra = sqlite3.connect("file::memory:?cache=shared", uri=True)
        # a memory
        db.conectar = lambda: sqlite3.connect("file::memory:?cache=shared", uri=True)
        db.crear_base_datos()
        db.limpiar_historial_viejo()


    def tearDown(self):
        "se ejecuta despues de cada test"
        # cerramos la master, destruyendo la ram
        self.conexion_maestra.close()
    

    def test_ingreso_y_consultas_db(self):
        "prueba que los inserts modifiquen correctamente el dashboard"
        # 1. accion agregar 2 gastos
        db.ingreso_gasto_bd(100)
        db.ingreso_gasto_bd(50)
        # 2. obtenemo el result
        metricas = db.consultas_bd()
        # verificamos (asserts)
        self.assertEqual(metricas["total"],150)
        self.assertEqual(metricas["cantidad"], 2)
        
    
    def test_la_tabla_gasto_se_crea_correctamente(self):
        "probo existe de table "
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gasto'")
        tabla_encontrada = cursor.fetchone()
        conexion.close()




if __name__ == '__main__':
    unittest.main()
