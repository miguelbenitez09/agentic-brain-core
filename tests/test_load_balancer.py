"""
Pruebas Unitarias para el Balanceador de Carga y Clasificador de Tareas
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import pytest
from src.orchestration.load_balancer import LoadBalancer, TaskClassifier


def test_task_classification_domain_and_effort():
    analysis = TaskClassifier.classify_task(
        title="Crear microservicio REST con FastAPI y endpoints SQL",
        description="Implementar CRUD con SQLAlchemy y Postgres"
    )
    assert analysis["primary_domain"] == "backend"
    assert analysis["effort_points"] >= 2


def test_load_balancer_least_effort_distribution():
    lb = LoadBalancer()
    lb.register_agent("agent_1", "Backend Dev", ["backend"], max_effort=20)
    lb.register_agent("agent_2", "Backend Dev Backup", ["backend"], max_effort=20)

    # Primera tarea asignada
    assigned_1 = lb.assign_task("task_01", "backend", 8)
    assert assigned_1 in ["agent_1", "agent_2"]

    # Segunda tarea debe ir al otro agente por algoritmo de menor esfuerzo acumulado
    other_agent = "agent_2" if assigned_1 == "agent_1" else "agent_1"
    assigned_2 = lb.assign_task("task_02", "backend", 6)
    assert assigned_2 == other_agent

    # Liberar tarea
    lb.release_task("task_01", 8)
    assert lb.agents[assigned_1]["current_effort"] == 0
