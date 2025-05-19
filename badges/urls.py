from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeViewSet, RewardViewSet, AssignBadgeView

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badges')  # Basename 'badges' importante
router.register(r'user-badges', UserBadgeViewSet, basename='userbadge')
router.register(r'rewards', RewardViewSet)

urlpatterns = [
    # Tuve que modificar el orden de las rutas para que no choque con la de badges
    # Si no, al hacer un post a badges/assign/ en el test me tiraba un 405
    path('badges/assign/', AssignBadgeView.as_view(), name='assign_badge'),  # Ruta para asignar badge
    path('', include(router.urls)),
]
