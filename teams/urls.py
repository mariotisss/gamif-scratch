from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, UserTeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'user-teams', UserTeamViewSet, basename='user-teams')

urlpatterns = [
    path('', include(router.urls)),
]
