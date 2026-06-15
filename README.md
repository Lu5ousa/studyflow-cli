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
- **Supabase (PostgreSQL)** para persistência de dados em nuvem
- `supabase-py` para integração com o banco de dados
- `requests` para consumo de API REST externa
- ZenQuotes API para citações motivacionais
- `pytest` para testes automatizados
- `ruff` para linting/análise estática
- GitHub Actions para Integração Contínua (CI)
- Streamlit para interface web pública

## 6. Estrutura do projeto
```text
studyflow-cli/
├── src/studyflow/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api.py
│   ├── app.py
│   └── database.py       ← integração Supabase
├── tests/
│   ├── test_app.py
│   └── test_integration.py
├── streamlit_app.py
├── pyproject.toml
└── .env.example
```

## 7. Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/Lu5ousa/studyflow-cli.git
cd studyflow-cli

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale as dependências
pip install -e ".[dev]"

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves do Supabase

# Rode os testes
pytest

# Rode o linter
ruff check .

# Inicie a interface web
streamlit run streamlit_app.py
```

## 8. Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_KEY` | Chave anon/public do Supabase |

## 👥 Equipe

| Nome | RA |
|---|---|
| Lucas Ferreira de Sousa | 22510970 |
| Arthur Amaral Dos Santos | 22506429 |

---

BootCamp — Etapa 3: Trabalho em Equipe, Banco de Dados e Code Review