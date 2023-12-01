from django.db.models import (Model, IntegerField, CharField, TextField, FloatField, URLField, DateTimeField)

from django.core.validators import URLValidator

from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point


class FoodTruck(Model):
    class Meta:
        verbose_name_plural = "Food Trucks"
    
    locationid = IntegerField(null=True, verbose_name="Location ID")
    applicant = TextField(null=True, verbose_name="Applicant")
    facility_type = CharField(max_length=50, null=True, verbose_name="Facility Type",
                              choices=[
                                  ('Push Cart', 'Push Cart'),
                                  ('Truck', 'Truck'),
                                  ]
                              )
    cnn = IntegerField(null=True, verbose_name="CNN")
    location_description = TextField(null=True, verbose_name="Location Description")
    address = TextField(null=True, verbose_name="Address")
    blocklot = CharField(max_length=20, null=True, verbose_name="Block Lot")
    block = CharField(max_length=10, null=True, verbose_name="Block")
    lot = CharField(max_length=10, null=True, verbose_name="Lot")
    permit = CharField(max_length=20, null=True, verbose_name="Permit")
    status = CharField(max_length=20, null=True, verbose_name="Status",
                       choices=[('APPROVED', 'Approved'),
                                ('REQUESTED', 'Requested'),
                                ]
                       )
    food_items = TextField(null=True, verbose_name="Food Items")
    x = FloatField(null=True, verbose_name="X")
    y = FloatField(null=True, verbose_name="Y")
    latitude = FloatField(null=True, verbose_name="Latitude")
    longitude = FloatField(null=True, verbose_name="Longitude")
    schedule = URLField(null=True, verbose_name="Schedule", validators=[URLValidator()])
    dayshours = TextField(null=True, verbose_name="Days/Hours")
    noisent = DateTimeField(null=True, verbose_name="NOI Sent")
    approved = DateTimeField(null=True, verbose_name="Approved")
    received = DateTimeField(null=True, verbose_name="Received")
    prior_permit = TextField(null=True, verbose_name="Prior Permit")
    expiration_date = DateTimeField(null=True, verbose_name="Expiration Date")
    location = PointField(geography=True, default=Point(0.0, 0.0), verbose_name="Location")
    fire_prevention_districts = IntegerField(null=True, verbose_name="Fire Prevention Districts")
    police_districts = IntegerField(null=True, verbose_name="Police Districts")
    supervisor_districts = IntegerField(null=True, verbose_name="Supervisor Districts")
    zip_codes = IntegerField(null=True, verbose_name="ZIP Codes")
    neighborhoods_old = IntegerField(null=True, verbose_name="Neighborhoods (Old)")


    def save(self, *args, **kwargs):
        # Automatically create a Point object from Latitude and Longitude
        if self.latitude is not None and self.longitude is not None and self.location is None:
            self.location = Point(self.latitude, self.longitude)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.applicant} - {self.location_description}"
