"""
Cola de Tareas, Seguimiento de Brechas (Gaps) y Despachador de Agentes
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Gestiona la cola de prioridades de tareas tecnicas, transiciones de estado
y coordinacion de ejecucion entre agentes especializados.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskQueue:
    """Cola de tareas con soporte de prioridades (1 = Alta, 5 = Baja)."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def add_task(self, title: str, description: str, priority: int = 3, target_agent: Optional[str] = None) -> Dict[str, Any]:
        """Agrega una nueva tarea a la cola."""
        task_id = str(uuid.uuid4())[:8]
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "target_agent": target_agent or "default",
            "status": TaskStatus.PENDING,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "result": None,
        }
        self.tasks[task_id] = task
        return task

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Retorna las tareas pendientes ordenadas por prioridad (menor numero = mayor prioridad)."""
        pending = [t for t in self.tasks.values() if t["status"] == TaskStatus.PENDING]
        pending.sort(key=lambda x: x["priority"])
        return pending

    def update_status(self, task_id: str, status: TaskStatus, result: Optional[Any] = None) -> Optional[Dict[str, Any]]:
        """Actualiza el estado y resultado de una tarea."""
        if task_id not in self.tasks:
            return None
        self.tasks[task_id]["status"] = status
        self.tasks[task_id]["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if result is not None:
            self.tasks[task_id]["result"] = result
        return self.tasks[task_id]

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una tarea por su identificador."""
        return self.tasks.get(task_id)
