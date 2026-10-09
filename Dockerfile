# Dockerfile para Agentic Brain Core v1.0.0
# Desarrollado por Ing. Miguel Antonio Benitez Gonzalez (UTP)
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente
COPY . .

# Ejecutar pruebas unitarias durante el build
RUN python -m pytest tests/ -v

# Punto de entrada por defecto: CLI
CMD ["python", "src/cli.py", "--help"]
