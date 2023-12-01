from rest_framework.routers import APIRootView, DefaultRouter

# from .users.urls import router as users_router
from .finder.urls import router as finder_router


class DjangoFoodTruck(APIRootView):
    """
    Project Description.
    """
    pass


class DocumentedRouter(DefaultRouter):
    APIRootView = DjangoFoodTruck


router = DocumentedRouter()
# router.registry.extend(users_router.registry)
router.registry.extend(finder_router.registry)