import streamlit as st
from datetime import datetime
from login import login_form
from components.sidebar import show_sidebar
from api_client import get_user_badges

# --- Verificar login ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

# --- Mostrar sidebar ---
show_sidebar()

# --- Funciones auxiliares ---
def format_date(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", ""))
        return dt.strftime("%d/%m/%Y")
    except:
        return ""

def badge_component(badge, awarded=False, awarded_at=None):
    image_url = badge["icon"] or "https://via.placeholder.com/100x100?text=Badge"
    name = badge["name"]
    date = format_date(awarded_at) if awarded else "Locked"
    style = "filter: grayscale(100%) opacity(0.4);" if not awarded else ""

    return f"""
        <div style="min-width: 120px; text-align: center; margin: 10px;">
            <img src="{image_url}" width="100" style="{style}"/>
            <div style="font-weight: bold; margin-top: 5px;">{name}</div>
            <div style="font-size: 0.85em;">{date}</div>
        </div>
    """

def render_badge_scroll(badges_html_list):
    row_html = "".join(badges_html_list)
    container = f"""
        <div style="
            display: flex;
            overflow-x: auto;
            padding: 10px;
            gap: 10px;
        ">
            {row_html}
        </div>
    """
    st.markdown(container, unsafe_allow_html=True)

# --- Contenido de la página ---
st.title("🎖️ Logros / Insignias")

# Obtener los badges del usuario y todos los badges disponibles
user_badges_raw, all_badges = get_user_badges(st.session_state["access_token"])

# Obtenidos
awarded_badge_ids = [ub["badge"]["id"] for ub in user_badges_raw]
awarded_badges_html = [
    badge_component(ub["badge"], awarded=True, awarded_at=ub["awarded_at"])
    for ub in user_badges_raw
]

# No obtenidos
locked_badges_html = [
    badge_component(badge, awarded=False)
    for badge in all_badges
    if badge["id"] not in awarded_badge_ids
]

# --- Renderizado ---
st.subheader("✅ Obtenidos")
render_badge_scroll(awarded_badges_html)

st.markdown("<hr style='border: 0.5px solid #555;'>", unsafe_allow_html=True)

st.subheader("🔒 Bloqueados")
render_badge_scroll(locked_badges_html)
