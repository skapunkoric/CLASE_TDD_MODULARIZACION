import unittest
from app.validador import es_gasto_valido


    
    # 🟢 Happy Path
def test_happy_path_entero_positivo():
        # solo usamos 'assert' y comparamos con '=='
        assert es_gasto_valido("150") == 150
    
# 🟡 EDGE CASE
def test_edge_case_cero():
    assert es_gasto_valido("0") == 0
    


def test_negative_path_letras(self):
    # Comparamos con 'is' para verificar nulos
    
    assert es_gasto_valido("hola") is None
    

def test_negative_path_negative(self):
    assert es_gasto_valido("-10") is None
    

def test_negative_path_flotante(self):
    assert es_gasto_valido("-100.5") is None
    
