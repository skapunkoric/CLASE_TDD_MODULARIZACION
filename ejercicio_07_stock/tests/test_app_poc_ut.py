import builtins
import unittest
import app.validador as val
from unittest.mock import patch


class TestValidador(unittest.TestCase):

    # ==========================================
    # 🟢 HAPPY PATH
    # ==========================================
    def test_determinar_estado_stock_ok(self):
       """Prueba si la cantidad es mayor a 3, devuelve STOCK OK"""
       valor= val.determinar_estado_stock(12)
       self.assertEqual(valor,"✅ [STOCK OK]")
       valor_dos = val.determinar_estado_stock(4)
       self.assertEqual(valor_dos, "✅ [STOCK OK]")

     # ==========================================
     # 🟡 EDGE CASES (Casos Límite)
     # ==========================================
    def test_determinar_estado_stock_bajo_limite_superior(self):
      """Prueba  que el limite exacto a igual a 3, devuelve STOCK BAJO"""
      resultado = val.determinar_estado_stock(3)
      self.assertEqual(resultado, "⚠️ [STOCK BAJO]")

    def test_determinar_estado_stock_bajo_limite_inferior(self):
      """Prueba que el limite minimo antes de 0 tomamo 1, debe ser STOCK BAJO"""
      resultado = val.determinar_estado_stock(1)
      self.assertEqual(resultado, "⚠️ [STOCK BAJO]")

    def test_determinar_estado_sin_stock_(self):
      """Prueba que el valor 0 exactp,debe ser STOCK BAJO"""
      resultado = val.determinar_estado_stock(0)
      self.assertEqual(resultado, "❌ [SIN STOCK]")

# ==========================================
# 🔴 NEGATIVE PATH
# ==========================================
    def test_determinar_estado_stock_negativo_lanza_error(self):
        """El sistema no debe permitir stock negativo (ej. -5). El patovica levanta ValueError."""
        with self.assertRaises(ValueError):
            val.determinar_estado_stock(-5)

    @patch('app.validador.cantidad_usuario')
    @patch('builtins.input')
    def test_updatear_productos_mantiene_valores_con_enter(self, mock_input, mock_cantidad):
        """Verifica que si el usuario escribe datos vacios, la función los devuelva correctamente"""
        mock_input.return_value = ""
        mock_cantidad.return_value = ""
        nombre_n, cantidad_n, estado_n = val.updatear_productos("A", 5, "✅ [STOCK OK]")
        self.assertEqual(nombre_n,"")
        self.assertEqual(cantidad_n,"")
        self.assertEqual(estado_n, "")

    @patch('app.validador.cantidad_usuario')
    @patch('builtins.input')
    def test_updatear_productos_modifica_con_valores_nuevos(self, mock_input, mock_cantidad):
        """Verifica que si el usuario escribe datos, la función los devuelva correctamente"""
        mock_input.side_effect = ["reemplazo de A", "⚠️ [STOCK BAJO]"]
        mock_cantidad.return_value = 2
        nombre_n, cantidad_n, estado_n = val.updatear_productos("A", 5, "✅ [STOCK OK]")
        self.assertEqual(nombre_n,"reemplazo de A")
        self.assertEqual(cantidad_n, 2)
        self.assertEqual(estado_n,"⚠️ [STOCK BAJO]")


if __name__ == "__main__":
    unittest.main()