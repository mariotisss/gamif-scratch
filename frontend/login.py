# frontend/login.py
import streamlit as st
import re
from api_client import login_user, register_user

def login_form():
    st.title("🔐 Iniciar sesión")

    if "show_register" not in st.session_state:
        st.session_state["show_register"] = False

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state["show_register"]:
            st.subheader("📝 Crear cuenta")

            with st.form("register_form"):
                username = st.text_input("Nuevo usuario")
                email = st.text_input("Nuevo email")
                password = st.text_input("Nueva contraseña", type="password")
                st.markdown(
                    """
                    **Requisitos de contraseña:**
                    - Mínimo 6 caracteres  
                    - Debe contener **letras** y **números**
                    """
                )
                submitted = st.form_submit_button("Registrarme")

                if submitted:
                    if len(password) < 6:
                        st.warning("La contraseña debe tener al menos 6 caracteres.")
                    elif not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
                        st.warning("La contraseña debe contener letras y números.")
                    else:
                        result = register_user(username, email, password)
                        if "success" in result:
                            st.success("✅ Cuenta creada correctamente. Ahora inicia sesión.")
                            st.session_state["show_register"] = False
                        else:
                            st.error(result["error"])

            if st.button("Volver al login"):
                st.session_state["show_register"] = False

        else:
            st.subheader("👤 Login")

            with st.form("login_form"):
                username = st.text_input("Usuario")
                password = st.text_input("Contraseña", type="password")
                submitted = st.form_submit_button("Acceder")

                if submitted:
                    result = login_user(username, password)
                    if "access" in result:
                        st.session_state["access_token"] = result["access"]
                        st.session_state["logged_in"] = True
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")

            if st.button("No tengo cuenta, registrarme"):
                st.session_state["show_register"] = True
