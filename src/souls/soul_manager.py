"""
Gestor de Identidades de Agentes y System Prompts (Souls)
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Gestiona la definicion, carga, verificacion criptografica (SHA-256) e interpolacion
de variables en las almas (souls) y system prompts de agentes autonomos.
"""

import os
import hashlib
from typing import Dict, Any, Optional
from src.readers.document_reader import DocumentReader


class Soul:
    """Representacion inmutable de la identidad y directrices de un agente."""

    def __init__(self, name: str, role: str, system_prompt: str, metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.metadata = metadata or {}
        self.fingerprint = self._calculate_fingerprint()

    def _calculate_fingerprint(self) -> str:
        """Calcula el digest SHA-256 del system prompt para garantizar su inmutabilidad."""
        data = f"{self.name}:{self.role}:{self.system_prompt}".encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def render(self, context_vars: Optional[Dict[str, Any]] = None) -> str:
        """Interpola variables contextuales (ej. {{nombre}}) dentro del prompt."""
        rendered = self.system_prompt
        if context_vars:
            for k, v in context_vars.items():
                rendered = rendered.replace(f"{{{{{k}}}}}", str(v))
        return rendered


class SoulManager:
    """Cargador y registro de almas de agentes desde el disco local."""

    def __init__(self, souls_dir: str = "examples/souls"):
        self.souls_dir = souls_dir
        self.souls_cache: Dict[str, Soul] = {}

    def load_soul(self, soul_path: str) -> Soul:
        """Carga una definicion de alma desde un archivo Markdown con frontmatter."""
        doc = DocumentReader.read_markdown(soul_path)
        fm = doc.get("frontmatter", {})
        
        name = fm.get("name", os.path.splitext(os.path.basename(soul_path))[0])
        role = fm.get("role", "Autonomous AI Assistant")
        prompt = doc.get("content", "")

        soul = Soul(name=name, role=role, system_prompt=prompt, metadata=fm)
        self.souls_cache[name] = soul
        return soul

    def get_soul(self, name: str) -> Optional[Soul]:
        """Obtiene un alma desde la memoria cache."""
        return self.souls_cache.get(name)

    def verify_integrity(self, soul_name: str, expected_fingerprint: str) -> bool:
        """Valida si el system prompt ha sido alterado comparando el digest SHA-256."""
        soul = self.get_soul(soul_name)
        if not soul:
            return False
        return soul.fingerprint == expected_fingerprint
