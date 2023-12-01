from rest_framework.routers import SimpleRouter
from .views import FoodTruckViewSet

app_name = 'finder'

router = SimpleRouter()
router.register(r'food-truck', FoodTruckViewSet, basename='food-truck')
