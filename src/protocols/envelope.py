"""
Protocolo Estandarizado de Mensajeria Inter-Agente y Envoltorio MCP / JSON-RPC
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Define el sobre formal de comunicacion (MessageEnvelope) para intercambio asincrono
entre agentes autonomos, supervisores y clientes, garantizando trazabilidad,
tipado estricto y firma de integridad.
"""

import time
import uuid
import hashlib
import json
from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    BROADCAST = "BROADCAST"
    HEARTBEAT = "HEARTBEAT"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    ERROR = "ERROR"


class MessageEnvelope(BaseModel):
    """Sobre universal de comunicacion entre agentes."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str = Field(default="global")
    sender: str
    recipient: str
    message_type: MessageType = MessageType.REQUEST
    payload: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=3, ge=1, le=5, description="1 = Critica, 5 = Baja")
    step_index: int = 0
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    signature: Optional[str] = None

    def sign(self, secret_key: str = "agentic_brain_secret") -> "MessageEnvelope":
        """Calcula una firma criptografica SHA-256 sobre el cuerpo del mensaje."""
        raw = f"{self.id}:{self.sender}:{self.recipient}:{json.dumps(self.payload, sort_keys=True)}:{secret_key}"
        self.signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self

    def verify_signature(self, secret_key: str = "agentic_brain_secret") -> bool:
        """Verifica la autenticidad del mensaje."""
        if not self.signature:
            return False
        raw = f"{self.id}:{self.sender}:{self.recipient}:{json.dumps(self.payload, sort_keys=True)}:{secret_key}"
        expected = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self.signature == expected
