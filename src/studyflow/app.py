"""Lógica de negócio do StudyFlow CLI."""
from __future__ import annotations

import re

from studyflow.api import fetch_motivational_quote
from studyflow.database import Task, delete_task, insert_task, load_tasks, update_task_status

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PRIORIDADES_VALIDAS = {"baixa", "media", "alta"}


class StudyFlowApp:
    def add_task(self, titulo: str, materia: str, prazo: str, prioridade: str) -> Task:
        if not titulo.strip():
            raise ValueError("título não pode estar vazio")
        if not _DATE_RE.match(prazo):
            raise ValueError("Prazo deve estar no formato YYYY-MM-DD")
        if prioridade not in _PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridade inválida: {prioridade!r}")

        return insert_task(titulo.strip(), materia, prazo, prioridade)

    def list_tasks(self, status: str | None = None) -> list[Task]:
        tasks = load_tasks()
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def complete_task(self, task_id: int) -> Task:
        return update_task_status(task_id, "concluida")

    def remove_task(self, task_id: int) -> None:
        delete_task(task_id)

    def summary(self) -> dict[str, int]:
        tasks = load_tasks()
        return {
            "total": len(tasks),
            "pendentes": sum(1 for t in tasks if t.status == "pendente"),
            "concluidas": sum(1 for t in tasks if t.status == "concluida"),
            "alta_prioridade": sum(1 for t in tasks if t.prioridade == "alta"),
        }

    def get_quote(self) -> dict[str, str]:
        return fetch_motivational_quote()