Veo
varios
problemas
críticos
en
tu
código
que
impiden
que
funcione
correctamente.Aquí
está
el
análisis
y
la
solución:

---

## **Problemas principales:**

### 1. **Conexión a base de datos incorrecta**
```python


def conectar():
    sqlite3.connect(":memory:")  # Esto crea una BD en RAM que se pierde
    return sqlite3.connect()  # Esto crea otra conexión sin nombre


```
** Solución **: Define
una
ruta
fija
para
tu
archivo
`.db
`.

### 2. **Error de sintaxis en `CREATE TABLE`**
```python
CREATE
TABLE
IF
NOT
EXISTS
ahorro(
    id_meta
INTEGER
PRIMARY
KEY
AUTOINCREMENT
NULL,  # AUTOINCREMENT no puede ser NULL
ahorro
INTEGER
NOT
NUL)  # FALTA coma entre tablas
```
** Solución **: Separar
en
dos
sentencias
y
corregir
tipos.

### 3. **Variables no definidas**
- `dinero_a_ingresar`
no
está
definida
en
`ingreso_dinero()`
- `ahorro_ingresado`
no
es
accesible
globalmente

### 4. **Lógica inconsistente**
- `ingreso_ahorro()`
devuelve
un
valor
pero
no
se
usa
en
`ingreso_dinero()`
- No
hay
estado
global para
almacenar
el
objetivo
de
ahorro

---

## **Código corregido y mejorado:**

