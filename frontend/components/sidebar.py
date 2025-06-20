import streamlit as st
from api_client import get_user_profile, get_user_badges

def user_level(xp, base=100, exponent=1.5):
    level = 1
    while xp >= base * (level ** exponent):
        level += 1
    return level

def next_level_xp(xp, base=100, exponent=1.5):
    level = user_level(xp, base, exponent)
    return int(base * (level ** exponent))

def show_sidebar():
    if "access_token" in st.session_state:
        profile = get_user_profile(st.session_state["access_token"])
        if "error" not in profile:
            username = profile.get("username", "usuario")
            xp = profile.get("xp", 0)
            level = profile.get("level") or user_level(xp)
            xp_needed = next_level_xp(xp)

            st.sidebar.title("📋 Inventario")
            st.sidebar.markdown(f"👤 **{username}**")
            st.sidebar.markdown(f"⭐ **Nivel**: {level}")
            st.sidebar.markdown(f"⚡ **XP**: {xp} / {xp_needed}")

            # Badges obtenidos reales
            user_badges, _ = get_user_badges(st.session_state["access_token"])
            unlocked_count = len([b for b in user_badges if b.get("awarded_at")])
            st.sidebar.markdown(f"🎖️ **Badges**: {unlocked_count}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()
