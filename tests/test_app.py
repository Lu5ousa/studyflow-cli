from pathlib import Path

import pytest

from studyflow.app import StudyFlowApp


@pytest.fixture()
def app(tmp_path: Path) -> StudyFlowApp:
    return StudyFlowApp(tmp_path / "study_tasks.json")


def test_add_task_creates_valid_record(app: StudyFlowApp) -> None:
    task = app.add_task(
        titulo="Revisar lógica de programação",
        materia="Bootcamp",
        prazo="2026-04-20",
        prioridade="alta",
    )

    tasks = app.list_tasks()
    assert task.id == 1
    assert len(tasks) == 1
    assert tasks[0].titulo == "Revisar lógica de programação"
    assert tasks[0].status == "pendente"


def test_add_task_rejects_empty_title(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="título não pode estar vazio"):
        app.add_task(
            titulo="   ",
            materia="Matemática",
            prazo="2026-04-20",
            prioridade="media",
        )


def test_complete_task_updates_status(app: StudyFlowApp) -> None:
    app.add_task(
        titulo="Fazer exercícios de Python",
        materia="Programação",
        prazo="2026-04-21",
        prioridade="media",
    )

    task = app.complete_task(1)

    assert task.status == "concluida"
    assert app.summary()["concluidas"] == 1


def test_remove_nonexistent_task_raises_error(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="Tarefa não encontrada"):
        app.remove_task(99)


def test_invalid_date_format_is_rejected(app: StudyFlowApp) -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        app.add_task(
            titulo="Estudar testes",
            materia="Qualidade de Software",
            prazo="20-04-2026",
            prioridade="baixa",
        )
