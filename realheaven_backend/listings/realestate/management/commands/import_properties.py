import csv
from django.core.management.base import BaseCommand
from listings.models import Property

class Command(BaseCommand):
    help = "Import property data from CSV"

    def handle(self, *args, **kwargs):
        csv_file_path = "/Users/akhilkumar/Desktop/MSCS-SEM4/capstone course/RealHaven/data_part/real_estate_data_v3.csv"

        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                price = row.get("Price", "").replace(",", "")
                Property.objects.create(
                    street_address=row["Street Address"],
                    city=row["City"],
                    state=row["State"],
                    zip_code=row["ZIP Code"],
                    price=price,
                    bedrooms=row["Bedrooms"],
                    bathrooms=row["Bathrooms"],
                    square_footage=row["Square Footage"],
                    property_type=row["Property Type"],
                    image_path=row["Image_Path"],
                    # Added listing_type field
                    listing_type = row.get("listing_type", "").strip().title() or "For Sale",  # Default to "For Sale"
                    
                    # Bedroom image fields
                    bedroom_1=row.get("bedroom_1", ""),
                    bedroom_2=row.get("bedroom_2", ""),
                    bedroom_3=row.get("bedroom_3", ""),
                    bedroom_4=row.get("bedroom_4", ""),
                    bedroom_5=row.get("bedroom_5", ""),
                    bedroom_6=row.get("bedroom_6", ""),
                    
                    # Bathroom image fields
                    bathroom_1=row.get("bathroom_1", ""),
                    bathroom_2=row.get("bathroom_2", ""),
                    bathroom_3=row.get("bathroom_3", ""),
                    bathroom_4=row.get("bathroom_4", ""),
                    bathroom_5=row.get("bathroom_5", ""),
                    
                    # Other room image fields
                    kitchen=row.get("kitchen", ""),
                    living_room=row.get("living_room", ""),
                    dining=row.get("dining", ""),
                )
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
