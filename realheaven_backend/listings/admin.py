from django.contrib import admin

# Register your models here.
from .models import Property, Customer

admin.site.register(Property)
admin.site.register(Customer)