from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, CompleteMissionView, MissionStatsView, UserMissionListView

router = DefaultRouter()
router.register(r'', MissionViewSet, basename='missions')

urlpatterns = [
    path('complete/', CompleteMissionView.as_view(), name='complete_mission'),
    path("mission-stats/", MissionStatsView.as_view(), name="mission-stats"),
    path("missions/user/", UserMissionListView.as_view(), name="user-missions"),
    path('', include(router.urls)),
]