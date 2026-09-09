import unittest
import sqlite3
import os
import bd.database as db

class TestBaseDeDatos(unittest.TestCase):
    def setUp(self):
        "crea la conexion para la bd en memoria "
        self.conexion_maestra =sqlite3.connect("file::memory:?cache=shared", uri=True)
        db.conectar = lambda: sqlite3.connect("file::memory:?cache=shared", uri=True)
        db.crear_tabla()
        db.cargar_datos()



    def tearDown(self):
        "cierra la conexion maestra"
        self.conexion_maestra.close()

    def test_la_tabla_puntajes_se_crea_correctamente_y_no_en_sqlmaster_negative_path(self):
        "verifica que la bd se cree"
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name='ranking'")
        tabla_encontrada = cursor.fetchone()
        conexion.close()
        self.assertIsNotNone(tabla_encontrada,"¡Error! La tabla 'puntajes' no fue creada.")

    def test_la_tabla_puntajes_se_crea_correctamente_y_happy_path(self):
        "verifica que se cree una tabla al menos"
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM ranking WHERE id_jugador = 1")
        tabla_encontrada = cursor.fetchone()
        conexion.close()
        self.assertEqual(tabla_encontrada[0], 1, "el jugador con id 1 no existe en la base de datos")


    def test_cargar_datos_no_duplica_registros_si_se_ejecuta_dos_veces(self):
        "Verifica que el escudo anti-clones funcione y no duplique la carga"
        db.cargar_datos()
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM ranking")
        total_cargados = cursor.fetchone()[0]
        conexion.close()
        self.assertEqual(total_cargados, 7, "¡Alerta! El escudo falló y la base duplicó los datos")


    def test_la_tabla_rechaza_jugadores_sin_nombre_o_sin_puntaje_negative_path(self):
        "Verifica que la restricción NOT NULL de la tabla esté funcionando"
        conexion = db.conectar()
        cursor = conexion.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO ranking (nombre_jugador, puntaje) VALUES (NULL, 500)")
        conexion.close()

    def test_crear_tabla_no_falla_si_se_ejecuta_cuando_ya_existe(self):
        "Verifica que el IF NOT EXISTS proteja contra errores de recreación"
        try:
            db.crear_tabla()
        except Exception as e:
            self.fail(f"Error! crear_tabla() falló al ejecutarse dos veces. Detalle: {e}")

    def test_obtener_jugadores_top_min_trae_a_gabriela_(self):
        "Verifica que el puntaje mínimo de la tabla sea 100"
        resultado = db.obtener_jugadores_top_min()
        self.assertEqual(resultado[0][0],"Gabriela")
        self.assertEqual(resultado[0][1], 100)

    def test_obtener_promedio_general_es_700(self):
        "Verifica que el calculo del prom. gral sea correcto"
        resulta_promedio = db.obtener_promedio_general()
        self.assertEqual(resulta_promedio[0], 700)

    def test_obtener_reporte_de_mas_800_top_devuelve_tres_jugadores(self):
        "Verifica que solo 3 jugadores superen los 800 puntos"
        resultado_top_800 = db.obtener_reporte_de_mas_800_top()
        self.assertEqual(len(resultado_top_800), 3)

    def test_obtener_cantidades_top_de_empates_devuelve_dos(self):
        "verifica que cuente correctamente a los 2 jugadores con 1200 puntos"    
        resultado_empates = db.obtener_cantidades_empates_top()
        self.assertEqual(resultado_empates[0][0], 2)




if __name__ == "__main__":
    unittest.main()