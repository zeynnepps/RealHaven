from rest_framework import serializers
from .models import Property
from django.conf import settings

class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'street_address', 'city', 'state', 'zip_code', 
            'price', 'bedrooms', 'bathrooms', 'square_footage', 
            'property_type', 'image_url'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image_path:
            return request.build_absolute_uri(obj.image_path.url) if request else f"{settings.MEDIA_URL}{obj.image_path}"
        return None
