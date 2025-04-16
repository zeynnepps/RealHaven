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

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} - ${self.price}"
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed manually or use Django's PBKDF2

    def __str__(self):
        return self.email