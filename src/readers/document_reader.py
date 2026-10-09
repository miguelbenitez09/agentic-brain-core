"""
Lectores de Documentos y Contexto Local (Markdown, JSON, YAML, TXT)
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Proporciona capacidades de lectura, analisis de frontmatter y extraccion estructurada
de conocimiento desde repositorios locales estilo Obsidian / Second Brain.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
import yaml


class DocumentReader:
    """Lector polimorfico de contexto y documentos para agentes autonomos."""

    @staticmethod
    def read_text(file_path: str) -> str:
        """Lee el contenido textual integro de un archivo con codificacion UTF-8."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    @classmethod
    def read_markdown(cls, file_path: str) -> Dict[str, Any]:
        """Lee un archivo Markdown extrayendo YAML frontmatter, encabezados y contenido."""
        raw = cls.read_text(file_path)
        frontmatter = {}
        body = raw

        # Extraccion de YAML frontmatter si existe (--- metadata ---)
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
        if frontmatter_match:
            yaml_content, body = frontmatter_match.groups()
            try:
                frontmatter = yaml.safe_load(yaml_content) or {}
            except Exception:
                frontmatter = {"raw_frontmatter": yaml_content}

        # Extraccion de encabezados Markdown
        headers = re.findall(r"^(#{1,6})\s+(.+)$", body, re.MULTILINE)
        headers_summary = [{"level": len(h[0]), "title": h[1].strip()} for h in headers]

        # Extraccion de bloques de codigo
        code_blocks = re.findall(r"```(\w*)\n(.*?)```", body, re.DOTALL)
        blocks_summary = [{"lang": b[0] or "text", "lines": len(b[1].splitlines())} for b in code_blocks]

        return {
            "path": os.path.abspath(file_path),
            "frontmatter": frontmatter,
            "headers": headers_summary,
            "code_blocks": blocks_summary,
            "content": body.strip(),
            "character_count": len(body),
            "line_count": len(body.splitlines())
        }

    @classmethod
    def read_json(cls, file_path: str) -> Dict[str, Any]:
        """Lee y deserializa un archivo JSON estructurado."""
        raw = cls.read_text(file_path)
        return json.loads(raw)

    @classmethod
    def read_yaml(cls, file_path: str) -> Dict[str, Any]:
        """Lee y parsea un archivo de configuracion YAML."""
        raw = cls.read_text(file_path)
        return yaml.safe_load(raw) or {}

    @classmethod
    def scan_directory(cls, dir_path: str, extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Escanea un arbol de directorios retornando un inventario de documentos."""
        if extensions is None:
            extensions = [".md", ".json", ".yaml", ".yml", ".txt"]
        
        inventory = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in extensions:
                    full_path = os.path.join(root, file)
                    inventory.append({
                        "name": file,
                        "path": full_path,
                        "extension": ext,
                        "size_bytes": os.path.getsize(full_path)
                    })
        return inventory
