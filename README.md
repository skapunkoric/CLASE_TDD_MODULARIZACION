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
