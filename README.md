# 🧠 Agentic Brain Core — Enterprise Multi-Agent Orchestration & Visual Studio

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![UI](https://img.shields.io/badge/UI-Visual_Drag_&_Drop_Canvas-purple.svg)
![Security](https://img.shields.io/badge/Security-Guardrails_&_SHA--256-emerald.svg)
![Architecture](https://img.shields.io/badge/Architecture-Least--Effort_Load_Balancer-orange.svg)
[![Autor](https://img.shields.io/badge/Autor-Ing._Miguel_Antonio_Benítez_González_(UTP)-informational.svg)](https://github.com/miguelbenitez09)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Firma Oficial:** **`Agentic Brain Core v1.0.0 • developed by Miguel Benítez`**  
> **Plataforma Integral de Orquestación Multi-Agente, Balanceo Dinámico de Esfuerzo, Guardrails de Seguridad de Entrada/Salida, Memoria Jerárquica Inmutable (JSONL Event Sourcing) e Interfaz Visual Drag & Drop para diseño de enjambres en tiempo real.**

---

## 👨‍💻 Autor

**Ing. Miguel Antonio Benítez González** (Universidad Tecnológica de Panamá - UTP)
- 🎓 **Título:** Ingeniero en Sistemas y Computación
- 📜 **Idoneidad Profesional:** Junta Técnica de Ingeniería y Arquitectura de Panamá (JTIA)
- 📧 **Email:** mbenitezg01@gmail.com
- 💻 **GitHub:** [miguelbenitez09](https://github.com/miguelbenitez09?tab=repositories)
- 💼 **LinkedIn:** [Miguel Antonio Benítez González](https://www.linkedin.com/in/miguel-antonio-ben%C3%ADtez-gonz%C3%A1lez-457816247/)

---

## 🎯 ¿Por qué este Proyecto Demuestra Madurez de Ingeniería?

El despliegue de sistemas multiagente en entornos de producción empresarial frecuentemente falla debido a tres causas críticas:
1. **Falta de Gobernanza y Seguridad:** Los agentes ejecutan comandos sin control, filtran secretos o son vulnerables a ataques de *Prompt Injection*.
2. **Distribución Ingenua de Carga:** Asignar tareas mediante *Round-Robin* colapsa agentes asignados a tareas complejas mientras otros quedan ociosos.
3. **Caja Negra sin Trazabilidad:** Dificultad para auditar el razonamiento (*Chain-of-Thought*) y verificar la inmutabilidad de los mensajes.

`Agentic Brain Core` resuelve estos desafíos aplicando **estrategias rigurosas de desarrollo de software y sistemas distribuidos aprendidas en la carrera de Ingeniería en Sistemas y Computación de la UTP**:
- **Protocolo Formal de Mensajería:** Mensajes sellados con firma criptográfica **SHA-256** bajo un envoltorio estandarizado (`MessageEnvelope`).
- **Motor de Guardrails:** Detección de inyección de prompts, anonimización de PII (correos, teléfonos, cédulas) y bloqueo de fugas de credenciales (`ghp_`, API keys).
- **Balanceador de Esfuerzo (Least-Effort Routing):** Clasificador heurístico de tareas que estima puntos de complejidad (1 a 10 pts) y distribuye la carga equilibrando la capacidad máxima del clúster.
- **Interfaz Drag & Drop de Alta Productividad:** Estudio visual donde desarrolladores y arquitectos pueden arrastrar nodos, conectar flujos, redactar prompts y despachar tareas con telemetría en vivo.

---

## 🏗️ Arquitectura de la Plataforma

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 STUDIO VISUAL DRAG & DROP                               │
│                (Canvas Interactivo • Conectores SVG • Kanban • Inspector)               │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │ REST API / WebSocket
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              AGENT SWARM SUPERVISOR CORE                                │
│                                                                                         │
│  ┌─────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────┐  │
│  │   Guardrails Engine     │   │     Task Classifier      │   │  Load Balancer       │  │
│  │   - Anti-Injection      │   │     - Dominio Tecnológico│   │  - Least-Effort      │  │
│  │   - PII Scrubbing       │   │     - Puntos de Esfuerzo │   │  - Rebalanceo Dinám. │  │
│  │   - Secret Masking      │   │     (1 a 10 puntos)      │   │  - Capacidad Clúster │  │
│  └────────────┬────────────┘   └─────────────┬────────────┘   └──────────┬───────────┘  │
│               │                              │                           │              │
│               └──────────────────────┬───────┴───────────────────────────┘              │
│                                      ▼                                                  │
│                    ┌──────────────────────────────────┐                                 │
│                    │     Despachador de Agentes       │                                 │
│                    └─────────────────┬────────────────┘                                 │
│                                      │                                                  │
│         ┌────────────────────────────┼────────────────────────────┐                     │
│         ▼                            ▼                            ▼                     │
│  ┌──────────────┐             ┌──────────────┐             ┌──────────────┐             │
│  │ Architect    │             │ QA & Sec     │             │ Backend Dev  │             │
│  │ Agent (UTP)  │             │ Auditor      │             │ Specialist   │             │
│  └──────┬───────┘             └──────┬───────┘             └──────┬───────┘             │
│         │                            │                            │                     │
│         └────────────────────────────┼────────────────────────────┘                     │
│                                      ▼                                                  │
│                    ┌──────────────────────────────────┐                                 │
│                    │    Memoria Jerárquica Unificada  │                                 │
│                    │    - Working Memory (Sliding)    │                                 │
│                    │    - Episodic (JSONL + SHA-256)  │                                 │
│                    │    - Semantic (Local Knowledge)  │                                 │
│                    └──────────────────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ Experiencia de Usuario: Drag & Drop Studio

El repositorio incluye una aplicación web completa desarrollada en HTML5, CSS moderno y JavaScript puro (sin frameworks pesados, 60fps constantes):

1. **Lienzo de Topología Drag & Drop:**
   - Arrastra agentes, supervisores, memorias, guardrails y herramientas desde la paleta izquierda hacia el lienzo.
   - Posiciona y reorganiza los nodos libremente; cables SVG calculan automáticamente curvas Bézier conectando puertos de entrada y salida.
2. **Inspector de Nodos en Tiempo Real:**
   - Configura el alma (*Soul*), rol, cuota máxima de esfuerzo y directrices de cada agente.
3. **Despachador de Tareas Inteligente:**
   - Redacta requerimientos en Markdown; el clasificador analiza el texto, evalúa la seguridad con los guardrails y delega la tarea al agente óptimo.
4. **Tablero Kanban Integrado:**
   - Visualiza el flujo de tareas entre columnas `Pendientes`, `En Proceso` y `Completadas`.
5. **Consola Criptográfica en Vivo:**
   - Inspecciona en tiempo real la traza de razonamiento (*Chain-of-Thought*), firmas SHA-256 de los sobres y latencias de ejecución.

---

## 🚀 Guía de Instalación y Ejecución Rápida

### Requisitos Previos
- Python 3.11+
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/miguelbenitez09/agentic-brain-core.git
cd agentic-brain-core
```

### 2. Crear Entorno Virtual e Instalar Dependencias
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Ejecutar Pruebas Unitarias Automatizadas
```bash
python -m pytest tests/ -v
```
*(20 pruebas unitarias passing certificando protocolos, guardrails, balanceador, memoria y API).*

---

## ⚡ Formas de Uso y Despliegue

### Opción A: Iniciar el Estudio Visual Web (FastAPI + Drag & Drop UI)
```bash
uvicorn src.serving.api:app --host 127.0.0.1 --port 8000 --reload
```
Abre tu navegador en: **`http://127.0.0.1:8000`** para interactuar con el lienzo visual, crear flujos arrastrando componentes y despachar tareas al clúster.

### Opción B: Iniciar el Dashboard en Streamlit
```bash
streamlit run src/ui/app.py
```
Abre automáticamente en `http://localhost:8501`, permitiendo monitorear métricas de esfuerzo del clúster, explorar la memoria episódica y probar el laboratorio de guardrails.

### Opción C: Usar la Interfaz de Línea de Comandos (CLI)
```bash
# Escanear base de conocimiento documental
python src/cli.py scan ./examples/souls

# Inspeccionar e inferir la huella criptográfica de un alma
python src/cli.py soul ./examples/souls/architect.md

# Administrar la cola de prioridades
python src/cli.py queue add --title "Auditar contratos REST" --priority 1
python src/cli.py queue list
```

---

## 🐳 Despliegue con Docker

Para construir y levantar el contenedor en producción:

```bash
# Construir imagen Docker
docker build -t agentic-brain-core:v1.0.0 .

# Ejecutar contenedor exponiendo API y Studio UI
docker run -p 8000:8000 agentic-brain-core:v1.0.0
```

---

## 📁 Estructura del Proyecto

```
agentic-brain-core/
├── examples/
│   ├── souls/
│   │   ├── architect.md                  # Definición de alma para Agente Arquitecto
│   │   └── qa_auditor.md                 # Definición de alma para Agente Auditor
│   └── workspace/                        # Notas y documentos de contexto local
├── src/
│   ├── agents/
│   │   ├── base_agent.py                 # Entidad fundamental de agente y máquina de estados
│   │   └── agent_swarm.py                # Coordinador del enjambre y supervisor
│   ├── guardrails/
│   │   └── guardrails.py                 # Motor anti-injection, PII scrubber y máscara de secretos
│   ├── memory/
│   │   ├── session_memory.py             # Event sourcing append-only en JSONL con digest SHA-256
│   │   └── memory_manager.py             # Memoria jerárquica unificada (Working, Episodic, Semantic)
│   ├── orchestration/
│   │   ├── task_queue.py                 # Cola de prioridades (1 a 5) y máquina de estados
│   │   └── load_balancer.py              # Clasificador de dominios y balanceador Least-Effort
│   ├── protocols/
│   │   └── envelope.py                   # Sobre formal MessageEnvelope y firmas SHA-256
│   ├── readers/
│   │   └── document_reader.py            # Lector de Markdown frontmatter, JSON, YAML y TXT
│   ├── security/
│   │   └── permission_guard.py           # Frontera RBAC y lista negra de comandos shell
│   ├── souls/
│   │   └── soul_manager.py               # Cargador y validador de integridad de system prompts
│   ├── serving/
│   │   ├── api.py                        # Microservicio FastAPI y servidor web
│   │   └── static/                       # Frontend Drag & Drop
│   │       ├── index.html                # Canvas visual, Kanban e Inspector
│   │       ├── css/studio.css            # Estilos modernos dark mode y cables SVG
│   │       └── js/studio.js              # Controlador interactivo 60fps Vanilla JS
│   ├── ui/
│   │   └── app.py                        # Dashboard complementario en Streamlit
│   └── cli.py                            # CLI nativo para terminal
├── tests/
│   ├── conftest.py
│   ├── test_agent_swarm.py
│   ├── test_api_endpoints.py
│   ├── test_envelope.py
│   ├── test_guardrails.py
│   ├── test_load_balancer.py
│   ├── test_memory.py
│   ├── test_orchestration.py
│   ├── test_readers.py
│   ├── test_security.py
│   └── test_souls.py
├── Dockerfile
├── requirements.txt
├── LICENSE                               # Licencia MIT (v1.0.0 Miguel Benitez)
└── README.md                             # Documentación técnica maestra
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT** - consulta el archivo [LICENSE](LICENSE) para más detalles.  
`Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez UTP - MIT License`
