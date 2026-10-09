"""
Pruebas Unitarias para el Gestor de Memoria de Sesion
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import os
import tempfile
import pytest
from src.memory.session_memory import SessionMemory


def test_session_memory_append_and_digest():
    with tempfile.TemporaryDirectory() as tmpdir:
        session = SessionMemory(session_id="test_session_01", storage_dir=tmpdir)
        ev1 = session.record_event("USER_INPUT", "Hola agente, inicia el analisis")
        ev2 = session.record_event("AGENT_RESPONSE", "Analisis completado exitosamente")

        assert len(session.events) == 2
        assert ev1["digest"] is not None
        assert ev2["digest"] is not None
        assert ev1["digest"] != ev2["digest"]

        # Validar persistencia e hidratacion de sesion
        reloaded = SessionMemory(session_id="test_session_01", storage_dir=tmpdir)
        assert len(reloaded.events) == 2
        assert reloaded.events[0]["content"] == "Hola agente, inicia el analisis"

        summary = reloaded.get_summary()
        assert summary["total_events"] == 2
