from django.contrib import admin
from .models import FoodTruck

@admin.register(FoodTruck)
class FoodTruckAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'location_description', 'status', 'schedule')
    search_fields = ('applicant', 'location_description', 'status')
    readonly_fields = ('location',)
