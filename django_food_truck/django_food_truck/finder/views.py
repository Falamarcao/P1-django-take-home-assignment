from django.views.generic import TemplateView

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import Collect
from django.contrib.gis.db.models.functions import Distance, Centroid

from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.renderers import JSONRenderer

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


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        # Initialize the context with super() to include any additional context data
        context = super().get_context_data(**kwargs)

        # Extract filtering parameters from the request
        distance, limit, point_str = self.request.GET.get('dist'), self.request.GET.get('limit'), self.request.GET.get('point')

        # Check if any of the required parameters is missing
        if None not in [distance, limit, point_str]:

            try:
                # Convert parameters to appropriate types
                distance, limit = float(distance), int(limit)
                longitude, latitude = map(float, point_str.split(','))
            except ValueError:
                return context

            # Create a Point object for the specified location
            point = Point(x=longitude, y=latitude, srid=4326)

            # Queryset with distance filter and ordering
            queryset = FoodTruck.objects.annotate(
                distance=Distance('location', point)
            ).order_by('distance').filter(distance__lte=distance)[:limit]

            # Calculate the centroid for all points in the queryset using Python
            if queryset:
                # Extract coordinates from queryset
                coordinates = [(food_truck.location.x, food_truck.location.y) for food_truck in queryset]

                # Calculate average coordinates as the centroid
                avg_longitude = sum(x for x, y in coordinates) / len(coordinates)
                avg_latitude = sum(y for x, y in coordinates) / len(coordinates)

                # Add the calculated centroid as the center point to the context
                context['center_point'] = {
                    'zoom_level': 16,
                    'latitude': avg_latitude,
                    'longitude': avg_longitude
                }

                context['location_points'] = [
                    {
                        'name': food_truck.applicant,
                        'address': food_truck.address,
                        'facility_type': food_truck.facility_type,
                        'latitude': food_truck.location.y,
                        'longitude': food_truck.location.x
                    }
                    for food_truck in queryset
                ]
                
            else:
                context['center_point'] = {
                    'zoom_level': 2,
                    'latitude': latitude,
                    'longitude': longitude
                }

        return context