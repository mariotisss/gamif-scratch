import streamlit as st
import time
from login import login_form
from api_client import (
    get_leaderboard,
    get_user_mission_stats,
    get_user_profile,
    get_user_notifications,
    delete_notification
)
from components.sidebar import show_sidebar
import pandas as pd
import plotly.graph_objects as go



def show_toast(message):
    st.markdown(f"""
        <script>
        const toast = document.createElement("div");
        toast.textContent = "{message}";
        toast.style.position = "fixed";
        toast.style.bottom = "30px";
        toast.style.right = "30px";
        toast.style.background = "#333";
        toast.style.color = "white";
        toast.style.padding = "10px 20px";
        toast.style.borderRadius = "8px";
        toast.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
        toast.style.zIndex = "10000";
        toast.style.fontSize = "0.9rem";
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
        </script>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="Dashboard", page_icon="🎮", layout="wide")

# Protege acceso
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

# Sidebar persistente con navegación
show_sidebar()


# Estilos CSS
st.markdown("""
    <style>
        .notification-card {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 10px;
            font-size: 0.9rem;
        }
        .notification-text {
            flex: 1;
            color: white;
        }
        .notification-actions {
            margin-left: 10px;
        }
        .notification-btn {
            background: transparent;
            border: none;
            color: #ccc;
            cursor: pointer;
            font-size: 0.8rem;
            padding: 4px 6px;
            border-radius: 6px;
        }
        .notification-btn:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
    </style>
""", unsafe_allow_html=True)


# Título
st.title("🎮 Mi Panel de Actividad")

col1, col2 = st.columns([2, 1])

# 📈 Misiones completadas
with col1:
    with st.container():
        st.markdown("#### 📈 Misiones completadas", unsafe_allow_html=True)
        with st.expander(" ", expanded=True):
            stats = get_user_mission_stats(st.session_state["access_token"])
            if "error" not in stats:
                df = pd.DataFrame(stats).rename(columns={"date": "fecha", "completed": "completadas"})
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df["fecha"], y=df["completadas"],
                    mode='lines+markers', line_shape='spline'
                ))
                fig.update_layout(
                    title="", xaxis_title="Fecha", yaxis_title="Misiones",
                    margin=dict(l=0, r=0, t=10, b=10), height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos disponibles.")


# 📬 Notificaciones
with col1:
    with st.container():
        st.markdown("#### 📬 Notificaciones", unsafe_allow_html=True)
        with st.expander(" ", expanded=True):
            notifs = get_user_notifications(st.session_state["access_token"])

            if isinstance(notifs, list) and notifs:
                # Crear almacenamiento de notificaciones borradas (por ID)
                if "read_notifications" not in st.session_state:
                    st.session_state["read_notifications"] = set()

                with st.container():
                    st.markdown('<div style="max-height:300px; overflow-y:auto;">', unsafe_allow_html=True)

                    for notif in notifs:
                        notif_id = notif["id"]
                        if notif_id in st.session_state["read_notifications"]:
                            continue  # no mostrar si ya se ha borrado en esta sesión

                        col1_, col2_ = st.columns([9, 1])
                        with col1_:
                            st.markdown(f"""
                                <div class="notification-card">
                                    <div class="notification-text">
                                        {notif['message']}
                                    </div>
                            """, unsafe_allow_html=True)

                        with col2_:
                            if st.button("❌", key=f"delete_{notif_id}"):
                                from api_client import delete_notification
                                success = delete_notification(notif_id, st.session_state["access_token"])
                                if success:
                                    st.session_state["read_notifications"].add(notif_id)
                                    show_toast("Notificación eliminada")
                                    time.sleep(0.1)  # da tiempo a mostrar el toast
                                    st.rerun()  # método interno no documentado (no recomendado, pero funcional)
                                else:
                                    st.error("No se pudo eliminar la notificación.")
                            st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No tienes notificaciones aún.")



# 🏆 Leaderboard
with col2:
    with st.container():
        st.markdown("#### 🏆 Ranking (Top 10)", unsafe_allow_html=True)
        with st.expander(" ", expanded=True):
            leaderboard = get_leaderboard(limit=10)
            for i, user in enumerate(leaderboard, 1):
                st.markdown(f"{i}. **{user['username']}** — {user['xp']} XP")
