"""
Frontera de Seguridad, Control de Permisos de Herramientas y Gestion de Secretos
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Garantiza ejecucion segura de herramientas por agentes autonomos implementando:
- Politicas de control de acceso basado en roles (RBAC) y listas blancas/negras.
- Prevencion de ejecucion de comandos destructivos en el shell.
- Enmascaramiento de tokens y claves en registros de auditoria.
"""

import os
import re
from typing import Set, Dict, Any, Optional

FORBIDDEN_COMMAND_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\bformat\s+[c-z]:",
    r"\bdel\s+/f\s+/s\s+/q\s+c:\\windows",
    r"\bshutdown\b",
    r"\bdd\s+if=",
]


class PermissionGuard:
    """Validador de limites de seguridad y permisos para llamadas a herramientas."""

    def __init__(self, allowed_capabilities: Optional[Set[str]] = None):
        # Capacidades por defecto: solo lectura de documentos
        self.allowed_capabilities = allowed_capabilities or {"READ_DOCS"}

    def has_permission(self, capability: str) -> bool:
        """Verifica si el agente posee la capacidad solicitada."""
        return capability.upper() in self.allowed_capabilities

    def validate_command_execution(self, command: str) -> bool:
        """Verifica si un comando del shell es seguro y esta autorizado."""
        if not self.has_permission("EXECUTE_SHELL"):
            return False

        for pattern in FORBIDDEN_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False

        return True


class SecretsManager:
    """Gestor seguro de variables confidenciales y enmascaramiento."""

    def __init__(self, secrets_dict: Optional[Dict[str, str]] = None):
        self._secrets: Dict[str, str] = secrets_dict or {}

    def get_secret(self, key: str, fallback_env: bool = True) -> Optional[str]:
        """Obtiene un secreto sin registrar su valor en texto claro."""
        val = self._secrets.get(key)
        if val is None and fallback_env:
            val = os.getenv(key)
        return val

    def mask_secret(self, text: str) -> str:
        """Enmascara cualquier ocurrencia de un secreto en cadenas de texto."""
        masked = text
        for k, v in self._secrets.items():
            if v and len(v) >= 6:
                masked = masked.replace(v, f"[SECRET_{k}_MASKED]")
        return masked
