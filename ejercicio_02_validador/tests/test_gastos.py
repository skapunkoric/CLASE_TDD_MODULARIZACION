import unittest
from app.validador import es_gasto_valido

class TestValidadorGastos(unittest.TestCase):
    
    # 🟢 Happy Path
    def test_happy_path_entero_positivo(self):
        """si recibe el string 0, debe retornar el entero 0 (condicion de corte)"""
        resultado = es_gasto_valido("150")
        self.assertEqual(resultado,150)
    
    # 🟡 EDGE CASE
    def test_edge_case_cero(self):
        "si recibe el string 0, debe retornar el entero 0 condicion de corte"
        resultado = es_gasto_valido("0")
        self.assertEqual(resultado,0)


    def test_negative_path_letras(self):
        "si recibe el caracteres no numericos, debe retornar none"
        #le pasamos el texto hardocodeado
        resultado = es_gasto_valido("hola")
        self.assertIsNone(resultado)

    def test_negative_path_negative(self):
        "si recibe un numero negativo, debe retornar None"
        resultado = es_gasto_valido("-10")
        self.assertIsNone(resultado)
    
    def test_negative_path_flotante(self):
        "si recibe un numero con decimales, debe retornar None"
        resultado = es_gasto_valido("-100.5")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()