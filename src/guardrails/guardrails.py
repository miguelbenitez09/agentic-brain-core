"""
Motor de Guardrails y Limites de Seguridad de Entrada / Salida
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Aplica filtros de seguridad en tiempo real para:
- Deteccion de inyeccion de prompts y evasiones de instrucciones.
- Enmascaramiento de datos personales (PII) y secretos del sistema.
- Control de cuotas de tokens y validacion de formato de salida.
"""

import re
from typing import Dict, Any, List, Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?guidelines",
    r"system\s+prompt\s+override",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"bypass\s+all\s+safety\s+checks",
    r"reveal\s+your\s+(hidden|internal|system)\s+prompt",
    r"olvida\s+todas\s+las\s+instrucciones\s+anteriores",
    r"ignora\s+las\s+reglas\s+de\s+seguridad",
]

PII_PATTERNS = {
    "email": (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]"),
    "phone": (r"\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]"),
    "panama_id": (r"\b\d{1,2}-\d{3,4}-\d{3,5}\b", "[REDACTED_CEDULA]"),
}

SECRET_KEY_PATTERNS = [
    (r"ghp_[a-zA-Z0-9]{36}", "[GITHUB_PAT_MASKED]"),
    (r"github_pat_[a-zA-Z0-9_]{82}", "[GITHUB_FINE_GRAINED_PAT_MASKED]"),
    (r"sk-[a-zA-Z0-9]{48}", "[API_KEY_MASKED]"),
]


class GuardrailsEngine:
    """Motor integral de proteccion de agentes."""

    def __init__(self, max_input_chars: int = 10000, enforce_pii_scrub: bool = True):
        self.max_input_chars = max_input_chars
        self.enforce_pii_scrub = enforce_pii_scrub
        self.injection_regexes = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

    def validate_input(self, text: str) -> Dict[str, Any]:
        """Evalua el texto de entrada del usuario o agente antes de procesarlo."""
        if not text:
            return {"is_safe": True, "sanitized_text": "", "violations": []}

        violations = []

        # 1. Comprobar limite de caracteres
        if len(text) > self.max_input_chars:
            violations.append(f"Input excedio el limite de {self.max_input_chars} caracteres")

        # 2. Comprobar inyeccion de prompts
        for regex in self.injection_regexes:
            if regex.search(text):
                violations.append(f"Prompt injection detectado: patron '{regex.pattern}'")
                break

        sanitized = text
        # 3. Anonimizacion de PII si corresponde
        if self.enforce_pii_scrub:
            for _, (pattern, replacement) in PII_PATTERNS.items():
                sanitized = re.sub(pattern, replacement, sanitized)

        return {
            "is_safe": len(violations) == 0,
            "violations": violations,
            "sanitized_text": sanitized,
            "original_length": len(text),
            "sanitized_length": len(sanitized)
        }

    def validate_output(self, text: str) -> Dict[str, Any]:
        """Filtra y enmascara la respuesta generada antes de enviarla al exterior."""
        if not text:
            return {"is_safe": True, "sanitized_text": "", "leaks_detected": []}

        leaks = []
        sanitized = text

        # Enmascarar claves y credenciales
        for pattern, replacement in SECRET_KEY_PATTERNS:
            if re.search(pattern, sanitized):
                leaks.append(f"Fuga potencial de credencial detectada: {replacement}")
                sanitized = re.sub(pattern, replacement, sanitized)

        return {
            "is_safe": len(leaks) == 0,
            "leaks_detected": leaks,
            "sanitized_text": sanitized
        }
