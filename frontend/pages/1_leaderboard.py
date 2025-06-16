# frontend/pages/1_Leaderboard.py
import streamlit as st
from api_client import get_leaderboard

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()


st.title("🏆 Leaderboard")

limit = st.slider("Número de jugadores a mostrar", min_value=5, max_value=50, value=10)
data = get_leaderboard(limit=limit)

if "error" in data:
    st.error(data["error"])
else:
    for i, user in enumerate(data, start=1):
        st.write(f"{i}. **{user['username']}** — {user['xp']} XP")
