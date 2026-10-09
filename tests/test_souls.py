"""
Pruebas Unitarias para el Gestor de Souls e Integridad de Prompts
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import os
import tempfile
import pytest
from src.souls.soul_manager import SoulManager, Soul


def test_soul_loading_and_fingerprint():
    content = """---
name: security_auditor
role: Cybersecurity Auditor
---
Eres el auditor encargado del proyecto {{project_name}}.
"""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md", encoding="utf-8") as f:
        f.write(content)
        temp_path = f.name

    try:
        mgr = SoulManager()
        soul = mgr.load_soul(temp_path)

        assert soul.name == "security_auditor"
        assert soul.role == "Cybersecurity Auditor"
        assert len(soul.fingerprint) == 64  # SHA-256 hex digest length

        rendered = soul.render({"project_name": "amp-cont-ai"})
        assert "amp-cont-ai" in rendered

        # Verificar integridad
        assert mgr.verify_integrity("security_auditor", soul.fingerprint) is True
        assert mgr.verify_integrity("security_auditor", "invalid_digest") is False
    finally:
        os.remove(temp_path)
