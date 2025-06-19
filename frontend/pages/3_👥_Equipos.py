import streamlit as st
from login import login_form
from components.sidebar import show_sidebar

# Verificar si el usuario está logueado
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

# Mostrar sidebar con datos de usuario
show_sidebar()

st.title("👥 Equipos")
st.markdown("Aquí se mostrarán los equipos...")