import builtins

import app.validador as val
import pytest
from unittest.mock import patch

# ==========================================
# 🟢 HAPPY PATH
# ==========================================
def test_determinar_estado_stock_ok():
    """Prueba si la cantidad es mayor a 3, devuelve STOCK OK"""
    assert val.determinar_estado_stock(12) == "✅ [STOCK OK]"
    assert val.determinar_estado_stock(4) == "✅ [STOCK OK]"

# ==========================================
# 🟡 EDGE CASES (Casos Límite)
# ==========================================
def test_determinar_estado_stock_bajo_limite_superior():
    """Prueba que el limite exacto a igual a 3, devuelve STOCK BAJO"""
    assert val.determinar_estado_stock(3) == "⚠️ [STOCK BAJO]"

def test_determinar_estado_stock_bajo_limite_inferior():
        """Prueba que el limite minimo antes de 0,tomamos 1 , devuelve STOCK BAJO"""
        assert val.determinar_estado_stock(1) == "⚠️ [STOCK BAJO]"

def test_determinar_estado_sin_stock_():
    """Prueba que el valor 0 exactp,debe ser STOCK BAJO"""
    assert val.determinar_estado_stock(0) =="❌ [SIN STOCK]"
# ==========================================
# 🔴 NEGATIVE PATH
# ==========================================
def test_determinar_estado_stock_negativo_lanza_error():
    """El sistema no debe permitir stock negativo (ej. -5). El patovica levanta ValueError."""
    with pytest.raises(ValueError):
        val.determinar_estado_stock(-5)
# --------------------------------------------------------
# TEST 1: El Happy Path con Enter (usando return_value)
# --------------------------------------------------------
@patch('app.validador.cantidad_usuario')
@patch('builtins.input')
def test_updatear_productos_mantiene_valores_con_enter(mock_input, mock_cantidad):
    mock_input.return_value = ""
    mock_cantidad.return_value = ""
    nombre_n, cantidad_n, estado_n = val.updatear_productos("A", 5, "✅ [STOCK OK]")
    assert nombre_n == ""
    assert cantidad_n == ""
    assert estado_n == ""

# --------------------------------------------------------
# TEST 2: Modificando datos (usando side_effect)
# --------------------------------------------------------
@patch('app.validador.cantidad_usuario')
@patch('builtins.input')
def test_updatear_productos_modifica_con_valores_nuevos( mock_input, mock_cantidad):
    """Verifica que si el usuario escribe datos, la función los devuelva correctamente"""
    mock_input.side_effect = ["reemplazo de A", "⚠️ [STOCK BAJO]"]
    mock_cantidad.return_value = 2
    nombre_n, cantidad_n, estado_n = val.updatear_productos("A", 5, "✅ [STOCK OK]")
    assert nombre_n == "reemplazo de A"
    assert cantidad_n == 2
    assert estado_n == "⚠️ [STOCK BAJO]"
