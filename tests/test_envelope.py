"""
Pruebas Unitarias para el Protocolo MessageEnvelope
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import pytest
from src.protocols.envelope import MessageEnvelope, MessageType


def test_envelope_creation_and_signing():
    env = MessageEnvelope(
        sender="agent_01",
        recipient="agent_02",
        message_type=MessageType.REQUEST,
        payload={"query": "Realizar auditoria de seguridad"}
    )
    assert env.id is not None
    assert env.signature is None

    env.sign(secret_key="test_secret_123")
    assert env.signature is not None
    assert len(env.signature) == 64

    # Validar firma correcta
    assert env.verify_signature(secret_key="test_secret_123") is True
    # Validar firma con clave incorrecta
    assert env.verify_signature(secret_key="wrong_secret") is False
