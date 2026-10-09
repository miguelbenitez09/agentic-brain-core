"""
Microservicio REST FastAPI y Servidor Web de Agentic Brain Core Studio
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Expone la API de orquestacion multi-agente, despacho balanceado, guardrails
y sirve la aplicacion web interactiva Drag & Drop.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agents.agent_swarm import AgentSwarm
from src.souls.soul_manager import Soul
from src.guardrails.guardrails import GuardrailsEngine

app = FastAPI(
    title="Agentic Brain Core API & Studio",
    description="Plataforma de Orquestacion Multi-Agente, Balanceo de Esfuerzo y Memoria v1.0.0 por Ing. Miguel Antonio Benitez Gonzalez (UTP)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar Swarm central con agentes de referencia
swarm = AgentSwarm()

# Registrar agentes por defecto
soul_arch = Soul(
    name="Architect Agent (UTP)",
    role="Solutions & Systems Architect",
    system_prompt="Eres el Agente Arquitecto Principal de Soluciones de Software y MLOps."
)
soul_qa = Soul(
    name="QA & Security Auditor",
    role="Quality Assurance and Security Auditor",
    system_prompt="Eres el Agente Auditor Principal de Calidad, Resiliencia y Seguridad."
)
soul_backend = Soul(
    name="Backend Specialist",
    role="High-Performance Backend Engineer",
    system_prompt="Eres el Ingeniero de Backend especializado en APIs REST, Go y Python."
)

swarm.register_agent("agent_architect", soul_arch, capabilities=["architecture", "design", "general"], max_effort=25)
swarm.register_agent("agent_qa", soul_qa, capabilities=["qa_security", "testing", "security"], max_effort=20)
swarm.register_agent("agent_backend", soul_backend, capabilities=["backend", "api", "database"], max_effort=25)

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class TaskDispatchRequest(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = Field(..., min_length=5)
    priority: int = Field(default=3, ge=1, le=5)


class GuardrailValidateRequest(BaseModel):
    text: str


@app.get("/")
def get_studio_ui():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Agentic Brain Core Studio v1.0.0 listo"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "agentic-brain-core",
        "version": "1.0.0",
        "author": "Ing. Miguel Antonio Benitez Gonzalez (UTP)",
        "active_agents": len(swarm.agents)
    }


@app.get("/api/v1/swarm/telemetry")
def get_telemetry():
    return swarm.get_swarm_telemetry()


@app.get("/api/v1/swarm/agents")
def list_agents():
    return {
        "agents": [
            {
                "id": a.agent_id,
                "name": a.soul.name,
                "role": a.soul.role,
                "state": a.state.value,
                "fingerprint": a.soul.fingerprint
            }
            for a in swarm.agents.values()
        ]
    }


@app.post("/api/v1/swarm/dispatch")
def dispatch_task(request: TaskDispatchRequest):
    result = swarm.dispatch_task(
        title=request.title,
        description=request.description,
        priority=request.priority
    )
    return result


@app.get("/api/v1/swarm/tasks")
def list_tasks():
    pending = swarm.task_queue.get_pending_tasks()
    return {
        "pending": pending,
        "completed": swarm.execution_history
    }


@app.post("/api/v1/guardrails/validate")
def validate_guardrails(request: GuardrailValidateRequest):
    guardrails = GuardrailsEngine()
    input_result = guardrails.validate_input(request.text)
    output_result = guardrails.validate_output(request.text)
    return {
        "input_evaluation": input_result,
        "output_evaluation": output_result
    }


@app.get("/api/v1/memory/{agent_id}")
def get_agent_memory(agent_id: str, limit: int = 10):
    if agent_id not in swarm.agents:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    agent = swarm.agents[agent_id]
    context = agent.memory.get_context_window(max_steps=limit)
    return {
        "agent_id": agent_id,
        "events": context
    }
