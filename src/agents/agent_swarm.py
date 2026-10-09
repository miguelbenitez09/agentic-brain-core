"""
Enjambre de Agentes y Coordinador Central de Ejecucion
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Orquesta un conjunto heterogeneo de agentes especializados, gestionando:
- Inyeccion de guardrails de entrada y salida.
- Clasificacion y balanceo de carga/esfuerzo en tiempo real.
- Enrutamiento de mensajes y trazabilidad global de ejecucion.
"""

import time
from typing import Dict, Any, List, Optional

from src.agents.base_agent import BaseAgent, AgentState
from src.souls.soul_manager import Soul, SoulManager
from src.security.permission_guard import PermissionGuard
from src.guardrails.guardrails import GuardrailsEngine
from src.orchestration.task_queue import TaskQueue, TaskStatus
from src.orchestration.load_balancer import LoadBalancer, TaskClassifier
from src.protocols.envelope import MessageEnvelope, MessageType


class AgentSwarm:
    """Coordinador central y supervisor de enjambre de agentes autonomos."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue = TaskQueue()
        self.load_balancer = LoadBalancer()
        self.guardrails = GuardrailsEngine()
        self.execution_history: List[Dict[str, Any]] = []

    def register_agent(
        self,
        agent_id: str,
        soul: Soul,
        capabilities: Optional[List[str]] = None,
        max_effort: int = 20
    ) -> BaseAgent:
        """Crea y registra un nuevo agente en el enjambre y en el balanceador."""
        caps = set(capabilities) if capabilities else {"READ_DOCS"}
        guard = PermissionGuard(allowed_capabilities=caps)
        agent = BaseAgent(agent_id=agent_id, soul=soul, permission_guard=guard)
        
        self.agents[agent_id] = agent
        
        # Registrar en el balanceador de carga con los dominios derivados del alma
        domain_tags = [soul.role.lower(), soul.name.lower()]
        if capabilities:
            domain_tags.extend([c.lower() for c in capabilities])
        
        self.load_balancer.register_agent(
            agent_id=agent_id,
            name=soul.name,
            capabilities=domain_tags,
            max_effort=max_effort
        )
        return agent

    def dispatch_task(self, title: str, description: str, priority: int = 3) -> Dict[str, Any]:
        """Procesa una tarea atravesando el pipeline completo: Guardrails -> Clasificacion -> Balanceo -> Ejecucion."""
        t0 = time.perf_counter()

        # 1. Guardrail de entrada
        input_check = self.guardrails.validate_input(description)
        if not input_check["is_safe"]:
            return {
                "status": "BLOCKED_BY_GUARDRAIL",
                "violations": input_check["violations"],
                "reason": "La tarea violo las politicas de seguridad del sistema."
            }

        sanitized_description = input_check["sanitized_text"]

        # 2. Agregar a la cola formal
        task = self.task_queue.add_task(title=title, description=sanitized_description, priority=priority)
        task_id = task["id"]

        # 3. Clasificacion y estimacion de esfuerzo
        analysis = TaskClassifier.classify_task(title, sanitized_description)
        domain = analysis["primary_domain"]
        effort = analysis["effort_points"]

        # 4. Asignacion en balanceador de carga
        assigned_agent_id = self.load_balancer.assign_task(task_id, domain, effort)

        if not assigned_agent_id or assigned_agent_id not in self.agents:
            self.task_queue.update_status(task_id, TaskStatus.FAILED, result={"error": "No hay agentes disponibles con capacidad"})
            return {
                "task_id": task_id,
                "status": "QUEUED_UNASSIGNED",
                "message": "En cola: Todos los agentes del clúster estan en maxima capacidad.",
                "analysis": analysis
            }

        agent = self.agents[assigned_agent_id]
        self.task_queue.update_status(task_id, TaskStatus.IN_PROGRESS)

        # 5. Ejecucion del agente
        envelope = agent.execute_step(sanitized_description, context={"title": title, "domain": domain})

        # 6. Guardrail de salida
        output_check = self.guardrails.validate_output(envelope.payload.get("response", ""))
        sanitized_response = output_check["sanitized_text"]
        envelope.payload["response"] = sanitized_response

        # 7. Liberar esfuerzo en el balanceador y actualizar estado
        self.load_balancer.release_task(task_id, effort)
        self.task_queue.update_status(task_id, TaskStatus.COMPLETED, result=envelope.payload)

        latency_ms = (time.perf_counter() - t0) * 1000.0

        trace_record = {
            "task_id": task_id,
            "title": title,
            "assigned_agent": assigned_agent_id,
            "agent_name": agent.soul.name,
            "domain": domain,
            "effort_points": effort,
            "latency_ms": round(latency_ms, 2),
            "envelope": envelope.model_dump(),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        self.execution_history.append(trace_record)

        return {
            "task_id": task_id,
            "status": "COMPLETED",
            "assigned_agent": assigned_agent_id,
            "agent_name": agent.soul.name,
            "domain": domain,
            "effort_points": effort,
            "latency_ms": round(latency_ms, 2),
            "response": sanitized_response,
            "reasoning_trace": envelope.payload.get("reasoning_trace"),
            "envelope_signature": envelope.signature
        }

    def get_swarm_telemetry(self) -> Dict[str, Any]:
        """Retorna telemetria completa del enjambre, cola y balanceador."""
        return {
            "agents_count": len(self.agents),
            "pending_tasks_count": len(self.task_queue.get_pending_tasks()),
            "completed_tasks_count": len(self.execution_history),
            "cluster_load": self.load_balancer.get_cluster_status(),
            "recent_traces": self.execution_history[-5:] if self.execution_history else []
        }
