"""
Pruebas Unitarias para el Lector de Documentos y Contexto
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)
"""

import os
import tempfile
import pytest
from src.readers.document_reader import DocumentReader


def test_read_markdown_with_frontmatter():
    content = """---
title: Arquitectura de Software
category: design
version: 1.0.0
---
# Capitulo 1
Este es el contenido principal.
```python
def test():
    pass
```
"""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md", encoding="utf-8") as f:
        f.write(content)
        temp_path = f.name

    try:
        doc = DocumentReader.read_markdown(temp_path)
        assert doc["frontmatter"]["title"] == "Arquitectura de Software"
        assert doc["frontmatter"]["version"] == "1.0.0"
        assert len(doc["headers"]) == 1
        assert doc["headers"][0]["title"] == "Capitulo 1"
        assert len(doc["code_blocks"]) == 1
        assert doc["code_blocks"][0]["lang"] == "python"
    finally:
        os.remove(temp_path)


def test_scan_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        f1 = os.path.join(tmpdir, "doc1.md")
        f2 = os.path.join(tmpdir, "data.json")
        f3 = os.path.join(tmpdir, "image.png")
        for f in [f1, f2, f3]:
            with open(f, "w") as fp:
                fp.write("dummy")

        inventory = DocumentReader.scan_directory(tmpdir, extensions=[".md", ".json"])
        names = [item["name"] for item in inventory]
        assert "doc1.md" in names
        assert "data.json" in names
        assert "image.png" not in names
