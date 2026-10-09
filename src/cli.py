"""
Interfaz de Linea de Comandos (CLI) de Agentic Brain Core
Desarrollado v1.0.0 Miguel Benitez / Ing. Miguel Antonio Benitez Gonzalez (UTP)

Permite escanear conocimiento local, gestionar sesiones, validar la integridad
de almas y operar colas de tareas directamente desde la terminal.
"""

import sys
import os
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.readers.document_reader import DocumentReader
from src.memory.session_memory import SessionMemory
from src.souls.soul_manager import SoulManager
from src.orchestration.task_queue import TaskQueue, TaskStatus


def main():
    parser = argparse.ArgumentParser(
        prog="brain",
        description="Agentic Brain Core CLI - Orquestador Ligero de Agentes y Memoria Local v1.0.0 (Miguel Benitez)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando: scan
    parser_scan = subparsers.add_parser("scan", help="Escanear documentos de un directorio")
    parser_scan.add_argument("path", nargs="?", default=".", help="Ruta a escanear")

    # Comando: session
    parser_session = subparsers.add_parser("session", help="Gestionar memoria de sesion")
    parser_session.add_argument("action", choices=["create", "list-events", "summary"], help="Accion de sesion")
    parser_session.add_argument("--id", required=True, help="Identificador de la sesion")
    parser_session.add_argument("--msg", help="Mensaje para registrar en evento")

    # Comando: soul
    parser_soul = subparsers.add_parser("soul", help="Inspeccionar y verificar integridad de almas")
    parser_soul.add_argument("path", help="Ruta al archivo Markdown del alma")

    # Comando: queue
    parser_queue = subparsers.add_parser("queue", help="Gestionar cola de tareas")
    parser_queue.add_argument("action", choices=["add", "list"], help="Accion en la cola")
    parser_queue.add_argument("--title", help="Titulo de la tarea")
    parser_queue.add_argument("--priority", type=int, default=3, help="Prioridad (1-5)")

    args = parser.parse_args()

    if args.command == "scan":
        print(f"[*] Escaneando documentos en: {args.path}")
        docs = DocumentReader.scan_directory(args.path)
        print(f"[+] Total de documentos encontrados: {len(docs)}")
        for d in docs[:10]:
            print(f"  - {d['name']} ({d['size_bytes']} bytes)")
        if len(docs) > 10:
            print(f"  ... y {len(docs)-10} archivos mas.")

    elif args.command == "session":
        mem = SessionMemory(session_id=args.id)
        if args.action == "create":
            ev = mem.record_event("SESSION_CREATED", f"Sesion {args.id} inicializada.")
            print(f"[+] Sesion '{args.id}' creada con digest SHA-256: {ev['digest']}")
        elif args.action == "summary":
            summary = mem.get_summary()
            print(json.dumps(summary, indent=2))
        elif args.action == "list-events":
            events = mem.get_context_window()
            for ev in events:
                print(f"[{ev['step_index']}] {ev['timestamp']} | {ev['type']} | digest={ev['digest'][:8]}...")

    elif args.command == "soul":
        mgr = SoulManager()
        soul = mgr.load_soul(args.path)
        print(f"[+] Alma cargada exitosamente:")
        print(f"  - Nombre: {soul.name}")
        print(f"  - Rol: {soul.role}")
        print(f"  - Huella SHA-256: {soul.fingerprint}")
        print(f"  - Metadatos: {soul.metadata}")

    elif args.command == "queue":
        tq = TaskQueue()
        if args.action == "add":
            if not args.title:
                print("[-] Error: --title es requerido para agregar tareas.")
                return
            t = tq.add_task(title=args.title, description="Agregada via CLI", priority=args.priority)
            print(f"[+] Tarea creada: [{t['id']}] {t['title']} (Prioridad: {t['priority']})")
        elif args.action == "list":
            pending = tq.get_pending_tasks()
            print(f"[+] Tareas pendientes ({len(pending)}):")
            for t in pending:
                print(f"  - [{t['id']}] (P{t['priority']}) {t['title']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
