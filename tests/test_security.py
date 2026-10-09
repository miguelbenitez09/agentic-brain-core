"""
Pruebas Unitarias de Seguridad, Control de Permisos y Enmascaramiento
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import pytest
from src.security.permission_guard import PermissionGuard, SecretsManager


def test_permission_guard_capabilities():
    guard_readonly = PermissionGuard(allowed_capabilities={"READ_DOCS"})
    assert guard_readonly.has_permission("READ_DOCS") is True
    assert guard_readonly.has_permission("EXECUTE_SHELL") is False
    assert guard_readonly.validate_command_execution("ls -la") is False

    guard_shell = PermissionGuard(allowed_capabilities={"READ_DOCS", "EXECUTE_SHELL"})
    assert guard_shell.has_permission("EXECUTE_SHELL") is True
    assert guard_shell.validate_command_execution("git status") is True
    # Comando destructivo en lista negra
    assert guard_shell.validate_command_execution("rm -rf /") is False


def test_secrets_manager_masking():
    secrets = {"API_KEY": "super_secret_pat_998877", "DB_PASS": "pass123456"}
    mgr = SecretsManager(secrets_dict=secrets)

    text = "Conectando con super_secret_pat_998877 a la base de datos"
    masked = mgr.mask_secret(text)
    assert "super_secret_pat_998877" not in masked
    assert "[SECRET_API_KEY_MASKED]" in masked
