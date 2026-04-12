from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from studyflow.storage import JsonStorage

VALID_PRIORITIES = {"baixa", "media", "alta"}
VALID_STATUS = {"pendente", "concluida"}
DATE_FORMAT = "%Y-%m-%d"


@dataclass(slots=True)
class Task:
    id: int
    titulo: str
    materia: str
    prazo: str
    prioridade: str
    status: str = "pendente"


class StudyFlowApp:
    def __init__(self, data_file: str | Path = "data/study_tasks.json") -> None:
        self.storage = JsonStorage(Path(data_file))

    def add_task(self, titulo: str, materia: str, prazo: str, prioridade: str) -> Task:
        titulo = titulo.strip()
        materia = materia.strip()
        prioridade = prioridade.strip().lower()

        if not titulo:
            raise ValueError("O título não pode estar vazio.")
        if not materia:
            raise ValueError("A matéria não pode estar vazia.")
        if prioridade not in VALID_PRIORITIES:
            raise ValueError("A prioridade deve ser: baixa, media ou alta.")
        self._validate_date(prazo)

        tasks = self._load_tasks()
        new_task = Task(
            id=self._next_id(tasks),
            titulo=titulo,
            materia=materia,
            prazo=prazo,
            prioridade=prioridade,
        )
        tasks.append(new_task)
        self._save_tasks(tasks)
        return new_task

    def list_tasks(self, status: str | None = None) -> list[Task]:
        if status is not None:
            status = status.strip().lower()
            if status not in VALID_STATUS:
                raise ValueError("O status deve ser: pendente ou concluida.")

        tasks = self._load_tasks()
        if status is None:
            return tasks
        return [task for task in tasks if task.status == status]

    def complete_task(self, task_id: int) -> Task:
        tasks = self._load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.status = "concluida"
                self._save_tasks(tasks)
                return task
        raise ValueError("Tarefa não encontrada.")

    def remove_task(self, task_id: int) -> None:
        tasks = self._load_tasks()
        remaining_tasks = [task for task in tasks if task.id != task_id]
        if len(remaining_tasks) == len(tasks):
            raise ValueError("Tarefa não encontrada.")
        self._save_tasks(remaining_tasks)

    def summary(self) -> dict[str, int]:
        tasks = self._load_tasks()
        return {
            "total": len(tasks),
            "pendentes": sum(task.status == "pendente" for task in tasks),
            "concluidas": sum(task.status == "concluida" for task in tasks),
            "alta_prioridade": sum(task.prioridade == "alta" for task in tasks),
        }

    def _load_tasks(self) -> list[Task]:
        raw_data = self.storage.load()
        return [Task(**task) for task in raw_data]

    def _save_tasks(self, tasks: Iterable[Task]) -> None:
        self.storage.save([asdict(task) for task in tasks])

    @staticmethod
    def _next_id(tasks: list[Task]) -> int:
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    @staticmethod
    def _validate_date(prazo: str) -> None:
        try:
            datetime.strptime(prazo, DATE_FORMAT)
        except ValueError as error:
            raise ValueError("O prazo deve estar no formato YYYY-MM-DD.") from error
