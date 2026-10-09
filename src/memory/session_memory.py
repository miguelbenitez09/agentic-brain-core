"""
Gestor de Sesiones y Memoria Episodica de Agentes
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Implementa almacenamiento persistente inmutable (append-only JSONL event sourcing)
para mantener la traza de ejecucion de agentes, memoria de conversacion y recuperacion
de contexto sin desbordamiento de memoria.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional


class SessionMemory:
    """Gestor de memoria de sesion con trazabilidad criptografica."""

    def __init__(self, session_id: str, storage_dir: str = ".brain/sessions"):
        self.session_id = session_id
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.log_file = os.path.join(self.storage_dir, f"{session_id}.jsonl")
        self.events: List[Dict[str, Any]] = []
        self._load_existing_events()

    def _load_existing_events(self) -> None:
        """Carga eventos previos si la sesion ya existia."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.events.append(json.loads(line))
                        except Exception:
                            pass

    def record_event(self, event_type: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Registra un evento inmutable en la memoria de la sesion."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        event = {
            "session_id": self.session_id,
            "step_index": len(self.events),
            "timestamp": timestamp,
            "type": event_type,
            "content": content,
            "metadata": metadata or {},
        }
        
        # Calcular hash de integridad del evento
        payload_bytes = json.dumps(event, sort_keys=True).encode("utf-8")
        event["digest"] = hashlib.sha256(payload_bytes).hexdigest()

        self.events.append(event)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        return event

    def get_context_window(self, max_steps: Optional[int] = None) -> List[Dict[str, Any]]:
        """Recupera los eventos mas recientes dentro de una ventana de contexto."""
        if max_steps is None or max_steps >= len(self.events):
            return list(self.events)
        return self.events[-max_steps:]

    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del estado actual de la sesion."""
        types_count = {}
        for ev in self.events:
            t = ev.get("type", "unknown")
            types_count[t] = types_count.get(t, 0) + 1

        return {
            "session_id": self.session_id,
            "total_events": len(self.events),
            "event_breakdown": types_count,
            "log_path": os.path.abspath(self.log_file)
        }
