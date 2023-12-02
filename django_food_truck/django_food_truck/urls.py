"""
URL configuration for django_food_truck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import RedirectView

from .finder import urls as finder_urls

from .routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('finder/', include(finder_urls)),
    
    path('api/v1/', include(router.urls)),
    
    path('', RedirectView.as_view(url='http://localhost:8000/finder/map?dist=300&point=-122.39015723961076,37.72441324329633&limit=5', permanent=False), name='home'),
]
