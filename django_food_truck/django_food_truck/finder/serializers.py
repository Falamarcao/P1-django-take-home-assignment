from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import FoodTruck

class FoodTruckSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = FoodTruck
        geo_field = 'location'

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        id_field = 'locationid'
        fields = '__all__'
        read_only_fields = ('',)
