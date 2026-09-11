# 🛠️ Backend Modular con CRUD de Stock & Suite TDD

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-Pytest%20%7C%20Unittest-green?style=for-the-badge&logo=pytest&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-SRP%20Modular-orange?style=for-the-badge)

Repositorio enfocado en la refactorización de un backend de gestión de stock en Python, implementando arquitectura modular bajo el **Principio de Responsabilidad Única (SRP)** y desarrollo guiado por pruebas (**TDD**).

---

## 🏗️ Arquitectura del Proyecto

El código está desacoplado para asegurar mantenibilidad, escalabilidad y aislamiento en los testings:

- **Módulo de Validaciones (`app/validador.py`):** "Patovicas" encargados del saneamiento y control estricto de inputs de usuario.
- **Módulo de Interfaz (`app/del_front.py`):** Capa de presentación por consola formateada visualmente.
- **Módulo de Persistencia (`bd/`):** Gestión de operaciones CRUD en base de datos SQLite.
- **Módulo de Pruebas (`tests/`):** Cobertura TDD evaluando _Happy Paths_, _Edge Cases_ y _Negative Paths_ usando bases de datos efímeras aisladas (`tmp_path` / `tempfile`).

Estructura de carpetas:
CLASE_TDD_MODULARIZACION/
├── .github/workflows/ # Pipelines de Integración Continua (CI)
├── app/
│ ├── del_front.py # Capa de presentación e interfaz
│ └── validador.py # Validaciones de entrada (SRP)
├── bd/ # Logica e integración con SQLite
├── ejercicio_02_validador/ # Módulos previos de validación (Dockerizado)
├── ejercicio_07_stock/ # Núcleo del CRUD de inventario (Dockerizado)
├── ejercicio_10_puntajes/ # Análisis estadístico de arrays (Dockerizado)
└── roadmap_persistencia.md # Hoja de ruta y arquitectura

---

## 🚀 Resumen de Ejercicios y Arquitectura Aplicada

### Ejercicio 02: Validador de Gastos

- **Desarrollo Guiado por Pruebas (TDD):** Implementación de validaciones robustas para el ingreso de datos del usuario.
- **Manejo de Excepciones:** Cobertura de _Negative Paths_ para evitar que ingresos inválidos rompan la ejecución del programa.
- **Mocking:** Uso de la librería `unittest.mock` para simular entradas de consola (`input`) y testear el comportamiento automatizado.

### Ejercicio 07: Sistema de Gestión de Inventario (Stock)

- **Arquitectura Modular:** Separación clara de responsabilidades entre lógica de negocio, interfaz de usuario y persistencia.
- **Migración de Testing (Unittest -> Pytest):** Refactorización de la suite hacia la sintaxis nativa de `pytest`.
- **Bases de Datos Temporales en Memoria:** Fixtures en Pytest con `autouse=True` y `yield` para levantar SQLite en RAM (`file::memory:?cache=shared`). Pruebas de integración 100% seguras y rápidas.
- **Magia Negra (Mocks Avanzados):** Uso de dobles de riesgo (`@patch`) con `return_value` y `side_effect` simulando múltiples interacciones del usuario.
- **Cobertura Completa:** Testing de _Happy Paths_, _Edge Cases_ y _Negative Paths_ (Validación contra stock negativo).

### Ejercicio 10: Análisis Estadístico de Puntajes

- **Procesamiento de Datos:** Análisis de listas de puntajes para calcular valores máximos, mínimos y promedios, aplicando filtros de validación.
- **Lógica de Acumulación:** Algoritmos para contar y gestionar puntajes duplicados aislando los picos máximos.

---

## 🤖 Integración Continua (CI/CD)

El proyecto cuenta con un pipeline automatizado mediante **GitHub Actions**. Ante cada _Push_ a la rama principal, un orquestador en la nube despliega un entorno virtual, instala las dependencias y ejecuta la suite completa de `pytest` para garantizar la integridad del código.

---

## 🐳 Contenedores y Entornos Aislados (Docker)

Para garantizar que las aplicaciones se ejecuten de manera idéntica en cualquier sistema sin conflictos de dependencias, los ejercicios principales corren en **contenedores Docker independientes**.

- **Aislamiento:** Implementación de `Dockerfile` individuales basados en imágenes ligeras (`python:3.10-slim`).
- **Optimización:** Uso de `.dockerignore` para excluir archivos de testing conflictivos y mantener los contenedores rápidos y limpios.

### 🏃‍♂️ Cómo ejecutar los contenedores localmente

1. Navegar al directorio del ejercicio (ej. cd ejercicio_07_stock).
2. Construir la imagen: docker build -t app-stock .
3. Ejecutar los tests dentro del contenedor: docker run app-stock
