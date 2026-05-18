"""Lógica de negócio do StudyFlow CLI."""
from __future__ import annotations

import re
from pathlib import Path

from studyflow.api import fetch_motivational_quote
from studyflow.storage import Task, load_tasks, save_tasks

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PRIORIDADES_VALIDAS = {"baixa", "media", "alta"}

class StudyFlowApp:
    def __init__(self, data_file: Path) -> None:
        self._path = data_file

    def _load(self) -> list[Task]:
        return load_tasks(self._path)

    def _save(self, tasks: list[Task]) -> None:
        save_tasks(self._path, tasks)

    def add_task(self, titulo: str, materia: str, prazo: str, prioridade: str) -> Task:
        if not titulo.strip():
            raise ValueError("título não pode estar vazio")
        if not _DATE_RE.match(prazo):
            raise ValueError("Prazo deve estar no formato YYYY-MM-DD")
        if prioridade not in _PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridade inválida: {prioridade!r}")

        tasks = self._load()
        next_id = max((t.id for t in tasks), default=0) + 1
        
        task = Task(
            id=next_id,
            titulo=titulo.strip(),
            materia=materia,
            prazo=prazo,
            prioridade=prioridade
        )
        
        tasks.append(task)
        self._save(tasks)
        return task

    def list_tasks(self, status: str | None = None) -> list[Task]:
        tasks = self._load()
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def complete_task(self, task_id: int) -> Task:
        tasks = self._load()
        for task in tasks:
            if task.id == task_id:
                task.status = "concluida"
                self._save(tasks)
                return task
        raise ValueError(f"Tarefa não encontrada: #{task_id}")

    def remove_task(self, task_id: int) -> None:
        tasks = self._load()
        new_tasks = [t for t in tasks if t.id != task_id]
        if len(new_tasks) == len(tasks):
            raise ValueError(f"Tarefa não encontrada: #{task_id}")
        self._save(new_tasks)

    def summary(self) -> dict[str, int]:
        tasks = self._load()
        return {
            "total": len(tasks),
            "pendentes": sum(1 for t in tasks if t.status == "pendente"),
            "concluidas": sum(1 for t in tasks if t.status == "concluida"),
            "alta_prioridade": sum(1 for t in tasks if t.prioridade == "alta"),
        }

    def get_quote(self) -> dict[str, str]:
        return fetch_motivational_quote()