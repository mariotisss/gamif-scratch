from django.urls import path
from .views import LeaderboardView

urlpatterns = [
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]


# Para peticiones al endpoint del leaderboard:
    # GET /api/leaderboard/
    # GET /api/leaderboard/?limit=5
    # GET /api/leaderboard/?team=3
