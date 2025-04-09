from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, CompleteMissionView

router = DefaultRouter()
router.register(r'', MissionViewSet, basename='missions')

urlpatterns = [
    path('complete/', CompleteMissionView.as_view(), name='complete_mission'),
    path('', include(router.urls)),
]