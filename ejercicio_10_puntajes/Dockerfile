# 1. Traemos la versión oficial de Python (ligera)
FROM python:3.10-slim
# 2. Le decimos a Docker: "Todo lo que hagamos ahora, hacelo adentro de esta carpeta en el contenedor"
WORKDIR /app
# 3. Instalamos pytest para poder correr tus tests (como es una imagen limpia, no lo tiene)
RUN pip install pytest
# 4. Copiamos TODOS los archivos de tu compu (el código y los tests) a la carpeta /app del contenedor
COPY . /app
# 5. El comando por defecto que se va a ejecutar cuando prendas el contenedor
CMD ["python", "-m", "pytest"]
