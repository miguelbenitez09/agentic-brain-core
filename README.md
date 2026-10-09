# 🧠 Agentic Brain Core

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Security](https://img.shields.io/badge/Security-RBAC_&_SHA--256-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-Event_Sourcing_JSONL-orange.svg)
![CLI](https://img.shields.io/badge/CLI-Command_Line_Interface-blueviolet.svg)
[![Autor](https://img.shields.io/badge/Autor-Ing._Miguel_Antonio_Benítez_González_(UTP)-informational.svg)](https://github.com/miguelbenitez09)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Firma Oficial:** **`Agentic Brain Core v1.0.0 • developed by Miguel Benitez`**  
> **Framework ligero y desacoplado para orquestación de agentes locales, gestión de memoria episódica inmutable (JSONL Event Sourcing), verificación criptográfica de system prompts (souls), control de acceso a herramientas y seguimiento de brechas técnicas.**

---

## 👨‍💻 Autor

**Ing. Miguel Antonio Benítez González** (Universidad Tecnológica de Panamá - UTP)
- 🎓 **Título:** Ingeniero en Sistemas y Computación
- 📜 **Idoneidad Profesional:** Junta Técnica de Ingeniería y Arquitectura de Panamá (JTIA)
- 📧 **Email:** mbenitezg01@gmail.com
- 💻 **GitHub:** [miguelbenitez09](https://github.com/miguelbenitez09?tab=repositories)
- 💼 **LinkedIn:** [Miguel Antonio Benítez González](https://www.linkedin.com/in/miguel-antonio-ben%C3%ADtez-gonz%C3%A1lez-457816247/)

---

## 📋 Tabla de Contenidos

1. [Visión General del Framework](#-visión-general-del-framework)
2. [Principios de Ingeniería de Software (UTP)](#-principios-de-ingeniería-de-software-utp)
3. [Arquitectura Modular de Componentes](#-arquitectura-modular-de-componentes)
4. [Módulos Principales](#-módulos-principales)
   - [Lector de Contexto y Documentos](#1-lector-de-contexto-y-documentos-srcreaders)
   - [Memoria Episódica Inmutable](#2-memoria-episódica-inmutable-srcmemory)
   - [Gestor de Identidades y Souls](#3-gestor-de-identidades-y-souls-srcsouls)
   - [Frontera de Seguridad y Secretos](#4-frontera-de-seguridad-y-secretos-srcsecurity)
   - [Cola de Tareas y Seguimiento de Brechas](#5-cola-de-tareas-y-seguimiento-de-brechas-srcorchestration)
5. [Interfaz de Línea de Comandos (CLI)](#-interfaz-de-línea-de-comandos-cli)
6. [Instalación y Pruebas Unitarias](#-instalación-y-pruebas-unitarias)
7. [Licencia](#-licencia)

---

## 📖 Visión General del Framework

Al diseñar sistemas basados en inteligencia artificial agentic (múltiples agentes colaborativos resolviendo tareas de ingeniería), surgen tres problemas arquitectónicos críticos:
1. **Pérdida y desbordamiento de contexto:** Los agentes requieren acceder a documentación local estructurada (Markdown, JSON, YAML) sin saturar la ventana de contexto del LLM.
2. **Falta de trazabilidad y auditoría:** Se necesita un registro inmutable e incorruptible de lo que pensó e hizo cada agente en cada paso.
3. **Riesgo de seguridad en ejecución de herramientas:** La ejecución autónoma de comandos del shell o llamadas a APIs externas requiere barreras estrictas de permisos y enmascaramiento automático de credenciales.

`agentic-brain-core` fue diseñado e implementado desde cero para proporcionar una base local, sin dependencias pesadas de nube ni telemetría externa, inspirada en los conceptos de *Second Brain* (Obsidian) y arquitecturas dirigidas por eventos (Event Sourcing).

---

## 📐 Principios de Ingeniería de Software (UTP)

Como Ingeniero en Sistemas y Computación egresado de la Universidad Tecnológica de Panamá, este framework implementa rigurosamente:
- **Desacoplamiento Estricto (Separación de Preocupaciones):** La memoria, la seguridad y la lectura de documentos son subsistemas autónomos testeables de forma independiente.
- **Inmutabilidad y Criptografía:** Cada evento en la memoria se almacena en registros append-only acompañados de su huella digital criptográfica **SHA-256**.
- **Seguridad por Diseño (Principle of Least Privilege):** Ningún agente tiene permisos de ejecución de comandos por defecto. El acceso se confiere explícitamente mediante capacidades RBAC.

---

## 🏗️ Arquitectura Modular de Componentes

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGENTIC BRAIN CORE                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌──────────────────────┐               ┌────────────────────────┐    │
│   │   Document Readers   │               │   Soul & Prompt Mgr    │    │
│   │   - Markdown Frontm. │               │   - YAML Identity      │    │
│   │   - JSON / YAML / TXT│               │   - SHA-256 Digest     │    │
│   └──────────┬───────────┘               └───────────┬────────────┘    │
│              │                                       │                 │
│              ▼                                       ▼                 │
│   ┌───────────────────────────────────────────────────────────────┐    │
│   │                Orchestrator & Agent Dispatcher                │    │
│   │                - Task Queue (Priority 1 to 5)                 │    │
│   │                - Gap Tracking & State Machine                 │    │
│   └──────────────────────┬────────────────────────────────────────┘    │
│                          │                                             │
│         ┌────────────────┴───────────────┐                             │
│         ▼                                ▼                             │
│   ┌───────────────────────────┐    ┌──────────────────────────────┐    │
│   │    Security Boundary      │    │   Session Episodic Memory    │    │
│   │    - Capability Matrix    │    │   - Append-Only JSONL Log    │    │
│   │    - Command Blacklist    │    │   - SHA-256 Event Digests    │    │
│   │    - Secrets Masker       │    │   - Context Window Slicing   │    │
│   └───────────────────────────┘    └──────────────────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Módulos Principales

### 1. Lector de Contexto y Documentos (`src/readers/`)
- Soporte para Markdown con extracción de metadatos YAML frontmatter.
- Resumen automático de encabezados, conteo de líneas y extracción de bloques de código por lenguaje.
- Escaneo recursivo de repositorios de notas y bases de conocimiento.

### 2. Memoria Episódica Inmutable (`src/memory/`)
- Almacenamiento basado en `JSONL` (*JSON Lines*) de solo adición (*append-only*).
- Cálculo en tiempo real de digest criptográfico **SHA-256** por evento.
- Soporte para rehidratación de contexto y delimitación de ventanas temporales.

### 3. Gestor de Identidades y Souls (`src/souls/`)
- Definición de agentes en archivos Markdown portables con frontmatter.
- Huella digital de integridad del system prompt para prevenir inyecciones o manipulaciones no autorizadas.
- Interpolación dinámica de parámetros en plantillas (`{{proyecto}}`, `{{usuario}}`).

### 4. Frontera de Seguridad y Secretos (`src/security/`)
- Lista blanca de capacidades granulares: `READ_DOCS`, `WRITE_DOCS`, `EXECUTE_SHELL`, `NETWORK_ACCESS`.
- Lista negra de comandos destructivos para protección de la máquina local.
- Enmascarador en memoria de claves privadas y tokens para evitar su fuga en trazas o logs.

### 5. Cola de Tareas y Seguimiento de Brechas (`src/orchestration/`)
- Cola de prioridades (1 = Crítica, 5 = Menor) para administración de gaps.
- Máquina de estados: `PENDING` ➔ `IN_PROGRESS` ➔ `COMPLETED` / `FAILED`.

---

## 💻 Interfaz de Línea de Comandos (CLI)

El framework incluye una CLI intuitiva para interactuar con el cerebro del sistema:

### Escanear Documentos
```bash
python src/cli.py scan ./examples/souls
```

### Inicializar Sesión y Registrar Eventos
```bash
python src/cli.py session create --id "sesion_auditoria_01"
python src/cli.py session summary --id "sesion_auditoria_01"
```

### Inspeccionar un Alma (Soul) y Validar Integridad
```bash
python src/cli.py soul ./examples/souls/architect.md
```

### Administrar Cola de Tareas y Brechas
```bash
python src/cli.py queue add --title "Corregir parser de tokens" --priority 1
python src/cli.py queue list
```

---

## 🚀 Instalación y Pruebas Unitarias

### Instalación
```bash
git clone https://github.com/miguelbenitez09/agentic-brain-core.git
cd agentic-brain-core

python -m venv venv
# Activar entorno
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/macOS

pip install -r requirements.txt
```

### Ejecución de Pruebas Unitarias (`pytest`)
```bash
python -m pytest tests/ -v
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT** - consulta el archivo [LICENSE](LICENSE) para más detalles.  
`Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez UTP - MIT License`
