"""
Clasificador de Tareas, Balanceador de Carga y Distribuidor de Esfuerzo
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Implementa algoritmos de balanceo inteligente de trabajo:
- Clasificacion semantica de tareas por dominio tecnologico.
- Estimacion heuristica de puntos de esfuerzo (Effort Points: 1 a 10).
- Despacho de carga mediante algoritmo de 'Menor Esfuerzo Acumulado' (Least-Effort Routing).
"""

import re
from typing import Dict, Any, List, Optional
from collections import defaultdict

DOMAIN_KEYWORDS = {
    "architecture": ["arquitectura", "diseño", "patron", "microservicio", "c4", "uml", "diagrama", "sistema"],
    "backend": ["api", "fastapi", "endpoint", "base de datos", "sql", "postgres", "query", "orm", "crud"],
    "frontend": ["ui", "interfaz", "css", "html", "javascript", "drag and drop", "componente", "responsive"],
    "data_science": ["modelo", "entrenamiento", "prediccion", "dataset", "eda", "lightgbm", "xgboost", "metrics"],
    "qa_security": ["test", "prueba", "pytest", "seguridad", "vulnerabilidad", "rbac", "auditoria", "guardrail"],
    "devops": ["docker", "dockerfile", "ci", "cd", "github actions", "k8s", "deploy", "pipeline"],
}


class TaskClassifier:
    """Clasifica tareas y estima la dificultad / esfuerzo requerido."""

    @staticmethod
    def classify_task(title: str, description: str) -> Dict[str, Any]:
        """Determina el dominio tecnologico y puntos de esfuerzo de la tarea."""
        combined_text = f"{title} {description}".lower()
        domain_scores = defaultdict(int)

        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in combined_text:
                    domain_scores[domain] += 1

        # Dominio predominante
        best_domain = "general"
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]

        # Estimacion de esfuerzo (1 = trivial, 10 = muy complejo)
        length_factor = min(4, len(combined_text) // 100)
        complexity_keywords = ["integral", "arquitectura", "critico", "seguridad", "balanceador", "multi-agente"]
        complexity_hits = sum(1 for kw in complexity_keywords if kw in combined_text)
        
        effort_points = max(1, min(10, 2 + length_factor + complexity_hits * 2))

        return {
            "primary_domain": best_domain,
            "domain_scores": dict(domain_scores),
            "effort_points": effort_points,
            "estimated_time_min": effort_points * 15
        }


class LoadBalancer:
    """Balanceador de carga y asignador de esfuerzo entre agentes disponibles."""

    def __init__(self):
        # Registro de agentes: agent_id -> { "name": ..., "capabilities": [...], "current_effort": 0, "max_effort": 20 }
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.assigned_tasks: Dict[str, str] = {}  # task_id -> agent_id

    def register_agent(self, agent_id: str, name: str, capabilities: List[str], max_effort: int = 20) -> None:
        """Registra un agente en el grupo de balanceo."""
        self.agents[agent_id] = {
            "id": agent_id,
            "name": name,
            "capabilities": [c.lower() for c in capabilities],
            "current_effort": 0,
            "max_effort": max_effort,
            "tasks_count": 0,
            "status": "AVAILABLE"
        }

    def unregister_agent(self, agent_id: str) -> None:
        """Elimina un agente del grupo."""
        if agent_id in self.agents:
            del self.agents[agent_id]

    def select_best_agent(self, domain: str, effort_points: int) -> Optional[str]:
        """Selecciona el agente idoneo utilizando el criterio de menor esfuerzo acumulado."""
        eligible_agents = []
        domain_lower = domain.lower()

        for a_id, info in self.agents.items():
            # Comprobar si puede aceptar la carga
            if info["current_effort"] + effort_points > info["max_effort"]:
                continue
            
            # Puntuacion por coincidencia de capacidad
            has_domain = domain_lower in info["capabilities"] or "general" in info["capabilities"] or not info["capabilities"]
            score = 10 if has_domain else 1
            
            eligible_agents.append((a_id, info["current_effort"], score))

        if not eligible_agents:
            # Fallback: devolver el agente con menor esfuerzo aunque exceda temporalmente
            if self.agents:
                return min(self.agents.items(), key=lambda x: x[1]["current_effort"])[0]
            return None

        # Ordenar por: coincidencia de habilidad descendente, luego esfuerzo acumulado ascendente
        eligible_agents.sort(key=lambda x: (-x[2], x[1]))
        return eligible_agents[0][0]

    def assign_task(self, task_id: str, domain: str, effort_points: int) -> Optional[str]:
        """Asigna una tarea al agente optimo y actualiza los medidores de esfuerzo."""
        selected_agent = self.select_best_agent(domain, effort_points)
        if selected_agent:
            self.agents[selected_agent]["current_effort"] += effort_points
            self.agents[selected_agent]["tasks_count"] += 1
            self.assigned_tasks[task_id] = selected_agent
            if self.agents[selected_agent]["current_effort"] >= self.agents[selected_agent]["max_effort"]:
                self.agents[selected_agent]["status"] = "SATURATED"
        return selected_agent

    def release_task(self, task_id: str, effort_points: int) -> None:
        """Libera la carga asociada a una tarea completada."""
        agent_id = self.assigned_tasks.pop(task_id, None)
        if agent_id and agent_id in self.agents:
            self.agents[agent_id]["current_effort"] = max(0, self.agents[agent_id]["current_effort"] - effort_points)
            self.agents[agent_id]["tasks_count"] = max(0, self.agents[agent_id]["tasks_count"] - 1)
            self.agents[agent_id]["status"] = "AVAILABLE"

    def get_cluster_status(self) -> Dict[str, Any]:
        """Retorna telemetria en tiempo real de la distribucion de carga."""
        total_effort = sum(a["current_effort"] for a in self.agents.values())
        max_capacity = sum(a["max_effort"] for a in self.agents.values())
        utilization_pct = (total_effort / max_capacity * 100.0) if max_capacity > 0 else 0.0

        return {
            "total_agents": len(self.agents),
            "total_effort_allocated": total_effort,
            "max_cluster_capacity": max_capacity,
            "cluster_utilization_pct": round(utilization_pct, 2),
            "agents_breakdown": self.agents
        }
