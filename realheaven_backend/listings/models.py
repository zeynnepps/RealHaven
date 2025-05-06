from django.db import models

# Create your models here.
from django.db import models

class Property(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_footage = models.IntegerField()
    property_type = models.CharField(max_length=50)
    image_path = models.ImageField(upload_to="property_images/", blank=True, null=True)
    
    #listing_type = models.CharField(max_length=50,default='For Sale')
    listing_type = models.CharField(
        max_length=50,
        choices=[
        ('for sale', 'For Sale'),
        ('rent', 'Rent'),
    ],
        default='for sale'
    )

   # Bedroom images
    bedroom_1 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)
    bedroom_2 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)
    bedroom_3 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)
    bedroom_4 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)
    bedroom_5 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)
    bedroom_6 = models.ImageField(upload_to='properties/bedrooms/', blank=True, null=True)

    # Bathroom images
    bathroom_1 = models.ImageField(upload_to='properties/bathrooms/', blank=True, null=True)
    bathroom_2 = models.ImageField(upload_to='properties/bathrooms/', blank=True, null=True)
    bathroom_3 = models.ImageField(upload_to='properties/bathrooms/', blank=True, null=True)
    bathroom_4 = models.ImageField(upload_to='properties/bathrooms/', blank=True, null=True)
    bathroom_5 = models.ImageField(upload_to='properties/bathrooms/', blank=True, null=True)

    # Other room images
    kitchen = models.ImageField(upload_to='properties/kitchen/', blank=True, null=True)
    living_room = models.ImageField(upload_to='properties/living_room/', blank=True, null=True)
    dining = models.ImageField(upload_to='properties/dining/', blank=True, null=True)
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} - ${self.price}"
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed manually or use Django's PBKDF2

    def __str__(self):
        return self.email