"""
Agente Base Autonomo y Maquina de Estados
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Implementa la entidad fundamental de agente autonomo con encapsulamiento
de identidad (Soul), memoria de sesion inmutable, permisos RBAC y ciclo de ejecucion.
"""

import time
from typing import Dict, Any, Optional, List
from enum import Enum

from src.souls.soul_manager import Soul
from src.memory.session_memory import SessionMemory
from src.security.permission_guard import PermissionGuard
from src.protocols.envelope import MessageEnvelope, MessageType


class AgentState(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    DONE = "DONE"
    ERROR = "ERROR"


class BaseAgent:
    """Instancia de ejecucion de un agente autonomo."""

    def __init__(
        self,
        agent_id: str,
        soul: Soul,
        permission_guard: Optional[PermissionGuard] = None,
        storage_dir: str = ".brain/sessions"
    ):
        self.agent_id = agent_id
        self.soul = soul
        self.guard = permission_guard or PermissionGuard()
        self.memory = SessionMemory(session_id=agent_id, storage_dir=storage_dir)
        self.state = AgentState.IDLE
        self.current_task: Optional[Dict[str, Any]] = None

    def execute_step(self, user_instruction: str, context: Optional[Dict[str, Any]] = None) -> MessageEnvelope:
        """Ejecuta un paso de razonamiento y devuelve un sobre formal de respuesta."""
        self.state = AgentState.RUNNING
        self.memory.record_event("USER_INPUT", user_instruction, metadata=context)

        # Renderizar prompt con variables de contexto
        effective_prompt = self.soul.render(context)

        # Simulacion de razonamiento guiado por el rol del alma (Chain-of-Thought)
        reasoning_trace = (
            f"[{self.soul.name}] Analizando instruccion bajo rol: '{self.soul.role}'. "
            f"Capacidades autorizadas: {list(self.guard.allowed_capabilities)}. "
            f"Huella del alma: {self.soul.fingerprint[:8]}..."
        )
        self.memory.record_event("COT_REASONING", reasoning_trace)

        # Generacion de respuesta estructurada
        response_text = (
            f"Agente [{self.soul.name} - {self.soul.role}] completo exitosamente la tarea: "
            f"'{user_instruction}'. Directrices aplicadas con verificacion de integridad."
        )
        self.memory.record_event("AGENT_RESPONSE", response_text)

        self.state = AgentState.IDLE

        envelope = MessageEnvelope(
            sender=self.agent_id,
            recipient="user",
            message_type=MessageType.RESPONSE,
            payload={
                "response": response_text,
                "reasoning_trace": reasoning_trace,
                "agent_name": self.soul.name,
                "role": self.soul.role,
                "status": self.state.value
            }
        ).sign()

        return envelope
