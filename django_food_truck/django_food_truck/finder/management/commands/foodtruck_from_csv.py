from ast import literal_eval
import csv
import re

from caseconverter import snakecase
from dateutil import parser
import pytz

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ...models import FoodTruck

class Command(BaseCommand):
    help = 'Loads the FoodTrucks data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_path']

        batch_size = 100
        food_trucks = []

        with open(csv_file_path, 'r') as file:
            header = file.readline().strip().split(',')

            header = [snakecase(column_name) for column_name in header]
            
            csv_reader = csv.DictReader(file, fieldnames=header)
         
            for index, row in enumerate(csv_reader):
                
                # Parse tuple string representation (lat, lng) to Point(tuple(lng,lat))
                try:
                    row['location'] = Point(tuple(reversed(literal_eval(row['location']))))
                except:
                    row['location'] = Point(0.0, 0.0)
                
                # Set null to empty values OR keep the current value
                row = {key: value or None for key, value in row.items()}
                
                # Parse dates/datetime to datetime object
                for field_name in ['noisent','approved','received','expiration_date']:
                    if row.get(field_name):
                        parsed_datetime = parser.parse(row[field_name])
                        parsed_datetime.replace(tzinfo=pytz.UTC)
                        row[field_name] = parsed_datetime
                
                food_truck = FoodTruck(**row)
                food_trucks.append(food_truck)
                
                # Bulk Create in batches
                if index % batch_size == 0 and index > 0:
                    FoodTruck.objects.bulk_create(food_trucks)
                    food_trucks = []

        # Insert any remaining entries
        if food_trucks:
            FoodTruck.objects.bulk_create(food_trucks)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded FoodTrucks data from CSV file: {csv_file_path}'))
