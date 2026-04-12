# StudyFlow CLI

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Version](https://img.shields.io/badge/version-1.0.0-success)
![CI](https://github.com/Lu5ousa/studyflow-cli/actions/workflows/ci.yml/badge.svg)

Aplicação CLI criada para ajudar estudantes com dificuldade de rotina, organização e acompanhamento de tarefas acadêmicas.

## 1. Problema real
Muitos estudantes têm dificuldade para organizar o que precisam estudar, controlar prazos e manter constância. Isso causa atrasos, acúmulo de atividades e queda no rendimento acadêmico.

## 2. Proposta da solução
O **StudyFlow CLI** oferece uma forma simples de cadastrar, listar, concluir e remover tarefas de estudo diretamente no terminal. A proposta é reduzir a desorganização e facilitar o acompanhamento da rotina de estudos com uma ferramenta leve, prática e reproduzível.

## 3. Público-alvo
- estudantes do ensino médio, técnico e superior;
- pessoas com dificuldade de rotina ou organização acadêmica;
- usuários que preferem ferramentas simples em linha de comando.

## 4. Funcionalidades principais
- cadastro de tarefas com título, matéria, prazo e prioridade;
- listagem de tarefas;
- filtro por status (`pendente` ou `concluida`);
- conclusão de tarefa por ID;
- remoção de tarefa por ID;
- resumo geral das tarefas.

## 5. Tecnologias utilizadas
- Python 3.11+
- `argparse` para interface CLI
- JSON para persistência dos dados
- `pytest` para testes automatizados
- `ruff` para linting/análise estática
- GitHub Actions para Integração Contínua (CI)

## 6. Estrutura do projeto
```text
studyflow-cli/
├── .github/workflows/ci.yml
├── src/studyflow/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   └── storage.py
├── tests/test_app.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## 7. Instalação
```bash
git clone https://github.com/Lu5ousa/studyflow-cli.git
cd studyflow-cli
python -m venv .venv
```

### Ativar ambiente virtual
**Windows PowerShell**
```bash
.venv\Scripts\Activate.ps1
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### Instalar dependências
```bash
pip install -e .[dev]
```

## 8. Execução da aplicação
### Adicionar uma tarefa
```bash
python -m studyflow add --titulo "Estudar GitHub Actions" --materia "Bootcamp" --prazo 2026-04-20 --prioridade alta
```

### Listar tarefas
```bash
python -m studyflow list
```

### Filtrar por status
```bash
python -m studyflow list --status pendente
```

### Concluir uma tarefa
```bash
python -m studyflow complete 1
```

### Remover uma tarefa
```bash
python -m studyflow remove 1
```

### Exibir resumo
```bash
python -m studyflow summary
```

## 9. Exemplo de uso
```bash
$ python -m studyflow add --titulo "Revisar Python" --materia "Bootcamp" --prazo 2026-04-20 --prioridade alta
Tarefa adicionada com sucesso: #1 - Revisar Python

$ python -m studyflow list
#1 | Revisar Python | Bootcamp | 2026-04-20 | alta | pendente

$ python -m studyflow summary
Resumo do StudyFlow
- Total de tarefas: 1
- Pendentes: 1
- Concluídas: 0
- Alta prioridade: 1
```

## 10. Testes automatizados
```bash
pytest
```

## 11. Linting / análise estática
```bash
ruff check .
```

## 12. Versionamento semântico
Versão atual: **1.0.0**

## 13. Autor
**Lucas Ferreira de Sousa**

## 14. Repositório público
Projeto pensado para ser publicado em:
`https://github.com/Lu5ousa/studyflow-cli`

> Caso você crie o repositório com outro nome, atualize o link acima e a badge de CI.
