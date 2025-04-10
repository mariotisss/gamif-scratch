from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeViewSet, RewardViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet)
router.register(r'user-badges', UserBadgeViewSet, basename='userbadge')
router.register(r'rewards', RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]