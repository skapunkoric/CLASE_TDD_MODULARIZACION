# 📌 ROADMAP DE PERSISTENCIA: PROYECTOS DE BASE DE DATOS

Este documento sirve como bitácora oficial y hoja de ruta para la evolución de los ejercicios clásicos de programación hacia sistemas robustos con persistencia de datos reales utilizando **Python** y **SQLite**.

---

## 📊 ESTADO DEL PROYECTO

| Ejercicio | Descripción | Estado | Enfoque Principal |
| :--- | :--- | :---: | :--- |
| **Ejercicio 7** | Control de Stock | 🟩 **COMPLETO** | CRUD, Restricción UNIQUE, Carga Inteligente. |
| **Ejercicio 9** | Simulador de Ahorro | 🟨 *Siguiente candidato* | Eliminar `while True`, Historial de Transacciones. |
| **Ejercicio 10**| Ranking de Puntajes | ⬜ *Pendiente* | Estadísticas SQL (MAX, MIN, AVG), Tabla Jugadores. |
| **Ejercicio 2** | Registro de Gastos | ⬜ *Pendiente* | Lógica Contable, Movimientos de Cuenta. |

---

## 🛠️ DETALLE DE LOS SISTEMAS

### 🟩 1. Control de Stock (Ejercicio 7) - **COMPLETO**
* **Objetivo:** Crear un inventario real donde la información no se borre al cerrar la consola.
* **Logros Arquitectónicos:**
  * Configuración de rutas absolutas para evitar bases de datos perdidas en VS Code.
  * Implementación de una función centralizada de renderizado con `tabulate`.
  * Creación de lógica dinámica para calcular el estado del stock mediante un "semáforo" visual.
  * Protección total contra registros duplicados usando el escudo `UNIQUE` de SQL e inyecciones seguras.
  * Debate de arquitectura: Enfoque iterativo en Python vs. Enfoque masivo con `CASE WHEN` en SQL.

### 🟨 2. Simulador de Ahorro / Cajero Automático (Ejercicio 9) - **PRÓXIMO PASO**
* **Objetivo de Refactorización:** Eliminar por completo el bucle infinito `while True` utilizando banderas de control (`flags`) o menús modulares más limpios.
* **Desafío Base de Datos:** * Crear una tabla `historial_ahorro` o `transacciones`.
  * Cada depósito o extracción no solo debe cambiar el saldo total, sino registrar una fila histórica con la fecha, el tipo de movimiento y el monto.

### ⬜ 3. Ranking de Puntajes (Ejercicio 10)
* **Objetivo de Refactorización:** Reemplazar las listas volátiles de Python por una tabla permanente de `jugadores` o `partidas`.
* **Desafío Base de Datos:**
  * Almacenar nombres y puntajes históricos.
  * Delegar la matemática pesada al motor SQL: utilizar funciones de agregación (`MAX()`, `MIN()`, `AVG()`) directamente en la consulta para traer el podio de ganadores al instante.

### ⬜ 4. Registro de Gastos (Ejercicio 2)
* **Objetivo de Refactorización:** Armar un clon de una billetera virtual o sistema contable básico.
* **Desafío Base de Datos:**
  * Crear una tabla `movimientos_cuenta` con columnas para `monto`, `categoria` y `tipo` (Ingreso/Egreso).
  * Practicar consultas con filtros complejos para obtener el balance neto final directamente desde la base de datos.

---

## 🚀 PRÓXIMAS ACCIONES
1. Seleccionar el Ejercicio 9 como el próximo laboratorio.
2. Diseñar la estructura de la nueva tabla de transacciones.
3. Atacar el refactor para limpiar el flujo de control del programa antes de conectarlo a la base de datos.
