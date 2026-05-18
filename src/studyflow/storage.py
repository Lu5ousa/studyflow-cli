"""Módulo de armazenamento de dados do StudyFlow."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class Task:
    id: int
    titulo: str
    materia: str
    prazo: str
    prioridade: str
    status: str = "pendente"

def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task(**item) for item in data]
    except (json.JSONDecodeError, TypeError):
        return []

def save_tasks(path: Path, tasks: list[Task]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, indent=4, ensure_ascii=False)