import streamlit as st
from datetime import datetime
from login import login_form
from components.sidebar import show_sidebar
from api_client import get_user_badges

# Verificar si el usuario está logueado
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

# Mostrar sidebar con datos de usuario
show_sidebar()

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
    html = f"""
        <div style="text-align:center; margin:10px;">
            <img src="{image_url}" width="100" style="{style}"/>
            <div style="font-weight:bold;">{name}</div>
            <div style="font-size:0.85em;">{date}</div>
        </div>
    """
    return html

# --- Página principal ---
st.title("🎖️ Logros / Insignias")

user_badges_raw, all_badges = get_user_badges(st.session_state["access_token"]) # Obtener los badges del usuario y todos los badges disponibles

# Badges obtenidos
awarded_badge_ids = [ub["badge"]["id"] for ub in user_badges_raw]
awarded_badges = {
    ub["badge"]["id"]: badge_component(
        ub["badge"], awarded=True, awarded_at=ub["awarded_at"]
    ) for ub in user_badges_raw
}

# Badges no obtenidos
locked_badges = {
    b["id"]: badge_component(b, awarded=False)
    for b in all_badges if b["id"] not in awarded_badge_ids
}

# Renderizado en Streamlit
st.subheader("✅ Obtenidos")
cols = st.columns(len(awarded_badges) or 1)
for col, html in zip(cols, awarded_badges.values()):
    col.markdown(html, unsafe_allow_html=True)

st.subheader("🔒 Bloqueados")
cols = st.columns(len(locked_badges) or 1)
for col, html in zip(cols, locked_badges.values()):
    col.markdown(html, unsafe_allow_html=True)
