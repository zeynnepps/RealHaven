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
from .models import Customer
from django.contrib.auth.hashers import make_password, check_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)