from django.urls import path
from .views import PropertyListView, PropertyDetailView,PropertySearchView, chatbot_api

urlpatterns = [
    path("properties/", PropertyListView.as_view(), name="property-list"),
    path("properties/<int:id>/", PropertyDetailView.as_view(), name="property-detail"),
    path('properties/search/', PropertySearchView.as_view(), name='property-search'),
    path("chatbot/", chatbot_api, name="chatbot_api"),
]
