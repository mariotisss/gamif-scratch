# frontend/api_client.py
import httpx

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
    

def read_notification(notification_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.patch(
            f"{BASE_URL}/notifications/{notification_id}/",
            json={"read": True},
            headers=headers
        )
        response.raise_for_status()
        return True
    except httpx.HTTPError:
        return False
