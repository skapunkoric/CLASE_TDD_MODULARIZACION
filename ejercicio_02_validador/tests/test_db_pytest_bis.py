import pytest
import bd.database as db

# ⚡ El fixture usa 'tmp_path', una herramienta que pytest inyecta automáticamente
@pytest.fixture(autouse=True)
def preparar_base_de_datos_temporal(tmp_path):
    # 1. Creamos una ruta falsa y temporal (ej. C:\Temp\pytest\test_gastos.db)
    ruta_temporal = tmp_path / "test_gastos.db"
    
    # 2. EL NUEVO TRUCO: Pisamos la variable DB_NAME de tu archivo
    # Ahora todas tus funciones apuntarán a este archivo temporal
    db.DB_NAME = str(ruta_temporal)
    
    # 3. Creamos la base de datos en ese archivo temporal
    db.crear_base_datos()
    db.limpiar_historial_viejo()
    
    # 4. Pausamos para que corran todos los tests
    yield 
    
    # Cuando terminan los tests, pytest borra la carpeta temporal automáticamente


def test_la_tabla_gasto_se_crea_correctamente():
    """Verifica en la tabla maestra de SQLite que 'gasto' realmente exista"""
    
    # Nos conectamos a la BD temporal (que ya fue creada por el fixture)
    conexion = db.conectar()
    cursor = conexion.cursor()
    
    # Consultamos la tabla oculta de SQLite
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gasto'")
    tabla_encontrada = cursor.fetchone()
    conexion.close()
    
    # Si la tabla existe, devuelve una tupla ej: ('gasto',). Si no, devuelve None.
    assert tabla_encontrada is not None


def test_ingreso_y_consultas_db():
    """Prueba que los inserts modifiquen correctamente el dashboard"""
    
    # 1. Acción
    db.ingreso_gasto_bd(100)
    db.ingreso_gasto_bd(50)
    
    # 2. Resultado
    metricas = db.consultas_bd()
    
    # 3. Verificación
    assert metricas["total"] == 150
    assert metricas["cantidad"] == 2
    assert metricas["promedio"] == 75.0