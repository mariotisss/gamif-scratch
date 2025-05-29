from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaderboardView, NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]


# Para peticiones al endpoint del leaderboard:
    # GET /api/leaderboard/  (ranking global)
    # GET /api/leaderboard/?limit=5
    # GET /api/leaderboard/?team=3  ( ranking del equipo 3)
    # GET /api/leaderboard/?period=week  (ranking de los últimos 7 días)
    # GET /api/leaderboard/?team=3&period=month&limit=5  (ranking de los últimos 30 días, solo del equipo 3)
