"""
Gestor Unificado de Memoria Jerarquica (Trabajo, Episodica y Semantica)
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Integra la jerarquia de memoria de agentes para resolucion de problemas complejos:
1. Memoria de Trabajo (Working Memory): Ventana deslizante para el prompt activo.
2. Memoria Episodica (Episodic Memory): Almacenamiento append-only JSONL con hash SHA-256.
3. Memoria Semantica / Documental: Recuperacion de conocimiento local estilo Obsidian.
"""

import os
import re
from typing import Dict, Any, List, Optional
from src.memory.session_memory import SessionMemory
from src.readers.document_reader import DocumentReader


class MemoryManager:
    """Administrador centralizado de memoria para agentes de alto desempeño."""

    def __init__(self, agent_id: str, knowledge_base_dir: str = "examples/workspace"):
        self.agent_id = agent_id
        self.knowledge_base_dir = knowledge_base_dir
        self.episodic_memory = SessionMemory(session_id=agent_id)
        self.working_window_size = 10

    def record_interaction(self, event_type: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Registra un evento en la memoria episodica inmutable."""
        return self.episodic_memory.record_event(event_type, content, metadata)

    def get_working_context(self) -> List[Dict[str, Any]]:
        """Recupera la memoria de trabajo mas reciente sin sobrecargar el contexto."""
        return self.episodic_memory.get_context_window(max_steps=self.working_window_size)

    def search_knowledge_base(self, query: str) -> List[Dict[str, Any]]:
        """Busca fragmentos relevantes en la base documental local por coincidencia de palabras clave."""
        if not os.path.exists(self.knowledge_base_dir):
            return []

        query_terms = set(re.findall(r"\w+", query.lower()))
        matches = []
        docs = DocumentReader.scan_directory(self.knowledge_base_dir)

        for doc_info in docs:
            content = DocumentReader.read_text(doc_info["path"])
            content_lower = content.lower()
            
            # Calcular puntuacion de coincidencia
            hits = sum(1 for term in query_terms if term in content_lower)
            if hits > 0:
                # Extraer parrafo o seccion relevante
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                relevant_para = ""
                for p in paragraphs:
                    if any(term in p.lower() for term in query_terms):
                        relevant_para = p[:300] + "..." if len(p) > 300 else p
                        break

                matches.append({
                    "file_name": doc_info["name"],
                    "path": doc_info["path"],
                    "relevance_score": hits,
                    "snippet": relevant_para
                })

        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matches[:5]