```python
import re
import os
import sqlite3
from datetime import datetime
from tabulate import tabulate

# ==================== CONFIGURACIÓN ====================
DB_PATH = "ahorro.db"  # Ruta fija para la base de datos

# ==================== MENSAJES ====================
MENSAJE_INVALIDO = " | ESTADO: ❌ Ingreso no válido"
MENSAJE_OBJETIVO_LOGRO = "✅ OBJETIVO ALCANZADO"
MENSAJE_OBJETIVO_PENDIENTE = "⏳ AHORRO PENDIENTE"


# ==================== GESTIÓN DE BASE DE DATOS ====================
class AhorroDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.crear_tablas()

    def conectar(self):
        """Conexión segura a la base de datos"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error conectando a BD: {e}")
            return None

    def crear_tablas(self):
        """Crea tablas si no existen"""
        conexion = self.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS meta_ahorro
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               monto_total
                               INTEGER
                               NOT
                               NULL,
                               fecha_creacion
                               DATETIME
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS registro_ahorro
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               monto
                               INTEGER
                               NOT
                               NULL,
                               fecha
                               DATETIME
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               tipo
                               TEXT
                               CHECK (
                               tipo
                               IN
                           (
                               'ingreso',
                               'retiro'
                           ))
                               )
                           """)
            conexion.commit()
            print("✅ Base de datos inicializada correctamente")
            return True
        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")
            return False
        finally:
            conexion.close()

    def guardar_meta(self, monto):
        """Guarda el objetivo de ahorro"""
        conexion = self.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            # Primero borramos meta anterior si existe
            cursor.execute("DELETE FROM meta_ahorro")
            cursor.execute("INSERT INTO meta_ahorro (monto_total) VALUES (?)", (monto,))
            conexion.commit()
            print(f"✅ Meta establecida: ${monto:,}")
            return True
        except sqlite3.Error as e:
            print(f"Error guardando meta: {e}")
            return False
        finally:
            conexion.close()

    def registrar_movimiento(self, monto, tipo='ingreso'):
        """Registra un movimiento (ingreso o retiro)"""
        conexion = self.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO registro_ahorro (monto, tipo) VALUES (?, ?)",
                (monto, tipo)
            )
            conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error registrando movimiento: {e}")
            return False
        finally:
            conexion.close()

    def obtener_meta_actual(self):
        """Obtiene el objetivo de ahorro actual"""
        conexion = self.conectar()
        if not conexion:
            return 0

        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT monto_total FROM meta_ahorro ORDER BY id DESC LIMIT 1")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except sqlite3.Error as e:
            print(f"Error obteniendo meta: {e}")
            return 0
        finally:
            conexion.close()

    def obtener_total_ahorrado(self):
        """Calcula el total ahorrado (ingresos - retiros)"""
        conexion = self.conectar()
        if not conexion:
            return 0

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                           SELECT SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE -monto END)
                           FROM registro_ahorro
                           """)
            resultado = cursor.fetchone()
            return resultado[0] or 0
        except sqlite3.Error as e:
            print(f"Error calculando total: {e}")
            return 0
        finally:
            conexion.close()

    def obtener_historial(self):
        """Obtiene el historial de movimientos"""
        conexion = self.conectar()
        if not conexion:
            return []

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                           SELECT fecha, monto, tipo
                           FROM registro_ahorro
                           ORDER BY fecha DESC
                           """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo historial: {e}")
            return []
        finally:
            conexion.close()


# ==================== VALIDACIÓN ====================
def validar_monto(valor):
    """Valida que el monto sea un número entero positivo"""
    if not re.match(r"^[1-9][0-9]*$", valor):
        return None
    return int(valor)


# ==================== INTERFAZ DE USUARIO ====================
class AplicacionAhorro:
    def __init__(self):
        self.db = AhorroDB()
        self.meta_actual = 0

    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("=== SISTEMA DE CONTROL DE AHORRO ===")
        print("=" * 50)
        print("\nMenú de opciones:")
        print("1. Establecer meta de ahorro")
        print("2. Registrar ingreso")
        print("3. Registrar retiro")
        print("4. Ver estado actual")
        print("5. Ver historial")
        print("6. Salir")
        print()

    def establecer_meta(self):
        """Establece un nuevo objetivo de ahorro"""
        monto = input("Ingresa la meta de ahorro: $")
        monto_validado = validar_monto(monto)

        if monto_validado is None:
            print(MENSAJE_INVALIDO)
            return

        if self.db.guardar_meta(monto_validado):
            self.meta_actual = monto_validado
            self.mostrar_estado()

    def registrar_movimiento(self, tipo):
        """Registra un movimiento de dinero"""
        monto = input(f"Ingresa el monto a {tipo}: $")
        monto_validado = validar_monto(monto)

        if monto_validado is None:
            print(MENSAJE_INVALIDO)
            return

        if self.db.registrar_movimiento(monto_validado, tipo):
            print(f"✅ {tipo.capitalize()} de ${monto_validado:,} registrado")
            self.mostrar_estado()

    def mostrar_estado(self):
        """Muestra el estado actual del ahorro"""
        meta = self.db.obtener_meta_actual()
        ahorrado = self.db.obtener_total_ahorrado()
        faltante = meta - ahorrado

        print("\n" + "=" * 50)
        print("=== ESTADO ACTUAL ===")
        print("=" * 50)
        print(f"Meta de ahorro: ${meta:,}")
        print(f"Ahorrado actual: ${ahorrado:,}")

        if ahorrado >= meta:
            print(MENSAJE_OBJETIVO_LOGRO)
        else:
            print(f"Faltante: ${faltante:,}")
            print(MENSAJE_OBJETIVO_PENDIENTE)
        print()

    def mostrar_historial(self):
        """Muestra el historial de movimientos"""
        historial = self.db.obtener_historial()

        if not historial:
            print("No hay movimientos registrados aún")
            return

        print("\n" + "=" * 50)
        print("=== HISTORIAL DE MOVIMIENTOS ===")
        print("=" * 50)

        # Formatear datos para mostrar
        tabla = []
        for fecha, monto, tipo in historial:
            fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
            tabla.append([
                fecha_formateada.strftime("%d/%m/%Y %H:%M"),
                f"${monto:,}",
                "Ingreso" if tipo == "ingreso" else "Retiro"
            ])

        print(tabulate(tabla, headers=["Fecha", "Monto", "Tipo"], tablefmt="grid"))
        print()

    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        while True:
            self.mostrar_menu()
            opcion = input("Selecciona una opción (1-6): ").strip()

            if opcion == "1":
                self.establecer_meta()
            elif opcion == "2":
                self.registrar_movimiento("ingreso")
            elif opcion == "3":
                self.registrar_movimiento("retiro")
            elif opcion == "4":
                self.mostrar_estado()
            elif opcion == "5":
                self.mostrar_historial()
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")

            input("Presiona Enter para continuar...")


# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    app = AplicacionAhorro()
    app.ejecutar()
""""
## **Características principales del código corregido:**

### ✅ **Base de datos persistente**
- Usa
archivo
`ahorro.db`
en
lugar
de
memoria
RAM
- Tablas
bien
estructuradas
con
relaciones
claras

### ✅ **Gestión completa de ahorro**
- ** Meta
de
ahorro **: Objetivo
total
a
alcanzar
- ** Ingresos / Retiros **: Movimientos
que
afectan
el
saldo
- ** Cálculo
automático **: Saldo = Ingresos - Retiros

### ✅ **Validación robusta**
- Solo
acepta
números
enteros
positivos
- Manejo
de
errores
de
base
de
datos

### ✅ **Interfaz amigable**
- Menú
interactivo
- Tablas
formateadas
con
`tabulate`
- Mensajes
claros
de
estado

### ✅ **Funcionalidades incluidas**
1.
Establecer
meta
de
ahorro
2.
Registrar
ingresos
3.
Registrar
retiros
4.
Ver
estado
actual(meta
vs
ahorrado)
5.
Ver
historial
completo
de
movimientos
6.
Detectar
cuando
se
alcanza
la
meta

---

## **Cómo usarlo:**

1. ** Ejecuta
el
script **:
```bash
python
ahorro.py
```

2. ** Primeros
pasos **:
- Opción
1: Establece
tu
meta
de
ahorro(ej: 10000)
- Opción
2: Registra
ingresos
- Opción
4: Verifica
tu
progreso

3. ** Cuando
alcances
la
meta **:
```
✅ OBJETIVO
ALCANZADO
```

---

## **Mejoras futuras posibles:**

1. ** Persistencia
en
la
nube ** (Firebase, AWS DynamoDB)
2. ** Gráficas
de
progreso ** (matplotlib)
3. ** Categorías
de
gastos ** (comida, transporte, etc.)
4. ** Exportar
a
CSV / Excel **
5. ** Notificaciones ** (Telegram, email)
6. ** Multi - moneda ** (USD, EUR, etc.)

¿Te
gustaría
que
añada
alguna
de
estas
funcionalidades
o
prefieres
ajustar
algo
específico?