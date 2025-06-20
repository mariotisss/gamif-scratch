import streamlit as st
from login import login_form
from components.sidebar import show_sidebar
from api_client import get_teams, get_user_teams, create_team, get_team_detail, get_team_members, join_team, get_team_ranking

# --- Verificar login ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form()
    st.stop()

# --- Mostrar sidebar ---
show_sidebar()

st.title("👥 Equipos")

# --- Crear nuevo equipo ---
with st.expander("➕ Crear un nuevo equipo"):
    with st.form("create_team_form"):
        name = st.text_input("Nombre del equipo")
        description = st.text_area("Descripción")
        submitted = st.form_submit_button("Crear equipo")

        if submitted and name:
            success = create_team(name, description)
            if success:
                st.success("Equipo creado correctamente. Recarga para verlo.")
                st.rerun()
            else:
                st.error("Error al crear el equipo.")

# --- Cargar datos de equipos ---
user_team_ids = get_user_teams()
all_teams = get_teams()

st.subheader("🌍 Equipos disponibles")

for team in all_teams:
    with st.expander(f"{team['name']} - {team['description']}"):
        team_details = get_team_detail(team["id"])
        members = get_team_members(team["id"])
        already_joined = team["id"] in user_team_ids

        st.markdown(f"📅 **Creado el:** `{team_details['created_at']}`")
        st.markdown(f"👥 **Miembros:** {team_details['member_count']}")
        st.markdown("🧑‍🤝‍🧑 **Lista de miembros:**")
        for username in members:
            st.markdown(f"- {username}")

        if not already_joined:
            if st.button("✅ Unirme a este equipo", key=f"join_{team['id']}"):
                success = join_team(team["id"])
                if success:
                    st.success("Te has unido correctamente al equipo.")
                    st.rerun()
                else:
                    st.error("Hubo un problema al intentar unirse.")
        else:
            st.info("Ya perteneces a este equipo.")


st.markdown("<hr style='border: 0.5px solid #555;'>", unsafe_allow_html=True)

st.subheader("📊 Ranking de equipos")

ranking = get_team_ranking()

for idx, team in enumerate(ranking, start=1):
    st.markdown(f"**{idx}. {team['name']}** — 🏆 Misiones completadas: {team['missions_completed']}")
