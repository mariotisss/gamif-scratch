# frontend/components/sidebar.py
import streamlit as st
from api_client import get_user_profile

def show_sidebar():

    # Datos del usuario logueado
    if "access_token" in st.session_state:
        profile = get_user_profile(st.session_state["access_token"])
        if "error" not in profile:
            st.sidebar.title("📋 Inventario")
            st.sidebar.markdown(f"👤  **{profile['username']}**")
            st.sidebar.markdown(f"⭐  **Nivel**: {profile['level']}")
            st.sidebar.markdown(f"⚡  **XP**: {profile['xp']}")
            st.sidebar.markdown(f"🎖️  **Badges**: {profile.get('badges', 0)}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

