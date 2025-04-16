import csv
from django.core.management.base import BaseCommand
from listings.models import Property

class Command(BaseCommand):
    help = "Import property data from CSV"

    def handle(self, *args, **kwargs):
        csv_file_path = "/Users/rgvmingudiya/Documents/RealHaven/real_estate_data_with_images_v1.csv"

        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Property.objects.create(
                    street_address=row["Street Address"],
                    city=row["City"],
                    state=row["State"],
                    zip_code=row["ZIP Code"],
                    price=row["Price"],
                    bedrooms=row["Bedrooms"],
                    bathrooms=row["Bathrooms"],
                    square_footage=row["Square Footage"],
                    property_type=row["Property Type"],
                    image_path=row["Image_Path"]
                )
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
