# frontend/api_client.py
import httpx
import streamlit as st

BASE_URL = "http://127.0.0.1:8000/api"  # Indicar aqui la URL de la API


def register_user(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    try:
        response = httpx.post(f"{BASE_URL}/users/register/", json=payload)
        response.raise_for_status()
        return {"success": True}
    except httpx.HTTPError as e:
        return {"error": str(e)}


def login_user(username, password):
    payload = {"username": username, "password": password}
    try:
        response = httpx.post(f"{BASE_URL}/users/login/", data=payload)
        response.raise_for_status()
        return response.json()  # {'access': '...', 'refresh': '...'}
    except httpx.HTTPError as e:
        return {"error": str(e)}


def get_user_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.get(f"{BASE_URL}/users/me/", headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}


def get_leaderboard(limit=10):
    try:
        response = httpx.get(f"{BASE_URL}/leaderboard/?limit={limit}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}
    

def get_user_mission_stats(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.get(f"{BASE_URL}/missions/mission-stats/", headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}


def get_user_notifications(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.get(f"{BASE_URL}/notifications/", headers=headers)
        response.raise_for_status()
        return response.json()  # Lista completa de objetos con 'id', 'message', etc.
    except httpx.HTTPError as e:
        return {"error": str(e)}
    

def delete_notification(notification_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.delete(
            f"{BASE_URL}/notifications/{notification_id}/",
            headers=headers
        )
        response.raise_for_status()
        return True
    except httpx.HTTPError:
        return False


def get_user_missions(token):
    headers = {"Authorization": f"Bearer " + token}
    try:
        response = httpx.get(f"{BASE_URL}/missions/user/", headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}


def complete_mission(token, mission_id):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"mission_id": mission_id}
    try:
        response = httpx.post(f"{BASE_URL}/missions/complete/", json=payload, headers=headers)
        response.raise_for_status()
        return {"success": True}
    except httpx.HTTPError as e:
        return {"error": str(e)}


def get_user_badges(token):
    headers = {"Authorization": f"Bearer " + token}
    with httpx.Client() as client:
            user_badges_response = client.get(f"{BASE_URL}/user-badges/", headers=headers)
            all_badges_response = client.get(f"{BASE_URL}/badges/", headers=headers)

            user_badges = user_badges_response.json()
            all_badges = all_badges_response.json()

    return user_badges, all_badges


def get_teams():
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/teams/", headers=headers)
        return response.json() if response.status_code == 200 else []

def get_user_teams():
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/user-teams/", headers=headers)
        return [ut["team"] for ut in response.json()] if response.status_code == 200 else []

def create_team(name, description):
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "description": description}
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/teams/", headers=headers, json=data)
        return response.status_code == 201


def get_team_detail(team_id):
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/teams/{team_id}/", headers=headers)
        return response.json()

def get_team_members(team_id):
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/teams/{team_id}/members/", headers=headers)
            if response.status_code == 200:
                return [ut["user"] for ut in response.json()]
            return []

def join_team(team_id):
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"team": team_id}  # el usuario lo fuerza el backend con perform_create()
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/user-teams/", headers=headers, json=data)
        return response.status_code == 201


def get_team_ranking():
    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/teams/ranking/", headers=headers)
        return response.json() if response.status_code == 200 else []
