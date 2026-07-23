import pytest
import sqlite3
import bd.database as db

# 1. EL FIXTURE: Este es el que mantiene la base de datos viva
@pytest.fixture(autouse=True)
def preparar_base_de_datos_en_memoria():
    # Abrimos la conexión maestra y NO la cerramos acá
    conexion_maestra = sqlite3.connect("file::memory:?cache=shared", uri=True)
    db.conectar = lambda: sqlite3.connect("file::memory:?cache=shared", uri=True)
    # create and clean 
    db.crear_base_datos()
    db.limpiar_historial_viejo()
    # Pausamos y dejamos que corran todos los tests
    yield 
    # Cuando terminan los tests, se cierra y se limpia la RAM
    conexion_maestra.close()

# 2. EL TEST DE LA TABLA: Se ejecuta usando la memoria que preparó el fixture
def test_la_tabla_gasto_se_crea_correctamente():
    """"""
    conexion = db.conectar()
    cursor = conexion.cursor()
    # Consultamos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gasto'")
    tabla_encontrada = cursor.fetchone()
    # Cerramos esta conexión local (no pasa nada porque la maestra sigue abierta)
    conexion.close()
    # Verificamos
    assert tabla_encontrada is not None

# 3. EL TEST DE LAS MÉTRICAS
def test_ingreso_y_consultas_db():
    """ """
    db.ingreso_gasto_bd(100)
    db.ingreso_gasto_bd(50)
    metricas = db.consultas_bd()
    
    assert metricas["total"] == 150
    assert metricas["cantidad"] == 2