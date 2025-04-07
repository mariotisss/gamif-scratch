from rest_framework.routers import DefaultRouter
from .views import MissionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', MissionViewSet, basename='missions')

urlpatterns = [
    path('', include(router.urls)),
]