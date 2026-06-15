import requests
import streamlit as st

st.set_page_config(page_title="StudyFlow", page_icon="📚")
st.title("📚 StudyFlow CLI")
st.caption("Organize sua rotina acadêmica.")
st.markdown("---")
st.markdown("### 💬 Frase motivacional")

if "frase" not in st.session_state:
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=10)
        d = r.json()
        st.session_state.frase = f'"{d[0]["q"]}" — {d[0]["a"]}'
    except Exception:
        st.session_state.frase = "Estude sempre."

if st.button("🔄 Nova frase"):
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=10)
        d = r.json()
        st.session_state.frase = f'"{d[0]["q"]}" — {d[0]["a"]}'
    except Exception:
        pass

st.info(st.session_state.frase)
st.markdown("---")
st.write("Desenvolvido por Lucas Ferreira de Sousa e Arthur Amaral · BootCamp 2026")
