from django.urls import path
from .views import LeaderboardView, NotificationViewSet

urlpatterns = [
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notification'),
]


# Para peticiones al endpoint del leaderboard:
    # GET /api/leaderboard/  (ranking global)
    # GET /api/leaderboard/?limit=5
    # GET /api/leaderboard/?team=3  ( ranking del equipo 3)
    # GET /api/leaderboard/?period=week  (ranking de los últimos 7 días)
    # GET /api/leaderboard/?team=3&period=month&limit=5  (ranking de los últimos 30 días, solo del equipo 3)
