"""Interface web do StudyFlow CLI via Streamlit."""
from __future__ import annotations

import streamlit as st

from studyflow.api import fetch_motivational_quote
from studyflow.app import StudyFlowApp

# ── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyFlow",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease;
}
.card:hover { transform: translateY(-2px); }

.badge-alta   { background:#ef4444; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-media  { background:#f59e0b; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-baixa  { background:#10b981; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-concluida { background:#6366f1; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-pendente  { background:#64748b; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }

.metric-card {
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}
.metric-num { font-size: 2.2rem; font-weight:700; color:#a78bfa; }
.metric-label { font-size: 0.85rem; color:#94a3b8; }

.quote-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    border-left: 4px solid #818cf8;
    border-radius: 12px;
    padding: 18px 22px;
    font-style: italic;
    color: #e2e8f0;
    margin: 16px 0;
}

h1, h2, h3 { color: #f1f5f9 !important; }
label, .stSelectbox label, .stTextInput label { color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)

# ── App ──────────────────────────────────────────────────────────────────────
app = StudyFlowApp()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 StudyFlow")
    st.markdown("---")
    page = st.radio(
        "Navegação",
        ["🏠 Dashboard", "➕ Nova Tarefa", "✅ Gerenciar Tarefas"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    st.markdown("### 💡 Frase do Dia")
    if st.button("🔄 Nova frase", use_container_width=True):
        st.session_state["quote"] = fetch_motivational_quote()

    if "quote" not in st.session_state:
        try:
            st.session_state["quote"] = fetch_motivational_quote()
        except Exception:
            st.session_state["quote"] = {"quote": "Foco e disciplina constroem o futuro.", "author": "StudyFlow"}

    q = st.session_state["quote"]
    st.markdown(f"""
    <div class="quote-box">
        "{q['quote']}"<br><br>
        <strong>— {q['author']}</strong>
    </div>
    """, unsafe_allow_html=True)

# ── Dashboard ─────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("# 🎓 StudyFlow — Seu Organizador de Estudos")
    st.markdown("---")

    try:
        summary = app.summary()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="metric-card"><div class="metric-num">{summary['total']}</div><div class="metric-label">Total de Tarefas</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-card"><div class="metric-num">{summary['pendentes']}</div><div class="metric-label">Pendentes</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-card"><div class="metric-num">{summary['concluidas']}</div><div class="metric-label">Concluídas</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-card"><div class="metric-num">{summary['alta_prioridade']}</div><div class="metric-label">Alta Prioridade</div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Tarefas Recentes")
        tasks = app.list_tasks()
        if not tasks:
            st.info("Nenhuma tarefa cadastrada ainda. Crie a primeira! ➕")
        else:
            for task in tasks[:5]:
                prioridade_class = f"badge-{task.prioridade}"
                status_class = f"badge-{task.status}"
                st.markdown(f"""
                <div class="card">
                    <strong style="color:#f1f5f9">#{task.id} — {task.titulo}</strong>
                    &nbsp;&nbsp;
                    <span class="{prioridade_class}">{task.prioridade}</span>
                    &nbsp;
                    <span class="{status_class}">{task.status}</span>
                    <br>
                    <small style="color:#94a3b8">📘 {task.materia} &nbsp;|&nbsp; 📅 {task.prazo}</small>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")

# ── Nova Tarefa ───────────────────────────────────────────────────────────────
elif page == "➕ Nova Tarefa":
    st.markdown("# ➕ Cadastrar Nova Tarefa")
    st.markdown("---")

    with st.form("form_nova_tarefa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            titulo = st.text_input("📝 Título da Tarefa", placeholder="Ex: Revisar capítulo 5 de Cálculo")
            materia = st.text_input("📘 Matéria", placeholder="Ex: Cálculo I")
        with col2:
            prazo = st.date_input("📅 Prazo")
            prioridade = st.selectbox("⚡ Prioridade", ["alta", "media", "baixa"])

        submitted = st.form_submit_button("✅ Criar Tarefa", use_container_width=True, type="primary")
        if submitted:
            if not titulo.strip():
                st.error("O título não pode estar vazio!")
            else:
                try:
                    task = app.add_task(
                        titulo=titulo,
                        materia=materia,
                        prazo=str(prazo),
                        prioridade=prioridade,
                    )
                    st.success(f"✅ Tarefa #{task.id} **{task.titulo}** criada com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro: {e}")

# ── Gerenciar Tarefas ─────────────────────────────────────────────────────────
elif page == "✅ Gerenciar Tarefas":
    st.markdown("# ✅ Gerenciar Tarefas")
    st.markdown("---")

    col_filter, _ = st.columns([1, 3])
    with col_filter:
        filtro = st.selectbox("Filtrar por status", ["todas", "pendente", "concluida"])

    try:
        tasks = app.list_tasks(status=None if filtro == "todas" else filtro)

        if not tasks:
            st.info("Nenhuma tarefa encontrada com esse filtro.")
        else:
            for task in tasks:
                prioridade_class = f"badge-{task.prioridade}"
                status_class = f"badge-{task.status}"
                c1, c2, c3 = st.columns([6, 1, 1])
                with c1:
                    st.markdown(f"""
                    <div class="card">
                        <strong style="color:#f1f5f9">#{task.id} — {task.titulo}</strong>
                        &nbsp;&nbsp;
                        <span class="{prioridade_class}">{task.prioridade}</span>
                        &nbsp;
                        <span class="{status_class}">{task.status}</span>
                        <br>
                        <small style="color:#94a3b8">📘 {task.materia} &nbsp;|&nbsp; 📅 {task.prazo}</small>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if task.status == "pendente":
                        if st.button("✅", key=f"done_{task.id}", help="Marcar como concluída"):
                            app.complete_task(task.id)
                            st.rerun()
                with c3:
                    if st.button("🗑️", key=f"del_{task.id}", help="Remover tarefa"):
                        app.remove_task(task.id)
                        st.rerun()
    except Exception as e:
        st.error(f"Erro ao carregar tarefas: {e}")
