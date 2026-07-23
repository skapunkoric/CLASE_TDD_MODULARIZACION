import unittest
import sqlite3
# Importamos tu módulo de base de datos
import bd.database as db


class TestBaseDeDatos(unittest.TestCase):

    def setUp(self):
        # ⚡ EL TRUCO: Sobrescribimos la función conectar temporalmente
        # para que no toque tu archivo .db real y use la RAM compartida
        db.conectar = lambda: sqlite3.connect("file::memory:?cache=shared", uri=True)

        # Preparamos el terreno limpio
        db.crear_base_datos()
        db.limpiar_historial_viejo()

    def test_ingreso_y_consultas_bd(self):
        """Prueba que los inserts modifiquen correctamente el dashboard"""

        # 1. Ejecutamos la acción (Agregamos 2 gastos)
        db.ingreso_gasto_bd(100)
        db.ingreso_gasto_bd(50)

        # 2. Obtenemos el resultado
        metricas = db.consultas_bd()

        # 3. Verificamos (Asserts)
        self.assertEqual(metricas["total"], 150)
        self.assertEqual(metricas["cantidad"], 2)
        self.assertEqual(metricas["promedio"], 75.0)


if __name__ == "__main__":
    unittest.main()