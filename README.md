# 🛠️ Backend Modular con CRUD de Stock & Suite TDD

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-Pytest%20%7C%20Unittest-green?style=for-the-badge&logo=pytest&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-SRP%20Modular-orange?style=for-the-badge)

Repositorio enfocado en la refactorización de un backend de gestión de stock en Python, implementando arquitectura modular bajo el **Principio de Responsabilidad Única (SRP)** y desarrollo guiado por pruebas (**TDD**).

---

## 🏗️ Arquitectura del Proyecto

El código está desacoplado para asegurar mantenibilidad, escalabilidad y aislamiento en los testings:

* **Módulo de Validaciones (`app/validador.py`):** "Patovicas" encargados del saneamiento y control estricto de inputs de usuario.
* **Módulo de Interfaz (`app/del_front.py`):** Capa de presentación por consola formateada visualmente.
* **Módulo de Persistencia (`bd/`):** Gestión de operaciones CRUD en base de datos SQLite.
* **Módulo de Pruebas (`tests/`):** Cobertura TDD evaluando *Happy Paths*, *Edge Cases* y *Negative Paths* usando bases de datos efímeras aisladas (`tmp_path` / `tempfile`).

```text
CLASE_TDD_MODULARIZACION/
├── app/
│   ├── del_front.py        # Capa de presentación e interfaz
│   └── validador.py        # Validaciones de entrada (SRP)
├── bd/                      # Logica e integración con SQLite
├── ejercicio_02_validador/  # Módulos previos de validación
├── ejercicio_07_stock/      # Núcleo del CRUD de control de inventario
└── roadmap_persistencia.md  # Hoja de ruta y arquitectura
## 🚀 Resumen de Ejercicios y Arquitectura Aplicada

### Ejercicio 02: Validador de Gastos
* **Desarrollo Guiado por Pruebas (TDD):** Implementación de validaciones robustas para el ingreso de datos del usuario.
* **Manejo de Excepciones:** Cobertura de *Negative Paths* para evitar que ingresos inválidos rompan la ejecución del programa.
* **Mocking:** Uso de la librería `unittest.mock` para simular entradas de consola (`input`) y testear el comportamiento de las funciones de forma automatizada y aislada.

### Ejercicio 07: Sistema de Gestión de Inventario (Stock)
* **Arquitectura Modular:** Separación clara de responsabilidades entre la lógica de negocio (`validador.py`), la interfaz de usuario y la persistencia de datos (`database.py`).
* **Migración de Testing (Unittest -> Pytest):** Refactorización completa de la suite de pruebas hacia la sintaxis nativa de `pytest` para un código más limpio y escalable.
* **Bases de Datos Temporales en Memoria:** Implementación de *Fixtures* en Pytest con `autouse=True` y `yield` (Setup/Teardown) para levantar una base de datos SQLite en memoria RAM (`file::memory:?cache=shared`). Esto permite pruebas de integración 100% seguras, rápidas y sin alterar la base de datos de producción.
* **Magia Negra (Mocks Avanzados):** Uso intensivo de dobles de riesgo (`@patch`) aplicando `return_value` y `side_effect` para testear el flujo completo de actualización de productos, simulando múltiples interacciones del usuario en consola sin detener la ejecución de los tests.
* **Cobertura Completa:** Testing exhaustivo abarcando *Happy Paths*, *Edge Cases* (Límites de stock) y *Negative Paths* (Validación contra stock negativo mediante `ValueError`).
