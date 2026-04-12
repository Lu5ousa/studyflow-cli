from __future__ import annotations

import argparse
from pathlib import Path

from studyflow import __version__
from studyflow.app import StudyFlowApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="studyflow",
        description="Organizador de estudos em linha de comando.",
    )
    parser.add_argument(
        "--data-file",
        default="data/study_tasks.json",
        help="Caminho do arquivo JSON usado para armazenar as tarefas.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"studyflow-cli {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Adiciona uma nova tarefa de estudo.")
    add_parser.add_argument("--titulo", required=True, help="Título da tarefa.")
    add_parser.add_argument("--materia", required=True, help="Matéria relacionada.")
    add_parser.add_argument("--prazo", required=True, help="Prazo no formato YYYY-MM-DD.")
    add_parser.add_argument(
        "--prioridade",
        required=True,
        choices=["baixa", "media", "alta"],
        help="Prioridade da tarefa.",
    )

    list_parser = subparsers.add_parser("list", help="Lista as tarefas cadastradas.")
    list_parser.add_argument(
        "--status",
        choices=["pendente", "concluida"],
        help="Filtra por status.",
    )

    complete_parser = subparsers.add_parser("complete", help="Marca uma tarefa como concluída.")
    complete_parser.add_argument("id", type=int, help="ID da tarefa.")

    remove_parser = subparsers.add_parser("remove", help="Remove uma tarefa.")
    remove_parser.add_argument("id", type=int, help="ID da tarefa.")

    subparsers.add_parser("summary", help="Exibe um resumo das tarefas.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    app = StudyFlowApp(Path(args.data_file))

    try:
        if args.command == "add":
            task = app.add_task(args.titulo, args.materia, args.prazo, args.prioridade)
            print(f"Tarefa adicionada com sucesso: #{task.id} - {task.titulo}")
            return 0

        if args.command == "list":
            tasks = app.list_tasks(status=args.status)
            if not tasks:
                print("Nenhuma tarefa encontrada.")
                return 0

            for task in tasks:
                print(
                    f"#{task.id} | {task.titulo} | {task.materia} | {task.prazo} | "
                    f"{task.prioridade} | {task.status}"
                )
            return 0

        if args.command == "complete":
            task = app.complete_task(args.id)
            print(f"Tarefa concluída: #{task.id} - {task.titulo}")
            return 0

        if args.command == "remove":
            app.remove_task(args.id)
            print(f"Tarefa removida com sucesso: #{args.id}")
            return 0

        if args.command == "summary":
            summary = app.summary()
            print("Resumo do StudyFlow")
            print(f"- Total de tarefas: {summary['total']}")
            print(f"- Pendentes: {summary['pendentes']}")
            print(f"- Concluídas: {summary['concluidas']}")
            print(f"- Alta prioridade: {summary['alta_prioridade']}")
            return 0

    except ValueError as error:
        print(f"Erro: {error}")
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
