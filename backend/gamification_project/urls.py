"""
URL configuration for gamification_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # App de users
    path('api/missions/', include('missions.urls')),  # App de missions
    path('api/', include('badges.urls')),  # App de badges
    path('api/', include('teams.urls')), # App de teams
    path('api/', include('analytics.urls')),  # App de analytics
    
    path('accounts/', include('allauth.urls')), # URLs de autenticación de allauth

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
