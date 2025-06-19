import streamlit as st
from login import login_form
from datetime import datetime, timezone
from components.sidebar import show_sidebar
from api_client import get_user_missions, complete_mission

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

show_sidebar()

st.title("🎯 Misiones")

missions = get_user_missions(st.session_state["access_token"])

if "error" in missions:
    st.error(missions["error"])
else:
    # Clasificar misiones
    available = [m for m in missions if m["status"] == "available"]
    completed = [m for m in missions if m["status"] == "completed"]
    expired = [m for m in missions if m["status"] == "expired"]

    # Estilos visuales para tarjetas
    def render_mission(mission, color, status=None):
        expires_at = mission.get("expires_at")
        expires_html = ""
        mission_type = mission.get("type")

        if expires_at:
            try:
                dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                days_left = (dt - now).days
                expires_html = f"""<div style="text-align: right; font-size: 0.85rem; color: #aaa;">🕓 Expira el {dt.strftime('%d/%m/%Y')}</div>"""
                if status == "expired":
                    expires_html += """<div style="text-align: right; font-size: 0.85rem; color: #f55;">⛔ Esta misión ha expirado</div>"""
                elif days_left <= 3 and days_left >= 0:
                    expires_html += f"""<div style="text-align: right; font-size: 0.85rem; color: orange;">⚠️ Caduca en {days_left} día{'s' if days_left != 1 else ''}</div>"""
            except Exception:
                expires_html = ""

        # Muestra primero la tarjeta de misión
        st.markdown(f"""
            <div style="
                border: 1px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 8px;
                background-color: rgba(255,255,255,0.03);
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <b>{mission['title']}</b><br>
                    <small>{mission['description']}</small><br>
                    <small>🎁 Recompensa: {mission['xp_reward']} XP</small>
                </div>
                {f'<div>{expires_html}</div>' if expires_html else ''}
            </div>
        """, unsafe_allow_html=True)

        # Luego el botón, debajo del bloque
        if status == "available" and mission_type == "manual":
            if st.button(f"✅ Completar misión", key=f"complete_{mission['id']}"):
                try:
                    response = complete_mission(st.session_state["access_token"], mission["id"])
                    if "error" in response:
                        st.error(f"Error al completar la misión: {mission['title']}. Detalles: {response['error']}")
                    else:
                        st.success(f"Misión completada: {mission['title']} 🎉")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error al completar la misión: {mission['title']}. Detalles: {str(e)}")



    # Disponibles
    if available:
        st.subheader("🟢 Disponibles")
        for m in available:
            render_mission(m, "#3fb950", status="available")
    else:
        st.info("No tienes misiones disponibles ahora mismo.")

    # Completadas
    if completed:
        st.subheader("🔵 Completadas")
        for m in completed:
            render_mission(m, "#58a6ff", status="completed")

    # Expiradas
    if expired:
        st.subheader("⛔ Caducadas")
        for m in expired:
            render_mission(m, "#c32f27", status="expired")
