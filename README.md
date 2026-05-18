# StudyFlow CLI

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Version](https://img.shields.io/badge/version-1.1.0-success)
![CI](https://github.com/Lu5ousa/studyflow-cli/actions/workflows/ci.yml/badge.svg)

🌐 **Deploy:** https://studyflow-cli-aoqortnccutdi9orjodtxe.streamlit.app

Aplicação CLI criada para ajudar estudantes com dificuldade de rotina, organização e acompanhamento de tarefas acadêmicas.

## 1. Problema real
Muitos estudantes têm dificuldade para organizar o que precisam estudar, controlar prazos e manter constância. Isso causa atrasos, acúmulo de atividades e queda no rendimento acadêmico.

## 2. Proposta da solução
O **StudyFlow CLI** oferece uma forma simples de cadastrar, listar, concluir e remover tarefas de estudo diretamente no terminal, além de buscar frases motivacionais via API pública.

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
- resumo geral das tarefas;
- busca de citação motivacional via API pública (ZenQuotes).

## 5. Tecnologias utilizadas
- Python 3.11+
- `argparse` para interface CLI
- JSON para persistência dos dados
- `requests` para consumo de API REST externa
- ZenQuotes API para citações motivacionais
- `pytest` para testes automatizados
- `ruff` para linting/análise estática
- GitHub Actions para Integração Contínua (CI)
- Streamlit para interface web pública

## 6. Estrutura do projeto
```text