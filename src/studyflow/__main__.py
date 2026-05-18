from __future__ import annotations

import argparse
from pathlib import Path

from studyflow import __version__
from studyflow.app import StudyFlowApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="studyflow", description="Organizador de estudos em linha de comando.")
    parser.add_argument("--data-file", default="data/study_tasks.json")
    parser.add_argument("--version", action="version", version=f"studyflow-cli {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Adiciona uma nova tarefa.")
    add_p.add_argument("--titulo", required=True)
    add_p.add_argument("--materia", required=True)
    add_p.add_argument("--prazo", required=True)
    add_p.add_argument("--prioridade", required=True, choices=["baixa", "media", "alta"])

    list_p = subparsers.add_parser("list", help="Lista as tarefas.")
    list_p.add_argument("--status", choices=["pendente", "concluida"])

    complete_p = subparsers.add_parser("complete", help="Conclui uma tarefa.")
    complete_p.add_argument("id", type=int)

    remove_p = subparsers.add_parser("remove", help="Remove uma tarefa.")
    remove_p.add_argument("id", type=int)

    subparsers.add_parser("summary", help="Resumo das tarefas.")
    subparsers.add_parser("quote", help="Exibe uma citação motivacional via API.")

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
                print(f"#{task.id} | {task.titulo} | {task.materia} | {task.prazo} | {task.prioridade} | {task.status}")
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
            s = app.summary()
            print("Resumo do StudyFlow")
            print(f"- Total de tarefas: {s['total']}")
            print(f"- Pendentes: {s['pendentes']}")
            print(f"- Concluídas: {s['concluidas']}")
            print(f"- Alta prioridade: {s['alta_prioridade']}")
            return 0
        if args.command == "quote":
            print("Buscando frase motivacional...")
            result = app.get_quote()
            print(f'\n💬 Frase do momento:\n   "{result["quote"]}"\n   — {result["author"]}\n')
            return 0
    except ValueError as error:
        print(f"Erro: {error}")
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())