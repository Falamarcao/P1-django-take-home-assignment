from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework_gis.filters import DistanceToPointOrderingFilter
from rest_framework_gis.pagination import GeoJsonPagination

from .serializers import FoodTruckSerializer
from .models import FoodTruck


class CustomGeoJsonPagination(GeoJsonPagination):
    page_size_query_param = 'limit'
    max_page_size = 100

class FoodTruckViewSet(ReadOnlyModelViewSet):
    """
    A read-only API endpoint that allows list and query food truck data.
    
    e.g. http://localhost:8000/api/v1/food-truck/?dist=30&point=-122.39015723961076,37.72441324329633&limit=5
    
    Ordered by distance to a given point, from the nearest to the most distant point.
    
    parameters:
    dist = 30 meters
    point = -122.39015723961076 longitude (lng), 37.72441324329633 latitude (lat).
    """
    
    # permission_classes = [] 
    queryset = FoodTruck.objects.all()
    pagination_class = CustomGeoJsonPagination
    serializer_class = FoodTruckSerializer
    distance_filter_field = 'location'
    filter_backends = (DistanceToPointOrderingFilter,)
    