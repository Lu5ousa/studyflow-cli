"""Módulo de banco de dados do StudyFlow — integração com Supabase."""
from __future__ import annotations

import os
from dataclasses import dataclass

from supabase import Client, create_client

_TABLE = "tasks"


def _get_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)


@dataclass
class Task:
    id: int
    titulo: str
    materia: str
    prazo: str
    prioridade: str
    status: str = "pendente"


def load_tasks() -> list[Task]:
    """Retorna todas as tarefas do banco de dados."""
    client = _get_client()
    response = client.table(_TABLE).select("*").order("id").execute()
    return [Task(**row) for row in response.data]


def insert_task(titulo: str, materia: str, prazo: str, prioridade: str) -> Task:
    """Insere uma nova tarefa e retorna o objeto criado."""
    client = _get_client()
    payload = {
        "titulo": titulo,
        "materia": materia,
        "prazo": prazo,
        "prioridade": prioridade,
        "status": "pendente",
    }
    response = client.table(_TABLE).insert(payload).execute()
    return Task(**response.data[0])


def update_task_status(task_id: int, status: str) -> Task:
    """Atualiza o status de uma tarefa pelo ID."""
    client = _get_client()
    response = (
        client.table(_TABLE)
        .update({"status": status})
        .eq("id", task_id)
        .execute()
    )
    if not response.data:
        raise ValueError(f"Tarefa não encontrada: #{task_id}")
    return Task(**response.data[0])


def delete_task(task_id: int) -> None:
    """Remove uma tarefa pelo ID."""
    client = _get_client()
    response = client.table(_TABLE).delete().eq("id", task_id).execute()
    if not response.data:
        raise ValueError(f"Tarefa não encontrada: #{task_id}")
