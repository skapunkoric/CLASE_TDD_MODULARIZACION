import pytest
import sqlite3
import bd.database as db

@pytest.fixture(autouse=True)
def preparar_base_de_datos_en_memoria():
    # 1. ⚡ EL SALVAVIDAS: Abrimos una conexión "maestra" y NO la cerramos.
    # Esto mantiene la base de datos viva en la RAM.
    conexion_maestra = sqlite3.connect("file::memory:?cache=shared", uri=True)
    
    # 2. Hacemos el truco para que las funciones usen la misma RAM
    db.conectar = lambda: sqlite3.connect("file::memory:?cache=shared", uri=True)
    
    # 3. Ahora sí, creamos y limpiamos (como la maestra sigue abierta, no se borra nada)
    db.crear_base_datos()
    db.limpiar_historial_viejo()
    
    # 4. yield pausa esta función acá y le dice a pytest: "¡Corré los tests!"
    yield 
    
    # 5. Cuando los tests terminan, cerramos la maestra y la memoria se libera sola
    conexion_maestra.close()
def test_ingreso_y_consultas_db():
    db.ingreso_gasto_bd(100)
    db.ingreso_gasto_bd(50)
    
    metricas = db.consultas_bd()
    
    assert metricas["total"] == 150
    assert metricas["cantidad"] == 2
    assert metricas["promedio"] == 75.0

def test_la_tabla_gasto_se_crea_correctamente():
    "test que verifica la creacion de la db correctamente"
    db.crear_base_datos()    
    conexion = db.conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= gasto")
    table_encontrada = cursor.fetchone()
    conexion.close()
    assert table_encontrada is not None    