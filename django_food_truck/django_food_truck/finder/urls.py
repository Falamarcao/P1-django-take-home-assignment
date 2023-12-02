from django.urls import path

from rest_framework.routers import SimpleRouter
from .views import FoodTruckViewSet, MapView

app_name = 'finder'

urlpatterns = [
    path('map/', MapView.as_view(), name='map'),
]

router = SimpleRouter()
router.register(r'food-truck', FoodTruckViewSet, basename='food-truck')
