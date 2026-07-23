import pytest
import sqlite3
# importamos tu bd
import bd.database as db

@pytest.fixture(autouse=True)
    # el fixture usa 'tmp_path' , una herramienta que pytest intecta automaticamente
def preparar_base_de_datos_temporal(tmp_path):
    # 1 creamos una ruta falsa y temporal
    ruta_temporal = tmp_path / "test_gastos.db"
    
    # 2 pisamos la variable  DB_NAME de tu archivo
    # todo apunta al archivo tempo
    db.DB_NAME = str(ruta_temporal)
    # 3 creamos la bd
    db.crear_base_datos()
    db.limpiar_historial_viejo()
    yield
    
def test_la_tabla_gasto_se_cre_correctamente():
    """Verifica en la tabla maestra de SQLite que 'gasto' realmente exista"""
    conexion = db.conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name ='gasto'")
    table_encontrada = cursor.fetchone()
    conexion.close()
    assert table_encontrada is not None

def test_ingreso_y_consultas_db():
    # 1. accion 
    db.ingreso_gasto_bd(100)
    db.ingreso_gasto_bd(50)
    # 2. resultado
    metricas = db.consultas_bd()
    # verificamos (asserts)
    assert metricas["total"] == 150
    assert metricas["cantidad"] ==  2
    assert metricas["promedio"] ==  75.0
