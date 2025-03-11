from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer

class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = "id"

class PropertySearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        # Start with all properties
        queryset = Property.objects.all()

        # Get the query parameters from the request
        street_address = self.request.query_params.get('street_address', None)
        zip_code = self.request.query_params.get('zip_code', None)
        property_type = self.request.query_params.get('property_type', None)

        # Filter based on the provided parameters
        if street_address:
            queryset = queryset.filter(address__icontains=street_address)  # Case-insensitive address search
        if zip_code:
            queryset = queryset.filter(zip_code=zip_code)  # Exact match for zip code
        if property_type:
            queryset = queryset.filter(property_type__iexact=property_type)  # Case-insensitive exact match for property type

        return queryset
