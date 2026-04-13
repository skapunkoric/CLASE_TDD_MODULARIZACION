
import pytest
import  builtins

# test_nombre de app.py
def test_nombre_simulado(monkeypatch):
    repuestas_datos =iter(["raul","tolentino","47","babul@gmail..com"])
    monkeypatch.setattr(builtins, "input", lambda _: next(repuestas_datos))

    import app

    assert app.nombre == "raul"



def test_datos_en_lista_nombre_apellido_edad_email_simulado(monkeypatch):
    import importlib
    import app
    repuestas_datos =iter(["raul","tolentino",47,"babul@gmail..com"])
    monkeypatch.setattr(builtins, "input", lambda _: next(repuestas_datos))
    importlib.reload(app)

    assert app.nombre == "raul"
    assert app.apellido == "tolentino"
    assert app.edad == 47
    assert app.correo == "babul@gmail..com"