"""Testes unitários para StudyFlowApp com Supabase mockado."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from studyflow.app import StudyFlowApp
from studyflow.database import Task


def _make_task(**kwargs) -> Task:
    defaults = dict(id=1, titulo="Tarefa Teste", materia="Matéria", prazo="2026-04-20", prioridade="alta", status="pendente")
    defaults.update(kwargs)
    return Task(**defaults)


@pytest.fixture()
def app() -> StudyFlowApp:
    return StudyFlowApp()


# ── Testes de add_task ────────────────────────────────────────────────────────

def test_add_task_creates_valid_record(app: StudyFlowApp) -> None:
    task = _make_task(id=1, titulo="Revisar lógica de programação")
    with patch("studyflow.app.insert_task", return_value=task) as mock_insert:
        result = app.add_task(
            titulo="Revisar lógica de programação",
            materia="Bootcamp",
            prazo="2026-04-20",
            prioridade="alta",
        )
    mock_insert.assert_called_once_with("Revisar lógica de programação", "Bootcamp", "2026-04-20", "alta")
    assert result.id == 1
    assert result.titulo == "Revisar lógica de programação"
    assert result.status == "pendente"


def test_add_task_rejects_empty_title(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="título não pode estar vazio"):
        app.add_task(titulo="   ", materia="Matemática", prazo="2026-04-20", prioridade="media")


def test_add_task_rejects_invalid_date(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        app.add_task(titulo="Estudar testes", materia="QA", prazo="20-04-2026", prioridade="baixa")


def test_add_task_rejects_invalid_priority(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="Prioridade inválida"):
        app.add_task(titulo="Estudar", materia="QA", prazo="2026-04-20", prioridade="urgente")


# ── Testes de list_tasks ──────────────────────────────────────────────────────

def test_list_tasks_returns_all(app: StudyFlowApp) -> None:
    tasks = [_make_task(id=1), _make_task(id=2, status="concluida")]
    with patch("studyflow.app.load_tasks", return_value=tasks):
        result = app.list_tasks()
    assert len(result) == 2


def test_list_tasks_filters_by_status(app: StudyFlowApp) -> None:
    tasks = [_make_task(id=1, status="pendente"), _make_task(id=2, status="concluida")]
    with patch("studyflow.app.load_tasks", return_value=tasks):
        result = app.list_tasks(status="pendente")
    assert len(result) == 1
    assert result[0].status == "pendente"


# ── Testes de complete_task ───────────────────────────────────────────────────

def test_complete_task_updates_status(app: StudyFlowApp) -> None:
    task = _make_task(id=1, status="concluida")
    with patch("studyflow.app.update_task_status", return_value=task) as mock_update:
        result = app.complete_task(1)
    mock_update.assert_called_once_with(1, "concluida")
    assert result.status == "concluida"


def test_complete_task_raises_if_not_found(app: StudyFlowApp) -> None:
    with patch("studyflow.app.update_task_status", side_effect=ValueError("Tarefa não encontrada: #99")):
        with pytest.raises(ValueError, match="Tarefa não encontrada"):
            app.complete_task(99)


# ── Testes de remove_task ─────────────────────────────────────────────────────

def test_remove_task_calls_delete(app: StudyFlowApp) -> None:
    with patch("studyflow.app.delete_task") as mock_delete:
        app.remove_task(1)
    mock_delete.assert_called_once_with(1)


def test_remove_nonexistent_task_raises_error(app: StudyFlowApp) -> None:
    with patch("studyflow.app.delete_task", side_effect=ValueError("Tarefa não encontrada: #99")):
        with pytest.raises(ValueError, match="Tarefa não encontrada"):
            app.remove_task(99)


# ── Testes de summary ─────────────────────────────────────────────────────────

def test_summary_returns_correct_counts(app: StudyFlowApp) -> None:
    tasks = [
        _make_task(id=1, status="pendente", prioridade="alta"),
        _make_task(id=2, status="concluida", prioridade="media"),
        _make_task(id=3, status="pendente", prioridade="alta"),
    ]
    with patch("studyflow.app.load_tasks", return_value=tasks):
        s = app.summary()
    assert s["total"] == 3
    assert s["pendentes"] == 2
    assert s["concluidas"] == 1
    assert s["alta_prioridade"] == 2
