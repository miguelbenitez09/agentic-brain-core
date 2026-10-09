"""
Pruebas Unitarias para la Cola de Tareas y Orquestacion
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import pytest
from src.orchestration.task_queue import TaskQueue, TaskStatus


def test_task_queue_priority_ordering():
    tq = TaskQueue()
    t_low = tq.add_task("Tarea Baja", "Descripcion", priority=5)
    t_high = tq.add_task("Tarea Critica", "Descripcion", priority=1)
    t_med = tq.add_task("Tarea Media", "Descripcion", priority=3)

    pending = tq.get_pending_tasks()
    assert len(pending) == 3
    # Debe ordenar primero la de mayor prioridad (numero 1)
    assert pending[0]["id"] == t_high["id"]
    assert pending[1]["id"] == t_med["id"]
    assert pending[2]["id"] == t_low["id"]


def test_task_lifecycle_transitions():
    tq = TaskQueue()
    t = tq.add_task("Auditoria de Codigo", "Revisar AST")
    task_id = t["id"]

    assert t["status"] == TaskStatus.PENDING

    tq.update_status(task_id, TaskStatus.IN_PROGRESS)
    assert tq.get_task(task_id)["status"] == TaskStatus.IN_PROGRESS

    tq.update_status(task_id, TaskStatus.COMPLETED, result={"gaps_found": 0})
    final_task = tq.get_task(task_id)
    assert final_task["status"] == TaskStatus.COMPLETED
    assert final_task["result"]["gaps_found"] == 0
