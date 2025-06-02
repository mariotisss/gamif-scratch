from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, UserTeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'user-teams', UserTeamViewSet, basename='userteam')

urlpatterns = [
    path('', include(router.urls)),
]
